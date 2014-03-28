"""
File utility functions
"""

import errno, os

def make_dirs(p):
  """
  Make full directory path for p
  """

  try:
    os.makedirs(p)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise(e)

