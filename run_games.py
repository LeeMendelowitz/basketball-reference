"""
Download all 2013 boxscores.
"""

import os
import sys
from file_utils import make_dirs
import pandas
import time
import requests

from basketball_reference import games_table
from basketball_reference.globals import URL_BASE


def games_to_csv():
  src = os.path.join('pages', 'NBA_2013_games.html')
  games_table.to_csv(src, 'games.csv')

def download_boxscores():
  """ 
  Download all boxscores.
  """

  df = pandas.read_csv('games.csv')
  urls = df['box_score_url']

  #import pdb; pdb.set_trace()
  n = len(urls)

  for i, url in enumerate(urls):
    url = url.lstrip('/')
    dirpath = os.path.dirname(url)
    make_dirs(dirpath)

    full_url = '%s/%s'%(URL_BASE, url)
    sys.stderr.write("Downloading file %i of %i: %s..."%(i, n, full_url))
  
    response = requests.get(full_url)
    with open(url, 'w') as f:
      f.write(response.text.encode('utf-8', errors='ignore'))

    sys.stderr.write('done!\n')

    # Be kind to Basketball-Reference.com
    time.sleep(1)

if __name__ == '__main__':
  download_boxscores()
  