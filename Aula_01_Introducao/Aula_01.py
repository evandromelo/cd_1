temperaturas = [32.5, 33.1, 31.8, 34.0, 33.5, 32.8]
media = sum(temperaturas)/len(temperaturas)

print("Média:", media)
horarios = ["08h","10h","12h","14h","16h","18h"]
dados = dict(zip(horarios, temperaturas))
print(dados)