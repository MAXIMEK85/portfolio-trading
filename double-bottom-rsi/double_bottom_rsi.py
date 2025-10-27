import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# PARAMETERS

TICKERS = ["BTC-USD", "ETH-USD", "GOOG"]
LOOKBACK_PERIOD = "180d"
INTERVAL = "1h"
TOLERANCE = 0.15
SMOOTH_WINDOW = 10
RSI_WINDOW = 14
MIN_PEAK_DISTANCE = 5  # candles between bottoms and peak
MERGE_SECONDS = 3600  # merge signals within 1 hour

# RSI CALCULATION

def compute_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi


# FLEXIBLE DOUBLE BOTTOM DETECTION

def detect_double_bottoms_flexible(df):
    df["RSI"] = compute_rsi(df["Close"], RSI_WINDOW)
    smooth = df["Close"].rolling(window=SMOOTH_WINDOW).mean()
    df["Smooth"] = smooth

    peaks, _ = find_peaks(smooth)
    troughs, _ = find_peaks(-smooth)
    signals = []

    for i in range(len(troughs) - 1):
        lb = troughs[i]
        for j in range(i+1, len(peaks)):
            mp = peaks[j]
            if mp - lb < MIN_PEAK_DISTANCE:
                continue
            for k in range(j+1, len(troughs)):
                rb = troughs[k]
                if rb - mp < MIN_PEAK_DISTANCE:
                    continue

                # check bottoms are close
                if abs(df["Smooth"].iloc[lb] - df["Smooth"].iloc[rb]) / ((df["Smooth"].iloc[lb] + df["Smooth"].iloc[rb])/2) < TOLERANCE:
                    # check peak higher than bottoms
                    if df["Smooth"].iloc[mp] > (df["Smooth"].iloc[lb] + df["Smooth"].iloc[rb])/2:
                        rsi_alert = df["RSI"].iloc[rb] >= df["RSI"].iloc[lb]
                        signals.append({
                            "lb": lb,
                            "mp": mp,
                            "rb": rb,
                            "rsi_alert": rsi_alert,
                            "date": df.index[rb],
                            "price": df["Close"].iloc[rb]
                        })
                        break
            break
    return signals

# VISUALIZATION

def plot_double_bottoms(df, signals, ticker):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8), sharex=True)

    ax1.plot(df.index, df["Close"], label="Close", alpha=0.6)
    ax1.plot(df.index, df["Smooth"], alpha=0.3, label="Smooth")
    ax1.set_title(f"Detected Double Bottoms on {ticker}")

    for s in signals:
        ax1.scatter(df.index[s["lb"]], df["Smooth"].iloc[s["lb"]], color="blue")
        ax1.scatter(df.index[s["mp"]], df["Smooth"].iloc[s["mp"]], color="orange", marker="^", s=100)
        ax1.scatter(df.index[s["rb"]], df["Smooth"].iloc[s["rb"]], color="green")
        if s["rsi_alert"]:
            ax1.annotate("BUY", (df.index[s["rb"]], df["Smooth"].iloc[s["rb"]]),
                         textcoords="offset points", xytext=(0,15), ha='center', color="red", weight="bold")

    ax1.legend()

    ax2.plot(df.index, df["RSI"], color="purple", label="RSI")
    ax2.axhline(70, color="red", linestyle="--")
    ax2.axhline(30, color="green", linestyle="--")
    ax2.set_title("RSI (14 periods)")
    ax2.legend()

    plt.tight_layout()
    plt.show()


# MARKET SCAN WITH UNIQUE BUY POINTS

def scan_markets_once():
    print(f"🚀 Running Double Bottom + RSI scan ({LOOKBACK_PERIOD}, interval {INTERVAL})...\n")
    for ticker in TICKERS:
        try:
            df = yf.download(tickers=ticker, period=LOOKBACK_PERIOD, interval=INTERVAL,
                             progress=False, auto_adjust=True, group_by='column')
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] for col in df.columns]

            if 'Close' not in df.columns:
                print(f"❌ 'Close' column missing for {ticker}")
                continue

            df = df.dropna(subset=['Close'])
            signals = detect_double_bottoms_flexible(df)

            if signals:
                print(f"📈 {len(signals)} double bottom(s) detected on {ticker}")

                # Create initial summary table
                summary = pd.DataFrame([{"Date": s["date"], "Price": s["price"]} for s in signals])
                summary = summary.sort_values(by="Date").reset_index(drop=True)

                # Merge nearby signals: keep only the first in a group within MERGE_SECONDS
                merged_summary = []
                prev_date = None
                for idx, row in summary.iterrows():
                    if prev_date is None or (row["Date"] - prev_date).total_seconds() > MERGE_SECONDS:
                        merged_summary.append(row)
                        prev_date = row["Date"]

                merged_summary = pd.DataFrame(merged_summary)

                print(f"\n--- BUY POINTS SUMMARY for {ticker} ---")
                print(merged_summary.to_string(index=False))
                print("\n")
                plot_double_bottoms(df, signals, ticker)
            else:
                print(f"🔎 No signals detected on {ticker}")

        except Exception as e:
            print(f"❌ Error scanning {ticker}: {e}")

    print("\n✅ Scan completed.\n")

if __name__ == "__main__":
    scan_markets_once()





