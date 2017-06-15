import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBRegressor

if __name__ == "__main__":
    df_nba = pd.read_csv('data/rookies_from_cbb2.csv')
    df_cbb = pd.read_csv('data/cbb_to_rookies2.csv')

    df_cbb['Age'] = df_nba['Age']

    df_nba = df_nba[df_nba['MP'] >= 500]
    df_cbb = df_cbb[df_cbb['Player'].isin(df_nba['Player'])]

    X = np.array(df_cbb[df_cbb.columns[1:]])
    y = np.array(df_nba['3P%'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=21)
    # for i in np.arange(0.01, 1, 0.01):
    model = XGBRegressor(base_score=0.25738192342996741, learning_rate=.06, n_estimators=59)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(score)
