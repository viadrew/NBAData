#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
# Script to retrieve advanced stats of all players in a season
#
# Usage: python get_advanced_stats.py -y 2017 -o data/
#
# Author: Andrew Hong
# Last Updated: 2016-11-20
#
################################################################################

from bs4 import BeautifulSoup
from collections import deque
from distutils.dir_util import mkpath
import csv
import optparse
import os
import pandas as pd
import requests
import re
import sys

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

    # Write headers
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

    # Add all data to a queue, then pop a row's worth of data into another queue and write the row to csv
    data = deque()
    row_data = deque(maxlen=len(headers))

    with open(filename, 'a') as f:
        writer = csv.writer(f)

        for row in rows[1:]:
            cols = row.findAll('td')

            for col in cols:
                text = col.find(text=True)
                data.append(text)


        while not not data:
            for i in range(len(headers)):
                row_data.append(data.popleft())
            writer.writerow(row_data)

    # Get rid of empty columns
    parsed_headers = [h for h in headers if not re.search(h.string, u'\xc2\xa0')]
    f = pd.read_csv(filename)
    new_f = f[parsed_headers]
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
    filename = os.path.join(output_dir,'test' + year + '.csv')
    scrape(url, filename)