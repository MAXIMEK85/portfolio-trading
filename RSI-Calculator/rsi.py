import yfinance as yf
import matplotlib.pyplot as plt

ticker = input("Entrez le symbole de l'action (ex: AAPL, TSLA) : ").upper()

start_date = '2020-01-01'
end_date = '2025-10-25'

data = yf.download(ticker, start=start_date, end=end_date)
if data.empty:
    print(f"Nothing found for {ticker}. Check the stock and the internet connectiont.")
    exit()

#RSI
window = 14
delta = data["Close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(window=window).mean()
avg_loss = loss.rolling(window=window).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

data["RSI"] = rsi
# Graph
plt.figure(figsize=(12,8))

# Prix de clôture
plt.subplot(2,1,1)
plt.plot(data.index, data["Close"], label="Close Price")
plt.title("Price")
plt.legend()

# RSI
plt.subplot(2,1,2)
plt.plot(data.index, data["RSI"], label="RSI", color="orange")
plt.axhline(70, color="red", linestyle="--")
plt.axhline(30, color="green", linestyle="--")
plt.title("Relative Strength Index (RSI)")
plt.legend()

plt.tight_layout()
#Graphique show
plt.show()


