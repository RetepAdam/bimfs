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

def dump_index

if __name__ == '__main__':
    scrape_totals()
    scrape_advanced()