import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def scrape_totals_single_year(year):
    url = "http://www.basketball-reference.com/leagues/NBA_{0}_totals.html".format(year)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stuff = soup.select('tr')

    table = []

    for i in range(len(stuff)):
        table.append(stuff[i].get_text(' ').split())

    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = table[i][j].encode('ascii', 'ignore')

    cols = table[0]
    table.pop(0)

    dropsies = []

    for i in range(len(table)):
        if table[i][0] == 'Rk':
            dropsies.append(i)

    dropsies.sort(reverse=True)

    for i in dropsies:
        table.pop(i)

    for i in range(len(table)):
        table[i].pop(0)

    positions = ['PG', 'SG', 'SF', 'PF', 'C', 'PG-SG', 'SG-SF', 'SF-PF', 'PF-C', 'SG-PG', 'SF-SG', 'PF-SF', 'C-PF', 'G', 'F', 'G-F', 'F-G', 'F-C', 'C-F']

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] in positions:
                stop = j
        table[i][0:stop] = [' '.join(table[i][0:stop])]

    #FT% fix
    for i in range(len(table)):
        if table[i][-10] == '0':
            table[i].insert(-9, '.000')

    #eFG% fix
    for i in range(len(table)):
        if len(table[i][-14]) < 4:
            table[i].insert(-12, '.000')
        elif table[i][-14][0] != '.' and table[i][-14][1] != '.':
            table[i].insert(-12, '.000')

    #2P% fix
    for i in range(len(table)):
        if table[i][-14] == '0':
            table[i].insert(-13, '.000')

    #3P% fix
    for i in range(len(table)):
        if table[i][-17] == '0':
            table[i].insert(-16, '.000')

    #FG% fix
    for i in range(len(table)):
        if table[i][-20] == '0':
            table[i].insert(-19, '.000')

    #GS fix
    for i in range(len(table)):
        if len(table[i]) < 29:
            table[i].insert(6, 'NaN')

    cols.pop(0)

    df = pd.DataFrame(table, columns=cols)
    df['Yr'] = year
    df['Player'] = df['Player'].str.strip(' *')
    print(year)
    return df

def scrape_totals():
    print('Totals:')
    df = scrape_totals_single_year(2017)
    years = range(1980,2017)
    years.sort(reverse=True)
    for year in years:
        df2 = scrape_totals_single_year(year)
        df = df.append(df2, ignore_index=True)
    df.to_csv('data/player_totals.csv', index=False)

def scrape_advanced_single_year(year):
    url = "http://www.basketball-reference.com/leagues/NBA_{0}_advanced.html".format(year)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stuff = soup.select('tr')

    table = []

    for i in range(len(stuff)):
        table.append(stuff[i].get_text(' ').split())

    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = table[i][j].encode('ascii', 'ignore')

    cols = table[0]
    table.pop(0)

    dropsies = []

    for i in range(len(table)):
        if table[i][0] == 'Rk':
            dropsies.append(i)

    dropsies.sort(reverse=True)

    for i in dropsies:
        table.pop(i)

    for i in range(len(table)):
        table[i].pop(0)

    positions = ['PG', 'SG', 'SF', 'PF', 'C', 'PG-SG', 'SG-SF', 'SF-PF', 'PF-C', 'SG-PG', 'SF-SG', 'PF-SF', 'C-PF', 'G', 'F', 'G-F', 'F-G', 'F-C', 'C-F']

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] in positions:
                stop = j
        table[i][0:stop] = [' '.join(table[i][0:stop])]

    if year > 1977:
        for i in range(len(table)):
            if len(table[i]) == 22: # fix for 1980-2017 (and a few between 1978 and 1980)
                table[i].insert(13, 'NaN')
                table[i].insert(7, 'NaN')
                table[i].insert(7, 'NaN')
                table[i].insert(7, 'NaN')
            if len(table[i]) == 23: # fix for 1978-2017
                table[i].insert(7, 'NaN')
                table[i].insert(7, 'NaN')
                table[i].insert(7, 'NaN')
            if len(table[i]) == 25: # fix for 1978-1979 general
                table[i].insert(8, 'NaN')
    if year <= 1977:
        for i in range(len(table)):
            if len(table[i]) == 23: # fix for 1974-1977
                table[i].insert(15, 'NaN')
                table[i].insert(15, 'NaN')
                table[i].insert(8, 'NaN')
            if len(table[i]) == 21: # fix for 1974-1977
                table[i].insert(15, 'NaN')
                table[i].insert(15, 'NaN')
                table[i].insert(7, 'NaN')
                table[i].insert(7, 'NaN')
                table[i].insert(7, 'NaN')

    cols.pop(0)

    df = pd.DataFrame(table, columns=cols)
    df['Yr'] = year
    df['Player'] = df['Player'].str.strip(' *')
    print(year)
    return df

