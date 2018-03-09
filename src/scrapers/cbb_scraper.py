import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

def scrape_cbb_single_page(year, page):
    url = "http://www.sports-reference.com/cbb/play-index/psl_finder.cgi?request=1&match=single&year_min={0}&year_max={0}&conf_id=&school_id=&class_is_fr=Y&class_is_so=Y&class_is_jr=Y&class_is_sr=Y&pos_is_g=Y&pos_is_gf=Y&pos_is_fg=Y&pos_is_f=Y&pos_is_fc=Y&pos_is_cf=Y&pos_is_c=Y&games_type=A&qual=&c1stat=fg&c1comp=gt&c1val=0&c2stat=ts_pct&c2comp=gt&c2val=0&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=player&order_by_asc=Y&offset={1}".format(year, page)
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
            if table[i][0] == 'Totals':
                dropsies.append(i)

        dropsies.sort(reverse=True)

        for i in dropsies:
            table.pop(i)

        for i in range(len(table)):
            table[i].pop(0)

        classes = ['FR', 'SO', 'JR', 'SR']
        year_stop = '{0}-{1}'.format(int(year)-1,str(year)[2:])

        # player names
        for i in range(len(table)):
            for j in range(1,len(table[i])): # avoid players named 'JR' - yes, this happened
                if table[i][j] in classes:
                    stop = j
                    break
                elif table[i][j] == year_stop:
                    table[i].insert(j, 'NaN')
                    stop = j
                    break
            table[i][0:stop] = [' '.join(table[i][0:stop])]

        positions = ['G', 'G-F', 'F', 'F-G', 'F-C', 'C', 'C-F']
        conf = ['A-10', 'AAC', 'ACC', 'AEC', 'A-Sun', 'Big', 'CAA', 'CUSA', 'GWC', 'Horizon', 'Ind', 'Ivy', 'MAAC', 'MAC', 'MEAC', 'Mid-Cont', 'MVC', 'MW', 'MWC', 'NEC', 'OVC', 'Pac-10', 'Pac-12', 'Patriot', 'SEC', 'Southland', 'Summit', 'Sun', 'SWAC', 'WAC', 'WCC']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50']

        # school names
        for i in range(len(table)):
            if table[i][3] in positions:
                start = 3
            elif table[3] not in positions:
                table[i].insert(3, 'NaN')
                start = 3
            for k in range(len(table[i])):
                if table[i][k] in conf or table[i][k] == 'Southern' and table[i][k+1] in numbers:
                    stop = k
            table[i][start+1:stop] = [' '.join(table[i][start+1:stop])]

        # two-word conference names
        for i in range(len(table)):
            for j in range(len(table[i])):
                if table[i][5] == 'Sun' or table[i][5] == 'Big':
                    table[i][5:7] = [' '.join(table[i][5:7])]

        # eFG% fix
        for i in range(len(table)):
            if len(table[i]) == 44:
                table[i].insert(27, '.000')
        # all but AST% and BPM fix
        for i in range(len(table)):
            if len(table[i]) == 35 or len(table[i]) == 32:
                table[i].insert(29, '0') #DRtg
                table[i].insert(29, '0') #ORtg
                table[i].insert(29, '0') #PProd
                table[i].insert(29, '0') #USG%
                table[i].insert(28, '0') #BLK%
                table[i].insert(28, '0') #STL%
                table[i].insert(27, '0') #TRB%
                table[i].insert(27, '0') #DRB%
                table[i].insert(27, '0') #ORB%
                table[i].insert(25, '0') #PER
        # all but BPM fix
        for i in range(len(table)):
            if len(table[i]) == 34 or len(table[i]) == 31:
                table[i].insert(28, '0') #DRtg
                table[i].insert(28, '0') #ORtg
                table[i].insert(28, '0') #PProd
                table[i].insert(28, '0') #USG%
                table[i].insert(27, '0') #BLK%
                table[i].insert(27, '0') #STL%
                table[i].insert(27, '0') #AST%
                table[i].insert(27, '0') #TRB%
                table[i].insert(27, '0') #DRB%
                table[i].insert(27, '0') #ORB%
                table[i].insert(25, '0') #PER
        # BPM fix
        for i in range(len(table)): # separating these out to make sure if one gets bumped up to 42 that it gets hit
            if len(table[i]) == 42:
                table[i].extend(['0', '0', '0'])

        for i in range(len(table)):
            if len(table[i]) == 24:
                table[i].extend(['0', '0', '0'])
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-19, '0')
                table[i].insert(-21, '0')
                table[i].insert(-21, '0')
                table[i].insert(-27, '0')
                table[i].insert(-27, '0')
                table[i].insert(7, 'NaN')
            elif len(table[i]) == 25:
                table[i].extend(['0', '0', '0'])
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-19, '0')
                table[i].insert(-21, '0')
                table[i].insert(-21, '0')
                table[i].insert(-27, '0')
                table[i].insert(-27, '0')
                table[i].insert(7, 'NaN')
            elif year <= 2007 and len(table[i]) == 26:
                table[i].extend(['0', '0', '0'])
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-19, '0')
                table[i].insert(-21, '0')
                table[i].insert(-21, '0')
                table[i].insert(-27, '0')
                table[i].insert(-27, '0')
            elif year > 2007 and len(table[i]) == 26:
                table[i].extend(['0', '0', '0'])
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-19, '0')
                table[i].insert(-21, '0')
                table[i].insert(-27, '0')
                table[i].insert(-27, '0')
                table[i].insert(7, 'NaN')
            elif len(table[i]) == 27:
                table[i].extend(['0', '0', '0'])
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-19, '0')
                table[i].insert(-21, '0')
                table[i].insert(-27, '0')
                table[i].insert(-27, '0')
                table[i].insert(7, 'NaN')
            elif len(table[i]) == 28:
                table[i].extend(['0', '0', '0'])
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-6, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-11, '0')
                table[i].insert(-19, '0')
                table[i].insert(-21, '0')
                table[i].insert(-27, '0')
                table[i].insert(-27, '0')

        cols.pop(0)

        df = pd.DataFrame(table, columns=cols)
        df['Yr'] = year
        df['Player'] = df['Player'].str.strip(' *')
        print(page)
        return df
    elif not table:
        df = pd.DataFrame(table)
        print(page)
        return df

def scrape_cbb_full_year(year):
    pages = np.arange(100,10000,100)
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

def scrape_cbb_all_years():
    print('CBB:')
    df = scrape_cbb_full_year(2018)
    years = range(2001,2018)
    years.sort(reverse=True)
    for year in years:
        time.sleep(np.random.randint(0,5) + np.random.rand())
        df2 = scrape_cbb_full_year(year)
        df = df.append(df2, ignore_index=True)
    df.to_csv('../data/march_5_cbb_2001_to_2018.csv', index=False)

if __name__ == '__main__':
    scrape_cbb_all_years()
