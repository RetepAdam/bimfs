import pandas as pd
import numpy as np

def get_2017():
    df_2017 = df[df['Yr'] == 2017]
    df_2017 = df_2017[df_2017['3PA'] >= 50]
    group = np.where(df_2017['Player'].duplicated())
    group = group[0]
    df_2017.reset_index(inplace=True)
    df_2017.drop('index', axis=1, inplace=True)
    df_2017.drop(group, inplace=True)

    df2_2017 = df2[df2['Yr'] == 2017]
    df2_2017 = df2_2017[df2_2017['3PA'] >= 50]
    group = np.where(df2_2017['Player'].duplicated())
    group = group[0]
    df2_2017.reset_index(inplace=True)
    df2_2017.drop('index', axis=1, inplace=True)
    df2_2017.drop(group, inplace=True)

    df_2017 = df_2017[df_2017['Player'].isin(df2_2017['Player'])]
    df2_2017 = df2_2017[df2_2017['Player'].isin(df_2017['Player'])]
    return df_2017, df2_2017

def get_year(year_in_question):
    df_year = df[df['Yr'] == year_in_question]
    df_year = df_year[df_year['3PA'] >= 50]
    group = np.where(df_year['Player'].duplicated())
    group = group[0]
    df_year.reset_index(inplace=True)
    df_year.drop('index', axis=1, inplace=True)
    df_year.drop(group, inplace=True)

    df2_year = df2[df2['Yr'] == year_in_question]
    df2_year = df2_year[df2_year['3PA'] >= 50]
    group = np.where(df2_year['Player'].duplicated())
    group = group[0]
    df2_year.reset_index(inplace=True)
    df2_year.drop('index', axis=1, inplace=True)
    df2_year.drop(group, inplace=True)

    df_year = df_year[df_year['Player'].isin(df2_year['Player'])]
    df2_year = df2_year[df2_year['Player'].isin(df_year['Player'])]
    return df_year, df2_year

if __name__ == '__main__':
    df = pd.read_csv('data/player_totals.csv')
    df2 = pd.read_csv('data/player_NBADL_totals.csv')
    df_nba, df_dl = get_2017()
    years = range(2001, 2017)
    years.sort(reverse=True)
    for year in years:
        new_nba, new_dl = get_year(year)
        df_nba = df_nba.append(new_nba, ignore_index=True)
        df_dl = df_dl.append(new_dl, ignore_index=True)
        print(year)
