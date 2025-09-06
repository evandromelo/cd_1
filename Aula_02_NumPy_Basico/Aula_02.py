import numpy as np
dados = [32.5, 33.1, 31.8, 34.0, 33.5, 32.8]
arr = np.array(dados)
# modo 1 calcular média e desvio padrão
print("Média:", arr.mean(), "Desvio:", arr.std(), "\n")
# modo 2 calcula média e desvio padrão
print("Média:", np.mean(arr), "Desvio:", np.std(arr), "\n")

