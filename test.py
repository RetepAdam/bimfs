import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

group = []

years = np.arange(2005,2018,1)
years = years[::-1]

for year in years:
    url = "http://www.basketball-reference.com/draft/NBA_{0}.html".format(year)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stuff = soup.select('tr')



    for i in np.arange(2,32,1):
        group.append(stuff[i].select('td')[2]['csk'])
    print(year)

years = np.arange(1995,2005,1)
years = years[::-1]

for year in years:
    url = "http://www.basketball-reference.com/draft/NBA_{0}.html".format(year)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    stuff = soup.select('tr')



    for i in np.arange(2,30,1):
        group.append(stuff[i].select('td')[2]['csk'])
    print(year)
