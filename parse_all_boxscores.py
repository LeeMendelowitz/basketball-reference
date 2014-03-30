"""
Parse all 2013 boxscores. 
Output a dataframe with team totals for each game.
"""

import glob
import sys
from basketball_reference import boxscore
import pandas

def run():
  """
  Output team totals.
  """
  output_file = '2013_games_data.csv'
  boxscore_files = glob.glob('boxscores/*.html')
  n = len(boxscore_files)

  col_names = ['home_team', 'visiting_team']

  rows = []
  for i, bsfile in enumerate(boxscore_files):
    sys.stderr.write('reading file %i of %i: %s\n'%(i, n, bsfile))
    with open(bsfile) as f:
      src = f.read()
      data = boxscore.parse_box_scores(src)
      home_data = data['home_team_totals']
      visitor_data = data['visiting_team_totals']

      assert(all(home_data.index == visitor_data.index))
      base_names = list(home_data.index)
      visiting_names = ['visiting_' + bn for bn in base_names]
      home_names = ['home_' + bn for bn in base_names]
      
      # Rename the Series Data
      home_data.rename(index=dict(zip(base_names, home_names)), inplace=True)
      visitor_data.rename(index=dict(zip(base_names, visiting_names)), inplace=True)
      teams = pandas.Series([data['visiting_team'], data['home_team']], index=['visiting', 'home'])

      # Concat series
      row = pandas.concat([teams, visitor_data, home_data])
      rows.append(row)

  df = pandas.DataFrame(rows)
  df.to_csv(output_file, index=False)
  return df

def boxscores_diff(csv_path):
    """
    Take differential of winner minus loser
    """
    df = pandas.read_csv(csv_path)

    # Did home team win?
    home_win = df.home_pts > df.visiting_pts

    # Split the stats into visiting and home
    stats_index = df.columns[2:]
    n = len(stats_index)/2
    visiting_index = stats_index[:n]
    home_index = stats_index[n:]

    home_stats = df[home_index]
    visiting_stats = df[visiting_index]

    # Reindex the home and visiting dataframes
    new_cols = [colname.split('_', 1)[1] for colname in home_stats.columns]
    home_stats.columns = new_cols
    visiting_stats.columns = new_cols

    # Take differential
    win_differential = home_stats - visiting_stats

    # Negate values where the home team loss
    home_loss = win_differential.pts < 0
    win_differential.ix[home_loss] = -win_differential.ix[home_loss]

    return win_differential 

def run2():
  # Compute win differentials
  csv = 'data/2013_games_data.csv'
  diff = boxscores_diff(csv)
  diff.to_csv('2013_games_data_diff.csv', index=False)


if __name__ == '__main__':
  #run()
  run2()
