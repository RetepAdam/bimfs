import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import sklearn.cross_validation as xval
import forestci as fci
from xgboost import XGBRegressor

df_nba = pd.read_csv('data/rookies_from_cbb2.csv')
df_cbb = pd.read_csv('data/cbb_to_rookies2.csv')

df_cbb['Age'] = df_nba['Age']

df_nba = df_nba[df_nba['MP'] >= 500]
df_cbb = df_cbb[df_cbb['Player'].isin(df_nba['Player'])]

X = np.array(df_cbb[df_cbb.columns[1:]])
cols = df_nba.columns[38:41]

fig, axes = plt.subplots(1,3, figsize=(12,4))

for col, ax in zip(cols, axes.flatten()):
    print(col)
    y = np.array(df_nba[col])

    nba_X_train, nba_X_test, nba_y_train, nba_y_test = xval.train_test_split(X, y, random_state=21)

    # for i in range(1,20):
    n_trees = 2000
    nba_forest = RandomForestRegressor(n_estimators=n_trees, random_state=66)
    nba_forest.fit(nba_X_train, nba_y_train)
    nba_y_hat = nba_forest.predict(nba_X_test)
    # regr = LinearRegression()
    # regr.fit(X_train, y_train)
    # model_X = sm.add_constant(X)
    # model = sm.OLS(y, model_X)
    # results = model.fit()
    print('RF: {0}'.format(nba_forest.score(nba_X_test, nba_y_test)))
    # print('Linear: {0}'.format(regr.score(X_test, y_test)))
    # print('OLS R2: {0}'.format(results.rsquared_adj))
    print('')

    nba_inbag = fci.calc_inbag(nba_X_train.shape[0], nba_forest)
    nba_V_IJ_unbiased = fci.random_forest_error(nba_forest, nba_X_train,
                                                nba_X_test)

    # Plot error bars for predicted MPG using unbiased variance
    ax.errorbar(nba_y_test, nba_y_hat, yerr=np.sqrt(nba_V_IJ_unbiased), fmt='o')
    ax.set_xlabel('Actual %s' % col)
    ax.set_ylabel('Predicted %s' % col)

plt.tight_layout()
plt.show()
