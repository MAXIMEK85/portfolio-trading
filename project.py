import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def main():

    print("Stock market trend analyzer(MA50/MA200)")
    symbol = input("Enter the stock of your choice (ex:AAPL, MSFT, MMM):")

    try:

        data = get_stock_data(symbol)

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]
        data = calculate_ma(data, 50)
        data = calculate_ma(data, 200)

        trends = determine_trends(data)

        print(f"\nResults for {symbol} :")
        print(f"Trend {trends['short_term']}")
        print(f"Trend {trends['long_term']}")
        print(f"Last Price : {round(data['Close'].iloc[-1], 2)} $")

        plot_trends(data, symbol)

    except Exception as e:
        print("Error:", e)

def get_stock_data(symbol, period="5y"):

    data = yf.download(symbol, period=period, interval="1wk")
    if data.empty:
        raise ValueError("Symbol Error")

    return data

def calculate_ma(data, window):
    data[f"MA_{window}"] = data["Close"].rolling(window = window).mean()
    return data

def determine_trends(data):

    required_cols = ["MA_50", "MA_200"]

    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing column {col}")

    data = data.dropna(subset=required_cols)
    if data.empty :
        raise ValueError("Not enough data")
    last = data.iloc[-1]
    trends = {}

    #short-term
    if last["Close"] > last["MA_50"]:
        trends["short_term"] = "short-term bullish"
    else:
        trends["short_term"] = "short-term bearish"

    #short-term
    if last["Close"] > last["MA_200"]:
        trends["long_term"] = "long-term bullish"
    else:
        trends["long_term"] = "long-term bearish"

    return trends

def plot_trends(data, symbol):

    plt.figure(figsize=(10, 5))
    plt.plot(data["Close"], label="Prix", color="black")
    plt.plot(data["MA_50"], label="MA 50", color="blue", linestyle="--")
    plt.plot(data["MA_200"], label="MA 200", color="orange", linestyle="--")
    plt.title(f"Trend of {symbol} (MA 50 & 200 week)")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True)

    file_name = f"{symbol}_trend.png"
    plt.savefig(file_name, dpi=300)
    print(f"graph saved as '{file_name}'")



if __name__ == "__main__":
    main()
