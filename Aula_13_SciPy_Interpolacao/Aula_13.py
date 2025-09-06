import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

prof = np.array([0,10,20,30])
temp = np.array([25,22,20,18])
f = interp1d(prof, temp, kind='linear')
novos = np.linspace(0,30,100)
plt.plot(prof, temp, 'o', novos, f(novos), '-')
plt.xlabel("Profundidade (cm)")
plt.ylabel("Temperatura (°C)")
plt.show()