def scrape_advanced():
    print('Advanced:')
    df = scrape_advanced_single_year(2017)
    years = range(1974,2017)
    years.sort(reverse=True)
    for year in years:
        df2 = scrape_advanced_single_year(year)
        df = df.append(df2, ignore_index=True)
    df.to_csv('data/player_advanced.csv', index=False)

def scrape_per_poss_single_year(year):
    url = "http://www.basketball-reference.com/leagues/NBA_{0}_per_poss.html".format(year)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stuff = soup.select('tr')

    table = []

    for i in range(len(stuff)):
        table.append(stuff[i].get_text(' ').split())

    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = table[i][j].encode('ascii', 'ignore')

    cols = table[0]
    table.pop(0)

    dropsies = []

    for i in range(len(table)):
        if table[i][0] == 'Rk':
            dropsies.append(i)

    dropsies.sort(reverse=True)

    for i in dropsies:
        table.pop(i)

    for i in range(len(table)):
        table[i].pop(0)

    positions = ['PG', 'SG', 'SF', 'PF', 'C', 'PG-SG', 'SG-SF', 'SF-PF', 'PF-C', 'SG-PG', 'SF-SG', 'PF-SF', 'C-PF', 'G', 'F', 'G-F', 'F-G', 'F-C', 'C-F']

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] in positions:
                stop = j
        table[i][0:stop] = [' '.join(table[i][0:stop])]

    for i in range(len(table)):
        if len(table[i]) == 7: # empties
            table[i].extend(['0', '0', '.000', '0', '0', '.000', '0', '0', '.000', '0', '0', '.000', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'NaN', 'NaN'])
        if '.' in table[i][-1] and '.' in table[i][-2]: # ORtg/DRtg fix
            table[i].extend(['NaN', 'NaN'])
        elif '.' in table[i][-2]:
            table[i].insert(-1, 'NaN')
        if len(table[i]) == 26: # fix for all shooting missing
            table[i].insert(15, '.000')
            table[i].insert(13, '.000')
            table[i].insert(11, '.000')
            table[i].insert(9, '.000')
        if len(table[i]) == 27: # fix for all shooting but FT missing
            table[i].insert(13, '.000')
            table[i].insert(11, '.000')
            table[i].insert(9, '.000')
        if len(table[i]) == 28: # fix for just 3P and FT missing
            table[i].insert(17, '.000')
            table[i].insert(12, '.000')
        if len(table[i]) == 29 and table[i][12][-2] != '.': # fix for just 3P and FT missing
            table[i].insert(18, '.000')
        elif len(table[i]) == 29 and table[i][12][-2] == '.':
            table[i].insert(12, '.000')

    cols.pop(0)

    df = pd.DataFrame(table, columns=cols)
    df['Yr'] = year
    df['Player'] = df['Player'].str.strip(' *')
    print(year)
    return df

def scrape_per_poss():
    print('Per Possession:')
    df = scrape_per_poss_single_year(2017)
    years = range(2001,2017)
    years.sort(reverse=True)
    for year in years:
        df2 = scrape_per_poss_single_year(year)
        df = df.append(df2, ignore_index=True)
    df.to_csv('data/player_per_poss.csv', index=False)

# reformatting names to align with how they are in lineup data
def clean_up_names(stat_type):
    df = pd.read_csv('data/player_{0}.csv'.format(stat_type))
    df['Player'] = df['Player'].str.split(' ')

    # a few players have two first names, so we need to address them separately
    # James Michael McAdoo = 344, 943, 1544
    # Peter John Ramos = 7445
    # Juan Carlos Navarro = 5730

    group = [344, 943, 1544, 7445, 5730]

    # abbreviating first names to match lineup data
    for i in range(len(df['Player'])):
        if i in group:
            df['Player'][i][:2] = [' '.join(df['Player'][i][:2])]
        else:
            df['Player'][i][1:] = [' '.join(df['Player'][i][1:])]

    # not sure why it won't just let me do this in the dataframe column, but scenic route it is
    new_names = []

    for i in range(len(df['Player'])):
            new_names.append(df['Player'][i][0][0] + '. ' + df['Player'][i][1])

    df['Player'] = new_names

    df.to_csv('data/player_{0}.csv'.format(stat_type), index=False)

if __name__ == '__main__':
    # scrape_totals()
    # clean_up_names('totals')
    # scrape_advanced()
    # clean_up_names('advanced')
    scrape_per_poss()
    clean_up_names('per_poss')
