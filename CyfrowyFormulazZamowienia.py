import pandas as pd
from pandas import DataFrame
import numpy as np

path = './Resources/CFZ_LuksLamp_201103_1.xlsx'

df = pd.read_excel(path, 'Pozycje')
df = df.dropna()
print(df.to_string(index=False))
