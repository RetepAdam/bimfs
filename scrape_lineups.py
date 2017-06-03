import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time


year = 2017

def scrape_lineups_single_page(year, page):
    url = "http://www.basketball-reference.com/play-index/lineup_finder.cgi?request=1&match=single&player_id=&lineup_type=5-man&output=total&year_id={0}&is_playoffs=N&team_id=&opp_id=&game_num_min=0&game_num_max=99&game_month=&game_location=&game_result=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=mp&order_by_asc=&offset={1}".format(year, page)

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stuff = soup.select('tr')

    table = []

    for i in range(len(stuff)):
        table.append(stuff[i].get_text(' ').split())

    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = table[i][j].encode('ascii', 'ignore')

    if table:
        table.pop(0)
        cols = table[0]
        table.pop(0)

        dropsies = []

        for i in range(len(table)):
            if table[i][0] == 'Rk':
                dropsies.append(i)
            elif table[i][0] == 'Poss':
                dropsies.append(i)

        dropsies.sort(reverse=True)

        for i in dropsies:
            table.pop(i)

        for i in range(len(table)):
            table[i].pop(0)

        teams = ['ATL', 'BOS', 'BRK', 'CHI', 'CHA', 'CHH', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NJN', 'NOH', 'NOK', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'SEA', 'TOR', 'UTA', 'VAN', 'WAS']

        for i in range(len(table)):
            for j in range(len(table[i])):
                if table[i][j] in teams:
                    stop = j
            table[i][0:stop] = [' '.join(table[i][0:stop])]

        # pace fix
        for i in range(len(table)):
            if len(table[i]) == 14:
                table[i].insert(7, 'NaN')

        # just free throw missing
        for i in range(len(table)):
            if len(table[i][-2]) < 4:
                table[i].insert(-1, '.000')
            elif table[i][-2][0] != '+' and table[i][-2][0] != '-' and table[i][-2][0] != '.':
                table[i].insert(-1, '.000')

        # shooting fixes for all missing
        for i in range(len(table)):
            if len(table[i]) == 16:
                table[i].insert(12, '.000')
                table[i].insert(12, '.000')
                table[i].insert(10, '.000')

        # just 3P% missing
        for i in range(len(table)):
            if len(table[i]) == 18:
                table[i].insert(-5, '.000')

        cols.pop(0)

        df = pd.DataFrame(table, columns=cols)
        df['Lineup'] = df['Lineup'].str.strip(' *')
        print(page)
        return df
    elif not table:
        df = pd.DataFrame(table)
        print(page)
        return df

def scrape_lineups_full_year(year):
    pages = np.arange(100,20000,100)
    df = scrape_lineups_single_page(year,0)
    for page in pages:
        time.sleep(np.random.randint(0,2) + np.random.rand()) # let's give it a random, quick break
        df2 = scrape_lineups_single_page(year, page)
        if df2.shape[0] == 0:
            print(year)
            return df
        else:
            df = df.append(df2, ignore_index=True)
    print(year)
    return df

def scrape_lineups_all_years():
    print('Lineups:')
    df = scrape_lineups_full_year(2017)
    years = range(2001,2017)
    years.sort(reverse=True)
    for year in years:
        time.sleep(np.random.randint(0,120) + np.random.rand())
        df2 = scrape_lineups_full_year(year)
        df = df.append(df2, ignore_index=True)
    df.to_csv('data/all_lineups.csv', index=False)

if __name__ == '__main__':
    scrape_lineups_all_years()
