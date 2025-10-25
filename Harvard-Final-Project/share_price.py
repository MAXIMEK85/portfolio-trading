# share_price.py
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#Apple
ticker = "AAPL"  
data = yf.download(ticker, start="2022-01-01", end="2023-12-31")

data['SMA'] = data['Close'].rolling(window=20).mean()

# Calcul de la moyenne mobile sur 20 jours
data['SMA'] = data['Close'].rolling(window=20).mean()

plt.plot(data['Close'], label='Close')
plt.plot(data['SMA'], label='SMA 20')
plt.title(f"Analyse de {ticker}")
plt.legend()
plt.show()
