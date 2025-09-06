import matplotlib.pyplot as plt
import numpy as np
horas = [1,2,3,4,5]
secagem1 = [25.0,22.5,20.1,18.0,16.2]
secagem2 = [25.0,21.0,18.5,16.5,15.0]
plt.subplot(1,2,1)
plt.plot(horas, secagem1, label="40°C")
plt.plot(horas, secagem2, label="60°C")
plt.legend()
plt.subplot(1,2,2)
plt.boxplot([secagem1, secagem2], labels=["40°C","60°C"])
plt.show()