import pandas as pd
import numpy as np
import scipy.stats as scs
import matplotlib.pyplot as plt

df_inputs = pd.read_csv('data/nba_inputs.csv')
df_comp = pd.read_csv('data/cbb_comp_list.csv')

df_comp = df_comp[df_comp['MP'] >= 500]
df_comp.reset_index(drop=True, inplace=True)

selected = raw_input('Enter a player name: ')
stats = np.array(df_inputs[df_inputs['Player'] == selected])[0][2:]

probabilities = []

for i in range(len(stats)):
    comp_pred = np.load('numpy/{0}_preds.npy'.format(i))
    comp_err = np.load('numpy/{0}_yerr.npy'.format(i))
    comp_proba = scs.norm.cdf((comp_pred - stats[i]) / (.5 * comp_err))
    probabilities.append(comp_proba)

for i in range(len(probabilities)):
    for j in range(len(probabilities[i])):
        probabilities[i][j] = round(probabilities[i][j], 3)

labels = pd.DataFrame(np.array(df_comp['Player'].values), columns=['Player'])
proba = pd.DataFrame(np.array(probabilities).T, columns=df_inputs.columns[2:])
proba = proba.fillna(0)
df_output = labels.merge(proba, left_index=True, right_index=True)
print(df_output.head())

fig, axes = plt.subplots(5,5, figsize=(25,25))

months = range(proba.shape[1])

for i, ax in zip(months, axes.flatten()):
    y = proba[proba.columns[i]].values

    ax.scatter(range(len(labels)), y)

    ax.set_xlabel('Player Index')
    ax.set_ylabel('{0}'.format(proba.columns[i]))

plt.tight_layout()
plt.savefig('Will_Barton_all.png', dpi=600)
