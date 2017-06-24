# this one's gonna be kind of messy unless I decide to double back to clean it up.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def scrape_initial_page():
    url = "http://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=totals&per_minute_base=36&per_poss_base=100&lg_id=NBA&is_playoffs=N&year_min=2001&year_max=&franch_id=&season_start=1&season_end=1&age_min=0&age_max=99&shoot_hand=&height_min=0&height_max=99&birth_country_is=Y&birth_country=&birth_state=&college_id=&draft_year=&is_active=&debut_yr_aba_start=&debut_yr_aba_end=&debut_yr_nba_start=&debut_yr_nba_end=&is_hof=&is_as=&as_comp=gt&as_val=&award=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&c5stat=&c5comp=&c6mult=1.0&c6stat=&order_by=season&order_by_asc=Y&offset=0"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stuff = soup.select('tr')

    table = []

    for i in range(len(stuff)):
        table.append(stuff[i].get_text(' ').split())

    return table

def scrape_other_pages(table, page):
    url = "http://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=totals&per_minute_base=36&per_poss_base=100&lg_id=NBA&is_playoffs=N&year_min=2001&year_max=&franch_id=&season_start=1&season_end=1&age_min=0&age_max=99&shoot_hand=&height_min=0&height_max=99&birth_country_is=Y&birth_country=&birth_state=&college_id=&draft_year=&is_active=&debut_yr_aba_start=&debut_yr_aba_end=&debut_yr_nba_start=&debut_yr_nba_end=&is_hof=&is_as=&as_comp=gt&as_val=&award=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&c5stat=&c5comp=&c6mult=1.0&c6stat=&order_by=season&order_by_asc=Y&offset={0}".format(page)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stuff = soup.select('tr')

    for i in range(len(stuff)):
        table.append(stuff[i].get_text(' ').split())

    return table


if __name__ == '__main__':
    table = scrape_initial_page()
    for i in range(0,1300,100):
        print(i)
        table = scrape_other_pages(table, i)

    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = table[i][j].encode('ascii', 'ignore')

    table.pop(0)
    cols = table[0]
    table.pop(0)

    dropsies = []

    for i in range(len(table)):
        if table[i][0] == 'Rk':
            dropsies.append(i)
        if table[i][0] == 'Totals':
            dropsies.append(i)

    dropsies.sort(reverse=True)

    for i in dropsies:
        table.pop(i)

    for i in range(len(table)):
        table[i].pop(0)

    teams = ['ATL', 'BOS', 'BRK', 'CHI', 'CHA', 'CHH', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NJN', 'NOH', 'NOK', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'SEA', 'TOR', 'TOT', 'UTA', 'VAN', 'WAS']

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] in teams:
                stop = j-1
        table[i][0:stop] = [' '.join(table[i][0:stop])]

    new_table = []

    for i in range(len(table)):
        if len(table[i]) == 25:
            new_table.append(table[i])
        elif len(table[i]) > 25:
            new_table.append(table[i][:25])

    cols.pop(0)
    cols = cols[:25]

    df = pd.DataFrame(new_table, columns=cols)
    df['Player'] = df['Player'].str.strip(' *')

    df.to_csv('../src/data/rookies.csv', index=False)
