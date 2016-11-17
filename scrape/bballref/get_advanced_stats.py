import requests
import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup

# Author: Andrew Hong
#
# Last Updated:

def scrape(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content)
    except:
        print('error')

    test = soup.find('div', {'class':'table_outer_container'} )
    tables = test.find_all('table')
    rows = tables[0].findAll('tr')

    for row in enumerate(rows):
        cols = row.findAll('td')

        for col in cols:
            print('')

if __name__ == '__main__':
    u = 'http://www.basketball-reference.com/leagues/NBA_2016_advanced.html'
    scrape(u)