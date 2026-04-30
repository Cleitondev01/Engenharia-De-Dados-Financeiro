import extract as ext
import pandas as pd
import numpy as np

def transformar_dados():
    # Extração silenciosa
    df_macro = ext.extrair_indicadores()
    df_moedas = ext.extrair_moedas()
    df_altas, df_baixas = ext.extrair_ranking_completo()
    df_cripto = ext.extrair_criptos()

    # Transformação
    df_altas['tipo'] = 'Alta'
    df_baixas['tipo'] = 'Baixa'
    df_b3 = pd.concat([df_altas, df_baixas]).reset_index(drop=True)

    # Renomeando a coluna 'tipo' para algo melhor
    df_b3.rename(columns={'tipo': 'tendencia_dia'}, inplace=True)


    # --- CRIAÇÃO DA COLUNA DE VARIAÇÃO NOMINAL ---
    # Aplico a fórmula: Preco / (1 + (Variacao/100)) para achar o preço anterior
    # Depois subtraímos do preço atual para ter a diferença em Reais

    df_b3['variacao_rs'] = df_b3['preco'] - (df_b3['preco'] / (1 + (df_b3['variacao'] / 100)))
    
    # Arredondando para 2 casas decimais
    df_b3['variacao_rs'] = df_b3['variacao_rs'].round(2)


    # --- PADRONIZAÇÃO B3 (Ações) ---
    condicoes_b3 = [
        (df_b3['variacao'] > 3),            # Subiu muito
        (df_b3['variacao'] < -3),           # Caiu muito
        (df_b3['variacao'].between(-1, 1))  # Quase não mudou
    ]

    categorias_b3 = [
        'Alta Relevante',   # Em vez de Alta Volatilidade
        'Queda Relevante',  # Em vez de Baixa Volatilidade
        'Estável / Sem Tendência'
    ]

    df_b3['status_mercado'] = np.select(condicoes_b3, categorias_b3, default='Oscilação Comum')

    # Criptos:
    df_cripto['variacao_rs'] = df_cripto['preco_brl'] - (df_cripto['preco_brl'] / (1 + (df_cripto['variacao'] / 100)))
    df_cripto['variacao_rs'] = df_cripto['variacao_rs'].round(2)

    # --- PADRONIZAÇÃO CRIPTO ---
    condicoes_cripto = [
        (df_cripto['variacao'] > 7),            # Subiu muito
        (df_cripto['variacao'] < -7),           # Caiu muito
        (df_cripto['variacao'].between(-2, 2))  # Quase não mudou
    ]

    categorias_cripto = [
        'Forte Alta',
        'Forte Queda',
        'Estável'
    ]
    df_cripto['status_mercado'] = np.select(condicoes_cripto, categorias_cripto, default='Oscilação Comum')


    # Moedas: Arredondando o câmbio para 2 casas (ex: 4.9886 -> 4.99)
    df_moedas['valor'] = df_moedas['valor'].round(2)

    # Macros: Garantindo que Selic e IPCA também fiquem com 2 casas
    df_macro['valor'] = df_macro['valor'].round(2)





    return df_b3, df_macro, df_moedas, df_cripto

b3, macro, moedas, cripto = transformar_dados()


# TRATAMENTO B3
#print(b3.dtypes)
#print(b3)


#TRATAMENTO MACROS
#print(macro.dtypes)
#print(macro)

# mudando a data de str para datetime64
macro['data'] = pd.to_datetime(macro['data'], dayfirst=True)

#print(macro.dtypes)
#print(macro)

# MOEDAS
#print(moedas.dtypes)
#print(moedas)

moedas['data'] = pd.to_datetime(moedas['data'], dayfirst=True)
#print (moedas)
#print(moedas.dtypes)

# CRIPTOS
#print(cripto.dtypes)
print(cripto)

cripto['data'] = pd.to_datetime(cripto['data'], dayfirst=True)
#print(cripto)
#print(cripto.dtypes)



    # Imprime apenas o resultado final que você quer
print("\n[TABELA B3]")
print(b3)
print("\n[TABELA CRIPTOS]")
print(cripto)
print("\n[TABELA MOEDAS]")
print(moedas)
print("\n[TABELA MACROS]")
print(macro)

#if __name__ == "__main__":
#    transformar_dados()