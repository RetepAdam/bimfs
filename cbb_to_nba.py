import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import forestci as fci
import pickle
from xgboost import XGBRegressor

df_nba = pd.read_csv('data/rookies_from_cbb2.csv')
df_cbb = pd.read_csv('data/cbb_to_rookies2.csv')
df_comp = pd.read_csv('data/cbb_comp_list.csv')

# df_cbb['Age'] = df_nba['Age'] # can't grab age for new class yet

df_nba = df_nba[df_nba['MP'] >= 500]
df_cbb = df_cbb[df_cbb['Player'].isin(df_nba['Player'])]

df_comp = df_comp[df_comp['MP'] >= 500]
df_comp = df_comp[df_comp['To'] == 2017]
df_comp.reset_index(drop=True, inplace=True)
nba_X_comp = np.array(df_comp[df_comp.columns[5:]])

X = np.array(df_cbb[df_cbb.columns[1:]])
cols = df_nba.columns[25:]

# fig, axes = plt.subplots(1,3, figsize=(12,4))

# for col, ax in zip(cols, axes.flatten()):
for i in range(len(cols)):
    col = cols[i]
    y = np.array(df_nba[col])

    nba_X_train, nba_X_test, nba_y_train, nba_y_test = train_test_split(X, y, random_state=21)

    # for i in range(1,20):
    with open('models/nba_forest_{0}.pickle'.format(col), "rb") as input_file:
        nba_forest = pickle.load(input_file)
    # nba_forest = RandomForestRegressor(n_estimators=1000, random_state=66)
    # nba_forest.fit(nba_X_train, nba_y_train)
    # print('RF: {0}'.format(nba_forest.score(nba_X_test, nba_y_test)))
    # with open('models/nba_forest_{0}.pickle'.format(str.lower(col)), 'wb') as handle:
    #         pickle.dump(nba_forest, handle, protocol=pickle.HIGHEST_PROTOCOL)

    nba_y_hat = nba_forest.predict(nba_X_comp)

    nba_inbag = fci.calc_inbag(nba_X_train.shape[0], nba_forest)
    nba_V_IJ_unbiased = fci.random_forest_error(nba_forest, nba_X_train,
                                                nba_X_comp)

    nba_yerr = np.sqrt(nba_V_IJ_unbiased)

    np.save('numpy/2017_{0}_preds.npy'.format(i), nba_y_hat)
    np.save('numpy/2017_{0}_yerr.npy'.format(i), nba_yerr)
    print(col)
    # i += 1

# # Plot error bars for predicted MPG using unbiased variance
# plt.errorbar(np.arange(len(nba_y_hat)), nba_y_hat, yerr=np.sqrt(nba_V_IJ_unbiased), fmt='o')
# plt.xlabel('Actual 3P%')
# plt.ylabel('Predicted 3P%')
#
# plt.show()
