import pandas as pd
import numpy as np

def drop_mp_nulls(df):
    converts = df['MP'].values
    converts = list(converts)

    for i in range(len(converts)):
        converts[i] = float(converts[i])

    df['MP'] = converts

    df = df[~df['MP'].isnull()]
    df.reset_index(drop=True, inplace=True)
    return df

def create_transfer_check_df(df):
    df_abbrev = df[['Player', 'School', 'Yr']]
    df_grouped = df_abbrev.groupby(['Player', 'School']).max()
    df_grouped.reset_index(inplace=True)
    # 21010 duplicate player names
    # when grouping by player name and school, 2296 duplicate player names
    # need to determine which of these are transfers and which are distinct players
    dupes = np.where(df_grouped['Player'].duplicated())[0]
    orig = dupes - 1
    orig = list(orig)
    dupes = list(dupes)
    dupes.extend(orig)
    dupes = set(dupes) # remove duplicates
    dupes = list(dupes)
    dupes = np.array(dupes)
    df_transfer_check = df_grouped.iloc[np.sort(dupes)]
    df_transfer_check.reset_index(drop=True, inplace=True)
    return df_transfer_check

if __name__ == '__main__':
    df = pd.read_csv('data/cbb_2001_to_2017.csv')
    df = drop_mp_nulls(df)
    df_transfer_check = create_transfer_check_df(df)
