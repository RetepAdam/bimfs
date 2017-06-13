import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

df_nba = pd.read_csv('data/rookies_from_cbb.csv')
df_cbb = pd.read_csv('data/cbb_to_rookies.csv')

df_cbb['Age'] = df_nba['Age']

df_nba = df_nba[df_nba['MP'] >= 100]
df_cbb = df_cbb[df_cbb['Player'].isin(df_nba['Player'])]

X = np.array(df_cbb[df_cbb.columns[2:]])
X = np.array(df_cbb[df_cbb.columns[[1, 6, 8, 12, 13, 15, 16, 17, 19, 29, 30, 31, 36, 38, 39, 40, 41, 43, 44, 47, 50, 54, 60, 61]]])
cols = df_nba.columns[42:44]
for col in cols:
    print(col)
    y = np.array(df_nba[col])

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=21)

    rf = RandomForestRegressor(random_state=66, max_depth=5)
    rf.fit(X_train, y_train)
    regr = LinearRegression()
    regr.fit(X_train, y_train)
    model_X = sm.add_constant(X)
    model = sm.OLS(y, model_X)
    results = model.fit()
    print('RF: {0}'.format(rf.score(X_test, y_test)))
    print('Linear: {0}'.format(regr.score(X_test, y_test)))
    print('OLS R2: {0}'.format(results.rsquared_adj))
    print('')
