import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Dados experimentais (simulados)
tempo = np.array([0,1,2,3,4,5])
teor = np.array([25,20,16,13,11,10])

def modelo(t, a, b):
    return a*np.exp(-b*t)
params, _ = curve_fit(modelo, tempo, teor)
plt.scatter(tempo, teor, label="Dados")
plt.plot(tempo, modelo(tempo, *params), label="Ajuste", color='red')
plt.legend()
plt.show()
