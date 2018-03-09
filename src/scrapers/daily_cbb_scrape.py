import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import time

def scrape_cbb_single_page(year, page):
    url = "http://www.sports-reference.com/cbb/play-index/psl_finder.cgi?request=1&match=single&year_min={0}&year_max={0}&conf_id=&school_id=&class_is_fr=Y&class_is_so=Y&class_is_jr=Y&class_is_sr=Y&pos_is_g=Y&pos_is_gf=Y&pos_is_fg=Y&pos_is_f=Y&pos_is_fc=Y&pos_is_cf=Y&pos_is_c=Y&games_type=A&qual=&c1stat=fg&c1comp=gt&c1val=0&c2stat=ts_pct&c2comp=gt&c2val=0&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=player&order_by_asc=Y&offset={1}".format(year, page)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stuff = soup.select('tr')

    table = []

    if not stuff: # backstop for when last page has already been reached
        df = pd.DataFrame(table)
        print(page)
        return df

    cats = soup.find_all('tr')[1].find_all('th') # just the categories header
    cols = []

    for i in range(len(cats)):
        cols.append(cats[i].text) # extracts text from categories header

    del cols[0] # removes 'rank' category since it serves no purpose

    player = soup.find_all('tr')[2:] # everything after the categories header

    if len(player) >= 89:
        deletions = [87, 86, 65, 64, 43, 42, 21, 20] # after 20 players, it restates the categories for two columns, using th, not td
        for i in deletions: # so let's just go ahead and get those out of the way
            del player[i]
    elif len(player) <= 42 and len(player) >= 23: # if it doesn't go all the way to the end, code breaks, so let's segment it off
        deletions = [21, 20]
        for i in deletions:
            del player[i]
    elif len(player) <= 64 and len(player) >= 45:
        deletions = [43, 42, 21, 20]
        for i in deletions:
            del player[i]
    elif len(player) <= 86 and len(player) >= 67:
        deletions = [65, 64, 43, 42, 21, 20]
        for i in deletions:
            del player[i]

    for i in range(len(player)):
        for j in range(len(player[i].find_all('td'))):
            table.append(player[i].find_all('td')[j].text.encode('utf-8'))

    df = pd.DataFrame(np.array(table).reshape((len(table)/45),45), columns=cols) # len/45 since it won't always be 100/page
    print(page)
    return df

def scrape_cbb_full_year(year):
    pages = np.arange(100,4800,100)
    df = scrape_cbb_single_page(year,0)
    for page in pages:
        time.sleep(np.random.randint(0,1) + np.random.rand()) # let's give it a random, quick break
        df2 = scrape_cbb_single_page(year, page)
        if df2.shape[0] == 0:
            print(year)
            return df
        else:
            df = df.append(df2, ignore_index=True)
    print(year)
    return df

def scrape_cbb():
    print('CBB:')
    df = scrape_cbb_full_year(2018)
    df2 = pd.read_csv('../data/cbb/updated_cbb.csv')
    df2 = df2[df2['Season'] != '2017-18']
    df = df.append(df2, ignore_index=True)
    df.to_csv('../data/cbb/updated_cbb.csv', index=False)

if __name__ == '__main__':
    scrape_cbb()
