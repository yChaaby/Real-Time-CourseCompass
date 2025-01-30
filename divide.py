import pandas as pd
import numpy as np

# Charger le fichier CSV
df = pd.read_csv('/Users/youssefchaabi/change name.csv')

# Calculer la taille de chaque partie
num_parts = 10
rows_per_part = len(df) // num_parts

# Diviser le dataframe en 10 parties
for i in range(num_parts):
    start = i * rows_per_part
    end = (i + 1) * rows_per_part if i < num_parts - 1 else len(df)
    df_part = df.iloc[start:end]
    df_part.to_csv(f'part_{i + 1}.csv', index=False)
