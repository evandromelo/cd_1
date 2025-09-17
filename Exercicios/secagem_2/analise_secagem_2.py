# Importando bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# 1. IMPORTAR OS DADOS
print("1. Importando dados do arquivo CSV...")
file_path = 'dados_secagem_folhas.csv'

if not os.path.exists(file_path):
    print(f"ERRO: O arquivo '{file_path}' não foi encontrado.")
    print("Por favor, crie o arquivo com os dados simulados fornecidos.")
    exit()

df = pd.read_csv(file_path)
print("Dados importados com sucesso!")
print("\nPrimeiras linhas do DataFrame:")
print(df.head())
print(f"\nDimensões do DataFrame: {df.shape}")
print(f"Colunas: {list(df.columns)}")

# 2. LIMPAR OS DADOS
print("\n2. Limpando os dados...")
# Verificar valores nulos
print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")

# Se houver nulos, poderíamos preencher ou remover. Aqui, apenas alertamos.
if df.isnull().sum().sum() > 0:
    print("Atenção: Existem valores nulos. Considere tratá-los.")
    # Exemplo: df = df.dropna()  # ou df = df.fillna(method='ffill')

# Verificar duplicatas
duplicatas = df.duplicated().sum()
print(f"Linhas duplicadas: {duplicatas}")
if duplicatas > 0:
    df = df.drop_duplicates()
    print("Duplicatas removidas.")

# Verificar tipos de dados
print(f"\nTipos de dados:\n{df.dtypes}")

# Converter, se necessário (não é o caso aqui, mas é boa prática)
# df['tempo_h'] = pd.to_numeric(df['tempo_h'], errors='coerce')

print("Limpeza concluída. Dados prontos para análise.")

# 3. ANALISAR OS DADOS
print("\n3. Analisando os dados...")
print("\nEstatísticas descritivas:")
print(df.describe())

print("\nInformações gerais do experimento:")
temp_const = df['temperatura_C'].unique()
vel_const = df['velocidade_ar_m_s'].unique()
print(f"Temperatura(s) utilizada(s): {temp_const} °C")
print(f"Velocidade(s) do ar utilizada(s): {vel_const} m/s")

# Verificar se as condições são constantes (como em um experimento controlado)
if len(temp_const) == 1 and len(vel_const) == 1:
    print("Condições experimentais são constantes. Análise univariada (umidade vs tempo) é válida.")
else:
    print("Atenção: Condições variam. Análise mais complexa pode ser necessária.")

# 4. VISUALIZAR OS DADOS
print("\n4. Visualizando os dados...")
plt.figure(figsize=(10, 6))
plt.plot(df['tempo_h'], df['umidade_g_agua_g_ms'], 'bo-', label='Dados Experimentais')
plt.title('Curva de Secagem de Folhas de Planta Medicinal', fontsize=14)
plt.xlabel('Tempo (h)', fontsize=12)
plt.ylabel('Umidade (g água / g matéria seca)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# 5. AJUSTAR MODELO COM SCIPY
print("\n5. Ajustando modelo com SciPy...")

# Escolher um modelo teórico comum para secagem: Modelo Exponencial de 1ª ordem
# Umidade(t) = Umidade_eq + (Umidade_0 - Umidade_eq) * exp(-k * t)
# Onde:
#   Umidade_0: umidade inicial
#   Umidade_eq: umidade de equilíbrio (assintótica)
#   k: constante de secagem

def modelo_exponencial(t, U_eq, k):
    U_0 = df['umidade_g_agua_g_ms'].iloc[0]  # Pega a umidade inicial dos dados
    return U_eq + (U_0 - U_eq) * np.exp(-k * t)

# Preparar dados para ajuste
t_data = df['tempo_h'].values
U_data = df['umidade_g_agua_g_ms'].values

# Chute inicial para os parâmetros [U_eq, k]
# U_eq: valor próximo ao último ponto
# k: um valor positivo pequeno
p0 = [U_data[-1], 0.5]

# Realizar o ajuste
try:
    popt, pcov = curve_fit(modelo_exponencial, t_data, U_data, p0=p0)
    U_eq_ajustado, k_ajustado = popt
    print(f"Parâmetros ajustados:")
    print(f"  Umidade de Equilíbrio (U_eq) = {U_eq_ajustado:.4f} g água / g ms")
    print(f"  Constante de Secagem (k)      = {k_ajustado:.4f} h⁻¹")

    # Calcular R²
    U_pred = modelo_exponencial(t_data, *popt)
    ss_res = np.sum((U_data - U_pred) ** 2)
    ss_tot = np.sum((U_data - np.mean(U_data)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print(f"  Coeficiente de Determinação (R²) = {r_squared:.4f}")

    # Plotar dados e curva ajustada
    t_fino = np.linspace(t_data.min(), t_data.max(), 100)
    U_ajustado_fino = modelo_exponencial(t_fino, *popt)

    plt.figure(figsize=(10, 6))
    plt.plot(t_data, U_data, 'bo', label='Dados Experimentais', markersize=6)
    plt.plot(t_fino, U_ajustado_fino, 'r-', label='Modelo Ajustado (Exponencial)', linewidth=2)
    plt.title('Ajuste do Modelo Exponencial aos Dados de Secagem', fontsize=14)
    plt.xlabel('Tempo (h)', fontsize=12)
    plt.ylabel('Umidade (g água / g matéria seca)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Erro ao ajustar o modelo: {e}")

print("\nAnálise completa concluída com sucesso!")