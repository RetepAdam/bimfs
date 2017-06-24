import pandas as pd
import numpy as np
import scipy.stats as scs
import matplotlib.pyplot as plt

def hooplicate():
    df_inputs = pd.read_csv("data/nba_inputs.csv") # import nba players to be hooplicated
    df_comp = pd.read_csv("data/cbb_comp_list.csv") # import database of non-NBA players

    df_comp = df_comp[df_comp["MP"] >= 500] # minutes restriction, also mirrored in the numpy array imports
    df_comp.reset_index(drop=True, inplace=True)

    selected = str(raw_input("Select a player: ")) # take user inputs; use drop-down on web app
    stats = np.array(df_inputs[df_inputs['Player'] == selected])[0][2:] # grab relevant model statistics

    probabilities = []

    for i in range(len(stats)):
        comp_pred = np.load("numpy/{0}_preds.npy".format(i)) # import projections for comp player per stat
        comp_err = np.load("numpy/{0}_yerr.npy".format(i)) # import error bars for comp player per stat
        comp_err = np.nan_to_num(comp_err) # zero out NaN values; haven't quite figured out why some error bars run negative
        if i in [19, 20]: # statistics where higher is worse
            comp_proba = 1 - scs.norm.cdf((comp_pred - stats[i]) / (.5 * comp_err)) # flip formula so it's probability of X or lower
        else:
            comp_proba = scs.norm.cdf((comp_pred - stats[i]) / (.5 * comp_err)) # probability of matching or exceeding NBA player's numbers
        probabilities.append(comp_proba)

    for i in range(len(probabilities)):
        for j in range(len(probabilities[i])):
            probabilities[i][j] = round(probabilities[i][j], 3) # round off probabilities

    labels = pd.DataFrame(np.array(df_comp["Player"].values), columns=["Player"]) # player names for comp list
    proba = pd.DataFrame(np.array(probabilities).T, columns=df_inputs.columns[2:]) # match probabilities to statistic name
    proba = proba.fillna(0) # make sure there are no NaN values
    df_output = labels.merge(proba, left_index=True, right_index=True) # combine the two dataframes
    sums = []
    for i in range(len(df_output)):
        sums.append(sum(df_output.iloc[i][1:])) # as an initial method of sorting, take cumulative probabilities for each player across all stats

    df_output["Sum"] = sums
    df_output.sort_values("Sum", ascending=False, inplace=True)
    df_output.reset_index(drop=True, inplace=True)
    df_output.drop("Sum", axis=1, inplace=True) # sort based on "Sum" column then drop it
    return df_output

if __name__ == '__main__':
    df = hooplicate()
