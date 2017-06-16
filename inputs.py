import pandas as pd
import numpy as np

df_inputs = pd.read_csv('data/nba_inputs.csv')

selected = raw_input('Enter a player name: ')
stats = np.array(df_inputs[df_inputs['Player'] == selected])[0][2:]
