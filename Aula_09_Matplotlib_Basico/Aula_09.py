import matplotlib.pyplot as plt
horas = [1,2,3,4,5]
umidade = [25.0,22.5,20.1,18.0,16.2]
plt.plot(horas, umidade, marker='o')
plt.xlabel("Hora")
plt.ylabel("Teor de água (% b.s.)")
plt.title("Curva de Secagem")
plt.show()