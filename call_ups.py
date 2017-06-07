import pandas as pd
import numpy as np

df = pd.read_csv('data/player_totals.csv')
df2 = pd.read_csv('data/player_NBADL_totals.csv')

df_callups = df[df['Player'].isin(df2['Player'])]
