import requests
import yfinance as yf

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



