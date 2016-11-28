#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
# Script to retrieve advanced stats of all players in a season
#
# Usage: python scrape.py -y 2017 -o data/
#
# Author: Andrew Hong
# Last Updated: 2016-11-23
#
################################################################################

from bs4 import BeautifulSoup
from collections import deque
from distutils.dir_util import mkpath
import optparse
from os.path import abspath, dirname, join
import pandas as pd
import requests
import re

def scrape(year):
    url = 'http://www.basketball-reference.com/leagues/NBA_' + year + '_advanced.html'

    ROOT_DIR = dirname(dirname(dirname(abspath(__file__))))
    filename = join(ROOT_DIR, 'data/bballref/players_advanced_' + year + '.csv')

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
    except:
        print('error')

    # Scrape table
    site = soup.find('div', {'class':'table_outer_container'} )
    tables = site.findAll('table')
    rows = tables[0].findAll('tr')

    headers = [h.string for h in rows[0].findAll('th')]
    # Remove 'Rk'; not parsed in 'td'
    headers = headers[1:]

    # Add all data to a queue, then pop a row's worth of data into an list to be stored in another list
    raw_data = deque()
    data = []

    for row in rows[1:]:
        cols = row.findAll('td')

        for col in cols:
            text = col.find(text=True)
            raw_data.append(text)

    while not not raw_data:
        tmp = []
        for i in range(len(headers)):
            tmp.append(raw_data.popleft())
        data.append(tmp)

    # Remove split data of players (due to trades etc)
    # Team TOT will always be first
    players = {}
    duplicates = []
    for index, row in enumerate(data):
        tup = (row[0], row[1], row[2])
        if (tup) not in players:
            players[tup] = index
        else:
            tot_index = players[tup]
            if data[tot_index][3] == 'TOT':
                data[tot_index][3] = data[index][3]
            else:
                data[tot_index][3] = data[tot_index][3] + ' / ' + data[index][3]
            duplicates.append(index)

    # Remove the separated data
    data = [row for i, row in enumerate(data) if i not in duplicates]

    # To dataframe, to easily remove empty columns
    f = pd.DataFrame.from_records(data, columns=headers)
    parsed_headers = [h for h in headers if not re.search(h.string, u'\xc2\xa0')]
    new_f = f[parsed_headers]

    # Write final to csv
    new_f.to_csv(filename, index=False)