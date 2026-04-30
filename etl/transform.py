import extract as ext
import pandas as pd

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

    # Imprime apenas o resultado final que você quer
    print("\n[TABELA B3 TOP 7 MAIORES ALTAS]")
    print(df_altas)

    print("\n[TABELA B3 TOP 7 MAIORES BAIXAS]")
    print(df_baixas)
    
    print("\n[TABELA CRIPTOS]")
    print(df_cripto)

    print("\n[TABELA MOEDAS]")
    print(df_moedas)

    print("\n[TABELA MACROS]")
    print(df_macro)

if __name__ == "__main__":
    transformar_dados()