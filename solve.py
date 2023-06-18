#!/usr/bin/env python3

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

# check for solution
if solution:
  # print solution
  print(sudoku.pair_to_string(grid, solution))
else:
  print('no solution')
