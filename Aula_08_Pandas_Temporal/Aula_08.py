import pandas as pd
rng = pd.date_range('2024-01-01', periods=6, freq='H')
dados = pd.Series([80,82,81,83,85,84], index=rng)
print("Série original:\n", dados)
print("Reamostrado diário:\n", dados.resample('D').mean())