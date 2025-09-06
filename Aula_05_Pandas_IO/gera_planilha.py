# -*- coding: utf-8 -*-

import pandas as pd

# Cria um DataFrame de exemplo com os dados
dados_exemplo = {
    'Temperatura (°C)': [60, 70, 80, 90, 100, 110],
    'Rendimento de Óleo (%)': [1.25, 1.52, 1.98, 2.21, 2.15, 1.89]
}
df_exemplo = pd.DataFrame(dados_exemplo)

# Salva o DataFrame em um arquivo Excel
# O parâmetro index=False evita que o índice do DataFrame seja salvo no arquivo
nome_arquivo = 'rendimentos.xlsx'
df_exemplo.to_excel(nome_arquivo, index=False)

print(f"Arquivo Excel '{nome_arquivo}' criado com sucesso!")
print("Agora você pode executar o script 'rendimento_oleo.py' para ler estes dados.")