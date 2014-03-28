"""
Parse games table.
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
  for url in urls:
    url = url.lstrip('/')
    dirpath = os.path.dirname(url)
    make_dirs(dirpath)

    sys.stderr.write("Downloading file %s..."%url)

    full_url = '%s%s'%(URL_BASE, url)
    response = requests.get(full_url)
    f = open(url, 'w')
    f.write(response.text)
    f.close()

    sys.stderr.write('done!\n')

    # Be kind to Basketball-Reference.com
    time.sleep(1)

if __name__ == '__main__':
  download_boxscores()
  