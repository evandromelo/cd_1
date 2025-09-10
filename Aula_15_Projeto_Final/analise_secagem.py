import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ---------------------------
# 1. Importar dados simulados
# ---------------------------
dados = pd.read_csv("secagem.csv")

print("Primeiras linhas dos dados:")
print(dados.head())

# ---------------------------
# 2. Limpeza dos dados
# ---------------------------
# Remover valores nulos
dados = dados.dropna()

# Garantir que tempo está em ordem crescente
dados = dados.sort_values(by="tempo")

# ---------------------------
# 3. Análise básica
# ---------------------------
print("\nResumo estatístico:")
print(dados.describe())

# ---------------------------
# 4. Visualização
# ---------------------------
plt.scatter(dados["tempo"], dados["umidade"], label="Dados experimentais", color="blue")
plt.xlabel("Tempo (h)")
plt.ylabel("Umidade (kg água/kg ms)")
plt.title("Curva de Secagem - Folhas Medicinais")
plt.legend()
plt.grid(True)
plt.show()

# ---------------------------
# 5. Ajuste de modelo com SciPy
# ---------------------------
# Modelo exponencial de secagem: MR = exp(-k*t)
def modelo_exponencial(t, k):
    return np.exp(-k * t)

# Normalizando os dados para razão de umidade (MR)
umidade_inicial = dados["umidade"].iloc[0]
MR = dados["umidade"] / umidade_inicial

# Ajuste do modelo
parametros, _ = curve_fit(modelo_exponencial, dados["tempo"], MR, p0=[0.1])
k_otimo = parametros[0]

print(f"\nParâmetro ajustado (k): {k_otimo:.4f}")

# Plot do ajuste
plt.scatter(dados["tempo"], MR, label="MR experimental", color="blue")
plt.plot(dados["tempo"], modelo_exponencial(dados["tempo"], k_otimo),
         label=f"Ajuste exponencial (k={k_otimo:.4f})", color="red")
plt.xlabel("Tempo (h)")
plt.ylabel("Razão de Umidade (MR)")
plt.title("Ajuste de Modelo de Secagem")
plt.legend()
plt.grid(True)
plt.show()
