import pandas as pd
import numpy as np
import scipy.stats as scs
import matplotlib.pyplot as plt

df_inputs = pd.read_csv("data/nba_inputs.csv")
df_comp = pd.read_csv("data/cbb_comp_list.csv")

df_comp = df_comp[df_comp["MP"] >= 500]
df_comp = df_comp[df_comp['To'] == 2017]
df_comp.reset_index(drop=True, inplace=True)

selected = "NBA Average"
stats = np.array([0.0, 0.2, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.2, 1.5, 3.3])

probabilities = []

for i in range(len(stats)):
    comp_pred = np.load("numpy/18_preds.npy")
    comp_err = np.load("numpy/18_yerr.npy")
    comp_err = np.nan_to_num(comp_err)
    comp_proba = scs.norm.cdf((comp_pred - stats[i]) / (.5 * comp_err))
    probabilities.append(comp_proba)

for i in range(len(probabilities)):
    for j in range(len(probabilities[i])):
        probabilities[i][j] = round(probabilities[i][j], 3)

# labels = pd.DataFrame(np.array(df_comp["Player"].values), columns=["Player"])
# proba = pd.DataFrame(np.array(probabilities).T, columns=df_inputs.columns[[4,15,16,17,18,19,20,25,26]])
# proba = proba.fillna(0)
# df_output = labels.merge(proba, left_index=True, right_index=True)
# sums = []
# for i in range(len(df_output)):
#     sums.append(sum(df_output.iloc[i][1:]))
#
# df_output["Sum"] = sums
# df_output.sort_values("Sum", ascending=False, inplace=True)
# df_output.reset_index(drop=True, inplace=True)
# df_output.drop("Sum", axis=1, inplace=True)
#
    with plt.style.context('seaborn-muted'):
        fig, axes = plt.subplots(2,6, figsize=(30,10))

        months = range(len(probabilities))

        for i, ax in zip(months, axes.flatten()):
            y = probabilities[i]

            ax.violinplot(y)

            ax.set_ylim(-.01,1.01)
            ax.set_ylabel("Probability of {0}th Percentile BLK/36 {1} Better".format(i*10, 'or', fontsize=16))

        plt.tight_layout()
        plt.savefig("save_the_graphs/blk_per_36_by_percentile.png".format(selected), dpi=600)
        plt.close()
