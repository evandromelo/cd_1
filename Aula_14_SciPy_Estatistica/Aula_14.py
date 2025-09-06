import numpy as np
from scipy import stats

grupo1 = [1.2, 1.3, 1.1]
grupo2 = [1.8, 1.7, 1.9]
grupo3 = [2.1, 2.0, 2.2]

f, p = stats.f_oneway(grupo1, grupo2, grupo3)
print("ANOVA F=", f, "p=", p)
