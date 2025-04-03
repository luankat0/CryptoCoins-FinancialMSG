import os
import smtplib
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from email.mime.text import MIMEText

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

# Retornos diários
dados["Daily Return"] = dados["BTC-USD"].pct_change()

dados["Volatility"] = dados["Daily Return"].rolling(window=7).std()
# Plotando volatilidade
plt.figure(figsize=(12,6))
plt.plot(dados.index, dados["Volatility"], label="Volatibilidade BTC", color='purple')

plt.xlabel("Data")
plt.ylabel("Volatibilidade (Desvio Padrão)")
plt.title("Volatibilidade do BTC (7 dias)")
plt.legend()
plt.grid()
plt.show()

# Configuração do Email

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_DEST = os.getenv("EMAIL_DEST")

# Preço alvo
ALERTA_BTC = 62500

preco_atual = dados["BTC-USD"].iloc[-1]

if preco_atual >= ALERTA_BTC:
    msg = MIMEText(f"O preço do BTC atingiu {preco_atual:.2f} USD")
    msg["Subject"] = "Alerta BTC"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_DEST

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_DEST, msg.as_string())
    
    print("Alerta enviado!")

else:
    print(f"BTC ainda não atingiu o preço-alvo ({preco_atual:.2f} USD)")