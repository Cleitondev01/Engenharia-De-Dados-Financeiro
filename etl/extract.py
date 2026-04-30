import requests
import yfinance as yf
import pandas as pd
from datetime import datetime

# ==========================================
# 1. ÍNDICES MACRO (SELIC, CDI, IPCA)
# ==========================================
def extrair_indicadores():
    series = {"Selic": "1178", "CDI": "4389", "IPCA": "433"}
    lista_macro = []
    for nome, codigo in series.items():
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"
        try:
            response = requests.get(url)
            dados = response.json()
            lista_macro.append({
                "indicador": nome,
                "valor": float(dados[0]['valor']), 
                "data": dados[0]['data']
            })
        except Exception as e:
            print(f"Erro ao extrair {nome}: {e}")
    return pd.DataFrame(lista_macro) 

# ==========================================
# 2. MOEDAS (CÂMBIO HÍBRIDO)
# ==========================================
def extrair_yuan():
    ticker = yf.Ticker("CNYBRL=X")
    dados = ticker.history(period="1d")
    valor = float(round(dados["Close"].iloc[-1], 4))
    data = dados.index[-1].strftime("%d/%m/%Y")
    return {"moeda": "Yuan", "valor": valor, "data": data}

def extrair_moedas():
    series = {"Dolar": "1", "Euro": "21619"}
    lista_moedas = []
    for nome, codigo in series.items():
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"
        try:
            response = requests.get(url)
            dados = response.json()
            lista_moedas.append({
                "moeda": nome,
                "valor": float(dados[0]['valor']),
                "data": dados[0]['data']
            })
        except Exception as e:
            print(f"Erro ao extrair {nome}: {e}")
    lista_moedas.append(extrair_yuan())
    return pd.DataFrame(lista_moedas)

# ==========================================
# 3. RANKING DE AÇÕES (TOP 7)
# ==========================================
def extrair_ranking_completo():
    tickers = [
        "PETR4.SA", "PETR3.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", 
        "ABEV3.SA", "BBAS3.SA", "B3SA3.SA", "MGLU3.SA", "WEGE3.SA", 
        "HAPV3.SA", "RENT3.SA", "SUZB3.SA", "GGBR4.SA", "JBSS3.SA", 
        "RAIL3.SA", "EQTL3.SA", "VIVT3.SA", "LREN3.SA", "PRIO3.SA", 
        "RDOR3.SA", "SBSP3.SA", "CPLE6.SA", "CSAN3.SA", "EMBR3.SA",
        "BRKM5.SA", "HYPE3.SA", "SLCE3.SA", "ELET3.SA", "MULT3.SA"
    ]
    lista_resultados = []
    for t in tickers:
        try:
            acao = yf.Ticker(t)
            hist = acao.history(period="2d")
            if len(hist) >= 2:
                p_atual = hist['Close'].iloc[-1]
                p_anterior = hist['Close'].iloc[-2]
                variacao = ((p_atual - p_anterior) / p_anterior) * 100
                lista_resultados.append({
                    "ticker": t.replace(".SA", ""),
                    "preco": round(p_atual, 2),
                    "variacao": round(variacao, 2)
                })
        except: continue
    df_base = pd.DataFrame(lista_resultados)
    altas = df_base.sort_values(by="variacao", ascending=False).head(7).reset_index(drop=True)
    baixas = df_base.sort_values(by="variacao", ascending=True).head(7).reset_index(drop=True)
    return altas, baixas

# ==========================================
# 4. CRIPTOMOEDAS
# ==========================================
def extrair_criptos():
    tickers_cripto = {"Bitcoin": "BTC-USD", "Ethereum": "ETH-USD", "Solana": "SOL-USD"}
    try:
        dolar_data = yf.Ticker("USDBRL=X").history(period="1d")
        cotacao_dolar = dolar_data['Close'].iloc[-1]
    except:
        cotacao_dolar = 5.00 
    lista_criptos = []
    for nome, ticker in tickers_cripto.items():
        try:
            cripto = yf.Ticker(ticker)
            hist = cripto.history(period="5d")
            if not hist.empty:
                valor_usd = hist['Close'].iloc[-1]
                valor_anterior_usd = hist['Close'].iloc[-2]
                valor_brl = valor_usd * cotacao_dolar
                variacao = ((valor_usd - valor_anterior_usd) / valor_anterior_usd) * 100
                lista_criptos.append({
                    "cripto": nome,
                    "preco_brl": round(valor_brl, 2),
                    "variacao": round(variacao, 2),
                    "data": hist.index[-1].strftime("%d/%m/%Y")
                })
        except: continue
    return pd.DataFrame(lista_criptos)

# ==========================================
# TESTE LOCAL (SÓ RODA SE DER PLAY AQUI)
# ==========================================
if __name__ == "__main__":
    print("\n--- MODO DE TESTE (EXTRACT) ---")
    print(extrair_indicadores())
    print(extrair_moedas())
    print(extrair_criptos())
    print(extrair_ranking_completo())