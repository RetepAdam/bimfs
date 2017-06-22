import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBRegressor

if __name__ == "__main__":
    df_nba = pd.read_csv('data/rookies_from_cbb2.csv')
    df_cbb = pd.read_csv('data/cbb_to_rookies2.csv')

    df_nba = df_nba[df_nba['MP'] >= 500]
    df_cbb = df_cbb[df_cbb['Player'].isin(df_nba['Player'])]

    X = np.array(df_cbb[df_cbb.columns[1:]])
    y = np.array(df_nba[df_nba.columns[49]])
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=21)
    test = []
    for j in np.arange(1, 101, 1):
        for i in np.arange(0.01, 1, 0.01):
            model = XGBRegressor(base_score=0.46229346552682926, learning_rate=i, n_estimators=j)
            model.fit(X_train, y_train)
            score = model.score(X_test, y_test)
            test.append(score)
            print(j, i)
