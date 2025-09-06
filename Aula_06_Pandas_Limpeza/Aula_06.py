import pandas as pd
import numpy as np
dados = {'Hora':[1,2,3,4,5], 'Temp':[25.0,np.nan,26.5,26.0,25.8]}
df = pd.DataFrame(dados)
print("Original:\n", df)
df['Temp'] = df['Temp'].fillna(df['Temp'].mean())
print("Corrigido:\n", df)