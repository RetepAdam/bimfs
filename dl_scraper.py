import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def scrape_totals_single_year(year):
    url = "http://www.basketball-reference.com/dleague/years/dleague_{0}_totals.html".format(year)
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
        if table[i][0] == 'Player':
            dropsies.append(i)

    dropsies.sort(reverse=True)

    for i in dropsies:
        table.pop(i)

    team = ['ARK', 'FAY', 'FLO', 'CHS', 'NCH', 'FTW', 'GRE', 'MOB', 'ROA', 'UTA', 'AUS', 'CLB', 'NAS', 'BAK', 'CAN', 'NMX', 'ABQ', 'HUN', 'DEL', 'ERI', 'FOR', 'SLS', 'IDA', 'IOW', 'LOS', 'MAI', 'REN', 'RIO', 'SAN', 'DAK', 'SFL', 'GRR', 'SPR', 'ANA', 'TEX', 'COL', 'OKL', 'TUL', 'ASH', 'WES', 'WCB', 'SWR', 'LIN', 'RAP', 'TOT']

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] in team:
                stop = j
        table[i][0:stop] = [' '.join(table[i][0:stop])]

    #FT% fix
    for i in range(len(table)):
        if '.' not in table[i][-10]:
            table[i].insert(-9, '.000')

    #eFG% fix
    for i in range(len(table)):
        if '.' not in table[i][-13] or '.' not in table[i][-14]:
            table[i].insert(-12, '.000')

    #2P% fix
    for i in range(len(table)):
        if '.' not in table[i][-14]:
            table[i].insert(-13, '.000')

    #3P% fix
    for i in range(len(table)):
        if '.' not in table[i][-17]:
            table[i].insert(-16, '.000')

    #FG% fix
    for i in range(len(table)):
        if '.' not in table[i][-20]:
            table[i].insert(-19, '.000')

    #age fix
    for i in range(len(table)):
        if len(table[i]) == 27:
            table[i].insert(2, 'NaN')

    df = pd.DataFrame(table, columns=cols)
    df['Yr'] = year
    df['Player'] = df['Player'].str.strip(' *')
    print(year)
    return df

def scrape_totals():
    print('Totals:')
    df = scrape_totals_single_year(2017)
    years = range(2002,2017)
    years.sort(reverse=True)
    for year in years:
        df2 = scrape_totals_single_year(year)
        df = df.append(df2, ignore_index=True)
    df.to_csv('data/player_NBADL_totals.csv', index=False)

def scrape_per_36_single_year(year):
    url = "http://www.basketball-reference.com/dleague/years/dleague_{0}_per_minute.html".format(year)
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
        if table[i][0] == 'Player':
            dropsies.append(i)

    dropsies.sort(reverse=True)

    for i in dropsies:
        table.pop(i)

    team = ['ARK', 'FAY', 'FLO', 'CHS', 'NCH', 'FTW', 'GRE', 'MOB', 'ROA', 'UTA', 'AUS', 'CLB', 'NAS', 'BAK', 'CAN', 'NMX', 'ABQ', 'HUN', 'DEL', 'ERI', 'FOR', 'SLS', 'IDA', 'IOW', 'LOS', 'MAI', 'REN', 'RIO', 'SAN', 'DAK', 'SFL', 'GRR', 'SPR', 'ANA', 'TEX', 'COL', 'OKL', 'TUL', 'ASH', 'WES', 'WCB', 'SWR', 'LIN', 'RAP', 'TOT']

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] in team:
                stop = j
        table[i][0:stop] = [' '.join(table[i][0:stop])]

    #empty table fix
    for i in range(len(table)):
        if len(table[i]) == 6:
            table[i].extend(['0', '0', '.000', '0', '0', '.000', '0', '0' ,'.000', '0', '0', '.000', '0', '0', '0', '0', '0', '0', '0', '0', '0'])

    #FT% fix
    for i in range(len(table)):
        if '.' not in table[i][-10]:
            table[i].insert(-9, '.000')

    #2P% fix
    for i in range(len(table)):
        if '.' not in table[i][-13]:
            table[i].insert(-12, '.000')

    #3P% fix
    for i in range(len(table)):
        if '.' not in table[i][-16]:
            table[i].insert(-15, '.000')

    #FG% fix
    for i in range(len(table)):
        if '.' not in table[i][-19]:
            table[i].insert(-18, '.000')

    #age fix
    for i in range(len(table)):
        if len(table[i]) == 26:
            table[i].insert(2, 'NaN')

    df = pd.DataFrame(table, columns=cols)
    df['Yr'] = year
    df['Player'] = df['Player'].str.strip(' *')
    print(year)
    return df

def scrape_per_36():
    print('Per 36:')
    df = scrape_per_36_single_year(2017)
    years = range(2002,2017)
    years.sort(reverse=True)
    for year in years:
        df2 = scrape_per_36_single_year(year)
        df = df.append(df2, ignore_index=True)
    df.to_csv('data/player_NBADL_per_36.csv', index=False)

def clean_up_names(stat_type):
    df = pd.read_csv('data/player_{0}.csv'.format(stat_type))
    df['Player'] = df['Player'].str.split(' ')

    # a few players have two first names, so we need to address them separately
    # James Michael McAdoo = 1231
    # Peter John Ramos = 4325, 4522
    # Bobby Ray Parks Jr. = 814
    # E. Victor Nickerson = 324

    group = [324, 814, 1231, 4325, 4522]

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

    df['Player'][451] = 'F. VanVleet' # VanVleet typo fix

    df.to_csv('data/player_{0}.csv'.format(stat_type), index=False)

if __name__ == '__main__':
    scrape_totals()
    clean_up_names('NBADL_totals')
    scrape_per_36()
    clean_up_names('NBADL_per_36')
