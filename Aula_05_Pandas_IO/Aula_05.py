import pandas as pd
dados = {'Temperatura':[40,50,60], 'Rendimento (%)':[1.2,1.8,2.1]}
df = pd.DataFrame(dados)
print(df)
df.to_csv("rendimentos.csv", index=False)