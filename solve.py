#!/usr/bin/env python3

import json
import os
import pathlib
import sudoku

# read grids.json
with open(pathlib.Path(__file__).parent.joinpath('grids.json')) as f:
  grids = json.loads(f.read())

# solve grids
for grid in grids:
  solution = sudoku.solve(grid['grid'])

  if solution:
    print(grid['name'] + ':')
    print(sudoku.pair_to_string(grid['grid'], solution))
  else:
    print('%s: no solution' % (grid['name']))
