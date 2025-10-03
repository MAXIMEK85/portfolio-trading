import yfinance as yf
import matplotlib.pyplot as plt

ticker = "AAPL"


data = yf.download(ticker, start="2022-01-01", end="2023-12-31")
print(f"Nombre de lignes téléchargées : {len(data)}")
if data.empty:
	print("Aucune donnée téléchargée. Vérifiez votre connexion internet ou le ticker.")
	exit()


plt.figure(figsize=(10, 5))
plt.plot(data['Close'], label="Close Price")
plt.title(f"Évolution du prix de {ticker} (1 an)")
plt.xlabel("Date")
plt.ylabel("Prix ($)")
plt.legend()
plt.show()