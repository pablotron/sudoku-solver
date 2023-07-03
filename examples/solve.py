#!/usr/bin/env python

#
# solve.py: Solve sample sudoku puzzle and print solution.
#

import os, sys

# prepend parent directory to module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sudoku

# sample grid
grid = [
  8, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 3,  6, 0, 0,  0, 0, 0,
  0, 7, 0,  0, 9, 0,  2, 0, 0,

  0, 5, 0,  0, 0, 7,  0, 0, 0,
  0, 0, 0,  0, 4, 5,  7, 0, 0,
  0, 0, 0,  1, 0, 0,  0, 3, 0,

  0, 0, 1,  0, 0, 0,  0, 6, 8,
  0, 0, 8,  5, 0, 0,  0, 1, 0,
  0, 9, 0,  0, 0, 0,  4, 0, 0,
]

# find solution
solution = sudoku.solve(grid)

# print solution if it exists, or 'no solution' if no solution exists
print(sudoku.pair_to_string(grid, solution) if solution else 'no solution')
