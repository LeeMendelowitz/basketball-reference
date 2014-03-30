"""
Parse all 2013 boxscores. 
Output a dataframe with team totals for each game.
"""

import glob
import sys
from basketball_reference import boxscore
import pandas

def run():
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


if __name__ == '__main__':
  run()
