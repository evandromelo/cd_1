import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Dados simulados
dados = {'Tempo':[0,1,2,3,4,5], 'Teor_água':[25,20,16,13,11,10]}
df = pd.DataFrame(dados)

# Estatísticas
print(df.describe())

# Ajuste de modelo
def modelo(t, a, b):
    return a*np.exp(-b*t)

params, _ = curve_fit(modelo, df['Tempo'], df['Teor_água'])

# Visualização
plt.scatter(df['Tempo'], df['Teor_água'], label="Dados")
plt.plot(df['Tempo'], modelo(df['Tempo'], *params), label="Ajuste", color="red")
plt.xlabel("Tempo (h)")
plt.ylabel("Teor de água (% bu)")
plt.legend()
plt.show()
