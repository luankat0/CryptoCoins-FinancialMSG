import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = ["BTC-USD", "ETH-USD", "USDT-USD"]

dados = yf.download(tickers, period="6mo")
dados = dados["Close"]
print(dados.head())

plt.figure(figsize=(12,6))
for cripto in tickers:
    plt.plot(dados.index, dados[cripto], label=cripto)

plt.xlabel("Data")
plt.ylabel("Preço (USD)")
plt.title("Evolução dos Preços - BTC, ETH, USDT")
plt.legend()
plt.grid()
plt.show()

# Médias Móveis entre 7 e 30 dias
dados["MA7"] = dados["BTC-USD"].rolling(window=7).mean()
dados["MA30"] = dados["BTC-USD"].rolling(window=30).mean()

# Plotando médias moveis e preço
plt.figure(figsize=(12,6))
plt.plot(dados.index, dados["BTC-USD"], label="Preço BTC", color='blue')
plt.plot(dados.index, dados["MA7"], label="Média Móvel 7d", color='orange')
plt.plot(dados.index, dados["MA30"], label="Média Móvel 30d", color='red')

plt.xlabel("Data")
plt.ylabel("Preço (USD)")
plt.title("Evolução do BTC com Médias Móveis")
plt.legend()
plt.grid()
plt.show()

# Volatidade
dados["Daily Return"] = dados["BTC-USD"].pct_change()

# Plotando volatilidade
plt.figure(figsize=(12,6))
plt.plot(dados.index, dados["Volatility"], label="Volatibilidade BTC", color='purple')

plt.xlabel("Data")
plt.ylabel("Volatibilidade (Desvio Padrão)")
plt.title("Volatibilidade do BTC (7 dias)")
plt.legend()
plt.grid()
plt.show()

