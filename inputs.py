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

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(range(len(df_comp)), probabilities[21])
ax.set_xlabel('Index')
ax.set_ylabel('Probability of replicating {0}'.format(df_inputs.columns[23]))
plt.show()
