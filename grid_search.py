print(__doc__)

import numpy as np

from time import time
from scipy.stats import randint as sp_randint

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df_nba = pd.read_csv('data/rookies_from_cbb2.csv')
df_cbb = pd.read_csv('data/cbb_to_rookies2.csv')
df_comp = pd.read_csv('data/cbb_comp_list.csv')

df_nba = df_nba[df_nba['MP'] >= 500]
df_cbb = df_cbb[df_cbb['Player'].isin(df_nba['Player'])]

df_comp = df_comp[df_comp['MP'] >= 500]
df_comp = df_comp[df_comp['To'] == 2017]
df_comp.reset_index(drop=True, inplace=True)
nba_X_comp = np.array(df_comp[df_comp.columns[5:]])

X = np.array(df_cbb[df_cbb.columns[1:]])
y = np.array(df_nba['3P_PCT'])
# build a classifier
nba_forest = RandomForestRegressor(n_estimators=1000, random_state=66)

# nba_X_train, nba_X_test, nba_y_train, nba_y_test = train_test_split(X, y, random_state=21)


# Utility function to report best scores
def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")


# specify parameters and distributions to sample from
param_dist = {"max_depth": [3, None],
              "max_features": sp_randint(1, 11),
              "min_samples_leaf": sp_randint(1, 11),
              "bootstrap": [True, False]}

# run randomized search
n_iter_search = 20
random_search = RandomizedSearchCV(nba_forest, param_distributions=param_dist,
                                   n_iter=n_iter_search)

start = time()
random_search.fit(X, y)
print("RandomizedSearchCV took %.2f seconds for %d candidates"
      " parameter settings." % ((time() - start), n_iter_search))
report(random_search.cv_results_)

# use a full grid over all parameters
param_grid = {"max_depth": [3, None],
              "max_features": [1, 3, 10],
              "min_samples_leaf": [1, 3, 10],
              "bootstrap": [True, False]}

# run grid search
grid_search = GridSearchCV(nba_forest, param_grid=param_grid)
start = time()
grid_search.fit(X, y)

print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
      % (time() - start, len(grid_search.cv_results_['params'])))
report(grid_search.cv_results_)
