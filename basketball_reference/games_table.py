"""
Parse the table of NBA games for a given season.

Here is an example of the page being parsed:
http://www.basketball-reference.com/leagues/NBA_2013_games.html
"""

from bs4 import BeautifulSoup
import pandas
import requests
import os

from .globals import *

def parse_games_table_row(row):
  """
  Parse a tbody row from a games table.
  """
  cells = row.find_all('td')

  # Parse Game date
  game_date = cells[0].text

  # Parse BoxScore URL
  box_score_url = cells[1].find('a').attrs['href']
  visitor_team = cells[2].text
  visitor_team_pts = int(cells[3].text)

  home_team = cells[4].text
  home_team_pts = int(cells[5].text)

  ots = cells[6].text
  notes = cells[7].text

  return [game_date, box_score_url, visitor_team, visitor_team_pts, home_team, home_team_pts,
          ots, notes]

def parse_games_table(src):
  """
  Given page html source, return a DataFrame with games table.
  """

  soup = BeautifulSoup(src)
  table = soup.find(id='games')

  # Read the header
  header = table.find('thead')
  header_cells = header.find_all('th')

  header_names = [h.attrs['data-stat'] for h in header_cells]
  header_names[1] = 'box_score_url'

  tbody = table.find('tbody')
  trs = tbody.find_all('tr')
  row_data = [parse_games_table_row(tr) for tr in trs]

  return pandas.DataFrame(data = row_data, columns = header_names)

def download(year, output_path=None):
  """
  Download the games page src for the specified NBA year,
  and write the html to the output_path.

  If output_path is not provided, return it.
  """
  year = int(year)
  url = "{base}/leagues/NBA_{year}_games.html".format(URL_BASE, year)
  response = requests.get(url)

  if output_path is None:
    return response.text
  else:
    fout = open(os.path.abspath(output_path), 'w')
    fout.write(response.text)
    fout.close()

  return response.text

def to_csv(src_file, output_path):
  """
  Convert the source file stored locally to a csv file.
  """
  src = open(src_file).read()
  df = parse_games_table(src)
  df.to_csv(os.path.abspath(output_path), index=False)
