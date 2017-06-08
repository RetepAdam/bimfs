import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm

df_nba = pd.read_csv('data/rookies_from_cbb.csv')
df_cbb = pd.read_csv('data/cbb_to_rookies.csv')

X = np.array(df_cbb[df_cbb.columns[2:]])
cols = df_nba.columns[25:]
for col in cols:
    y = np.array(df_nba[col])

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=21)

    rf = RandomForestRegressor(random_state=66, max_depth=5)
    rf.fit(X_train, y_train)
    print(col, rf.score(X_test, y_test))

# model_X = sm.add_constant(X)
# model = sm.OLS(y, model_X)
# results = model.fit()
# print(results.summary())
