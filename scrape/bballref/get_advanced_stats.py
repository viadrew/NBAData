#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
# Script to retrieve advanced stats of all players in a season
#
# Usage: python get_advanced_stats.py -y 2017 -o data/
#
# Author: Andrew Hong
# Last Updated: 2016-11-23
#
################################################################################

from bs4 import BeautifulSoup
from collections import deque
from distutils.dir_util import mkpath
import optparse
import os
import pandas as pd
import requests
import re

def scrape(url, filename):
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

if __name__ == '__main__':
    # Parse command line option
    p = optparse.OptionParser()
    p.add_option('-y', '--year', action='store', help='Season to pull data from')
    p.add_option('-o', '--output_dir', action='store', dest='output_dir', help='output directory name')
    opt, args = p.parse_args()

    # Get args
    year = opt.year
    output_dir = opt.output_dir

     # Check if output directory exists; if not, create it
    if not os.path.exists(output_dir):
        mkpath(output_dir)

    url = 'http://www.basketball-reference.com/leagues/NBA_' + year + '_advanced.html'
    filename = os.path.join(output_dir,'advanced_player_stats_' + year + '.csv')
    scrape(url, filename)