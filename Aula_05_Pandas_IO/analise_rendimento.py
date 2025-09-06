# -*- coding: utf-8 -*-

# Importa a biblioteca pandas
import pandas as pd

# Define o nome do arquivo Excel a ser lido
nome_arquivo_excel = 'rendimentos.xlsx'

try:
    # 1. Importa os dados da planilha Excel para um DataFrame
    # O Pandas lê o arquivo e o transforma em uma tabela (DataFrame)
    df_rendimento = pd.read_excel(nome_arquivo_excel)

    # 2. Imprime os dados importados
    print(f"--- Dados de Rendimento Importados de '{nome_arquivo_excel}' ---")
    print(df_rendimento)

    # 3. Calcula a média da coluna de rendimentos
    # Seleciona a coluna 'Rendimento de Óleo (%)' e usa o método .mean()
    media_rendimento = df_rendimento['Rendimento de Óleo (%)'].mean()

    # 4. Imprime o resultado do cálculo
    print("\n--- Análise dos Dados ---")
    print(f"A média do rendimento de óleo é: {media_rendimento:.2f}%")

except FileNotFoundError:
    print(f"\nERRO: O arquivo '{nome_arquivo_excel}' não foi encontrado.")
    print("Por favor, certifique-se de que o arquivo está na mesma pasta que o script,")
    print("ou execute o script 'criar_planilha_exemplo.py' primeiro.")