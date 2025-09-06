import pandas as pd
dados = {'Temp':[40,40,50,50,60,60], 'Rendimento':[1.1,1.3,1.8,1.9,2.0,2.2]}
df = pd.DataFrame(dados)
print(df.groupby('Temp').mean())