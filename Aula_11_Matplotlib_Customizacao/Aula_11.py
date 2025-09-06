import matplotlib.pyplot as plt
horas = [1,2,3,4,5]
umid1 = [25,22,20,18,16]
umid2 = [25,21,18,16,14]
plt.plot(horas, umid1, 'o-r', label="40°C")
plt.plot(horas, umid2, 's-b', label="60°C")
plt.xlabel("Tempo (h)")
plt.ylabel("Umidade (%)")
plt.title("Curvas de Secagem")
plt.legend()
plt.show()