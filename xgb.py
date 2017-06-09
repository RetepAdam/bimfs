import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBRegressor

if __name__ == "__main__":
    df_nba = pd.read_csv('data/rookies_from_cbb.csv')
    df_cbb = pd.read_csv('data/cbb_to_rookies.csv')

    df_cbb['Age'] = df_nba['Age']

    df_nba = df_nba[df_nba['MP'] >= 100]
    df_cbb = df_cbb[df_cbb['Player'].isin(df_nba['Player'])]

    X = np.array(df_cbb[df_cbb.columns[2:]])
    cols = df_nba.columns[25:]
    for col in cols:
        print(col)
        y = np.array(df_nba[col])
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=21)

        model = XGBRegressor(n_estimators=1000)
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        print(score)
