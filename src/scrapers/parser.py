import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

### this is a messy one, so bear with me.

def grab_from_page():
    df_transfer_check = pd.read_csv('../src/data/transfer_check.csv')
    searcher = str(stuff).replace('.html">', '</a>').split('</a>')

    player_schools = []
    schools = df_transfer_check['School'].unique()

    for i in range(len(searcher)):
        if searcher[i] in schools:
            player_schools.append(searcher[i])
    player_schools = set(player_schools)
    player_schools = list(player_schools)
    return player_schools


if __name__ == '__main__':
    df_transfer_check = pd.read_csv('../src/data/transfer_check.csv')
    player_match = []
    all_players = df_transfer_check['Player'].unique()

    for player in all_players:
        url = "http://www.sports-reference.com/cbb/search/search.fcgi?hint=&search={0}&pid=&idx=".format(player)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        stuff = soup.select('tr')

        if not stuff:
            iterable = soup.find_all('div', attrs = {'class': 'search-item-url'})
            for i in range(len(iterable)):
                url = "http://www.sports-reference.com/{0}".format(iterable[i].text)
                req = requests.get(url)
                soup = BeautifulSoup(req.text, 'html.parser')
                stuff = soup.select('tr')
                player_match.append([player, grab_from_page()])
        else:
            player_match.append([player, grab_from_page()])
        print(player)
