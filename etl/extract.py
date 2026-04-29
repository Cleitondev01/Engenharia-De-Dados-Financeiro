import requests
import yfinance as yf
import pandas as pd

def extrair_indicadores():
    # Dicionário de séries: Nome -> Código SGS
    series = {
        "Selic": "1178",
        "CDI": "4389",
        "IPCA": "433"
    }
    
    resultados = {}

    for nome, codigo in series.items():
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()
            
            # Armazenando o valor e a data
            resultados[nome] = {
                "valor": dados[0]['valor'],
                "data": dados[0]['data']
            }
            print(f"Sucesso ao extrair {nome}: {dados[0]['valor']} na data {dados[0]['data']}")
            
        except Exception as e:
            print(f"Erro ao extrair {nome}: {e}")
            
    return resultados

# Execução
indices = extrair_indicadores()



# MOEDAS

def extrair_yuan():
    ticker = yf.Ticker("CNYBRL=X")
    dados = ticker.history(period="1d")

    valor = float(round(dados["Close"].iloc[-1], 4))
    data = dados.index[-1].strftime("%d/%m/%Y")

    print(f"Sucesso ao extrair Yuan: {valor} na data {data}")
    return {"valor": valor, "data": data}


def extrair_moedas():
    series = {
        "Dolar": "1",
        "Euro": "21619",
    }

    resultados = {}

    for nome, codigo in series.items():
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"

        try:
            response = requests.get(url)
            response.raise_for_status()
            dados = response.json()

            resultados[nome] = {
                "valor": dados[0]['valor'],
                "data": dados[0]['data']
            }
            print(f"Sucesso ao extrair {nome}: {dados[0]['valor']} na data {dados[0]['data']}")

        except Exception as e:
            print(f"Erro ao extrair {nome}: {e}")

    yuan = extrair_yuan()
    resultados["Yuan"] = yuan

    return resultados


# Teste
moedas = extrair_moedas()
print(moedas)


# FIN

def extrair_ranking_acoes():
    # 1. Definimos os tickers (adicione os que desejar monitorar)
    tickers = [
        "PETR4.SA", "VALE3.SA", "ITUB4.SA", "MGLU3.SA", "B3SA3.SA", 
        "BRKM5.SA", "HYPE3.SA", "PETR3.SA", "PRIO3.SA", "SLCE3.SA",
        "CYRE4.SA", "CSAN3.SA", "BEEF3.SA", "EMBJ3.SA"
    ]
    
    lista_resultados = []

    print("Extraindo dados da B3...")
    for t in tickers:
        try:
            acao = yf.Ticker(t)
            # Pegamos os dados de hoje
            hist = acao.history(period="2d") # Pegamos 2 dias para calcular a variação de ontem para hoje
            
            if len(hist) >= 2:
                preco_atual = hist['Close'].iloc[-1]
                preco_anterior = hist['Close'].iloc[-2]
                
                # Cálculo da variação percentual
                variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100
                
                lista_resultados.append({
                    "ticker": t.replace(".SA", ""),
                    "preco": round(preco_atual, 2),
                    "variacao": round(variacao, 2)
                })
        except Exception as e:
            print(f"Erro ao extrair {t}: {e}")

    # 2. Transformamos em um DataFrame para rankear fácil
    df = pd.DataFrame(lista_resultados)

    # 3. Criamos os Rankings
    maiores_altas = df.sort_values(by="variacao", ascending=False).head(7)
    maiores_baixas = df.sort_values(by="variacao", ascending=True).head(7)

    return maiores_altas, maiores_baixas

# Executando
altas, baixas = extrair_ranking_acoes()

print("\n--- MAIORES ALTAS ---")
print(altas)

print("\n--- MAIORES BAIXAS ---")
print(baixas)
