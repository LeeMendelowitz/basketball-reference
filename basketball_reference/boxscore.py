"""
Parse a box score page.
"""
from bs4 import BeautifulSoup
from itertools import izip
import pandas
import numpy as np

def parse_basic_team_stats(elem):
  """
  Parse the basic team stats table from the box score page.

  Both the visiting and home team have basic stats table, which
  summarizes the stats for each player.
  """

  # Parse header
  thead = elem.find('thead')
  header_row = thead.find_all('tr')[1]
  stats_columns = [th.attrs['data-stat'] for th in header_row.find_all('th')] + ['starter']
 
  
  player_stats_columns = stats_columns
  team_stats_columns = stats_columns[1:-2] # Trim the 'player' first column and 'starter', +/- columns.

  # Specify the data type for each stat.
  stat_types = [str, #player
                str, #MP
                int,
                int,
                float, #FG%
                int,
                int,
                float, #3P%
                int,
                int,
                float, #FT%
                int, #ORB
                int, #DRB
                int, #TRB
                int, #AST
                int, #STL
                int, #BLK
                int, #TOV
                int, #PF
                int, #PTS
                int, #+/-,
                bool #is_starter
                ]

  player_stat_types = stat_types #for is_starter
  team_stat_types = stat_types[1:-2]

  #######################################
  # Parse body to build player stats table
  tbody = elem.find('tbody')
  is_starter = True
  data = []
  for tr in tbody.find_all('tr'):

    # Check if this row is the "header" row which splits starters and reserves
    if 'thead' in tr.attrs.get('class',''):
      is_starter = False
      continue

    # Parse/Convert the data in row.
    d = [t(td.text) if td.text else None for t,td in izip(player_stat_types, tr.find_all('td'))]
    d.append(is_starter)
    data.append(d)

  # Make a dataframe of player stats
  player_stats = pandas.DataFrame(data, columns = player_stats_columns)

  ###########################################
  # Parse footer to get team totals
  # Get the team team totals
  team_tds = elem.find('tfoot').find_all('td')[1:]
  team_stats = [t(td.text) if td.text else None for t,td in izip(team_stat_types, team_tds)] 
  team_stats = pandas.Series(team_stats, index = team_stats_columns)

  return (player_stats, team_stats)


def parse_box_scores(src):
  """
  Given page source, parse visiting and home team box scores.

  TODO: parse game date??
  """

  soup = BeautifulSoup(src)
  divs = soup.find_all('div', class_ = 'table_container')

  # Get team codes from the first div ("Four Factors")
  teams = [e.text for e in divs[0].find_all('a')]
  visiting_team, home_team = teams

  # Get the visiting team table
  visiting_player_stats, visiting_team_totals = parse_basic_team_stats(divs[1])
  home_player_stats, home_team_totals = parse_basic_team_stats(divs[3])


  return {'visiting_team' : visiting_team,
          'visiting_player_stats' : visiting_player_stats,
          'visiting_team_totals' : visiting_team_totals,
          'home_team' : home_team,
          'home_player_stats' : home_player_stats,
          'home_team_totals' : home_team_totals
          }

