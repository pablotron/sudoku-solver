import json
import os
import random
import sys

# parent directory to front of module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sudoku

def test_invalid_grid():
  """test sudoku.InvalidGrid()"""
  tests = [{
    # not enough cells
    'grid': [0],
  }, {
    # too many cells
    'grid': [i for i in range(82)],
  }]

  # run tests
  for test in tests:
    try:
      sudoku._check_grid(test['grid'])
      assert False, 'never reached'
    except sudoku.InvalidGrid:
      assert True, 'got expected exception'

def test_invalid_cell():
  """test sudoku.InvalidCell()"""
  tests = [{
    # cell > 9
    'grid': [
      8, 10, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 3,  6, 0, 0,  0, 0, 0,
      0, 7, 0,  0, 9, 0,  2, 0, 0,

      0, 5, 0,  0, 0, 7,  0, 0, 0,
      0, 0, 0,  0, 4, 5,  7, 0, 0,
      0, 0, 0,  1, 0, 0,  0, 3, 0,

      0, 0, 1,  0, 0, 0,  0, 6, 8,
      0, 0, 8,  5, 0, 0,  0, 1, 0,
      0, 9, 0,  0, 0, 0,  4, 0, 0,
    ],
  }, {
    # cell < 0
    'grid': [
      8, -1, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 3,  6, 0, 0,  0, 0, 0,
      0, 7, 0,  0, 9, 0,  2, 0, 0,

      0, 5, 0,  0, 0, 7,  0, 0, 0,
      0, 0, 0,  0, 4, 5,  7, 0, 0,
      0, 0, 0,  1, 0, 0,  0, 3, 0,

      0, 0, 1,  0, 0, 0,  0, 6, 8,
      0, 0, 8,  5, 0, 0,  0, 1, 0,
      0, 9, 0,  0, 0, 0,  4, 0, 0,
    ],
  }]

  # run tests
  for test in tests:
    try:
      sudoku._check_grid(test['grid'])
      assert False, 'never reached'
    except sudoku.InvalidCell:
      assert True, 'got expected exception'

def test_grid_to_string():
  """test sudoku.grid_to_string()"""
  tests = [{
    'grid': [
      8, 0, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 3,  6, 0, 0,  0, 0, 0,
      0, 7, 0,  0, 9, 0,  2, 0, 0,

      0, 5, 0,  0, 0, 7,  0, 0, 0,
      0, 0, 0,  0, 4, 5,  7, 0, 0,
      0, 0, 0,  1, 0, 0,  0, 3, 0,

      0, 0, 1,  0, 0, 0,  0, 6, 8,
      0, 0, 8,  5, 0, 0,  0, 1, 0,
      0, 9, 0,  0, 0, 0,  4, 0, 0,
    ],

    'exp': '\n'.join([
      '-------------------------',
      '| 8 - - | - - - | - - - |',
      '| - - 3 | 6 - - | - - - |',
      '| - 7 - | - 9 - | 2 - - |',
      '|-----------------------|',
      '| - 5 - | - - 7 | - - - |',
      '| - - - | - 4 5 | 7 - - |',
      '| - - - | 1 - - | - 3 - |',
      '|-----------------------|',
      '| - - 1 | - - - | - 6 8 |',
      '| - - 8 | 5 - - | - 1 - |',
      '| - 9 - | - - - | 4 - - |',
      '-------------------------',
    ]),
  }]

  # run tests
  for test in tests:
    got = sudoku.grid_to_string(test['grid'])
    assert got == test['exp']

def test_pair_to_string():
  """test sudoku.pair_to_string()"""
  tests = [{
    'grid': [
      8, 0, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 3,  6, 0, 0,  0, 0, 0,
      0, 7, 0,  0, 9, 0,  2, 0, 0,

      0, 5, 0,  0, 0, 7,  0, 0, 0,
      0, 0, 0,  0, 4, 5,  7, 0, 0,
      0, 0, 0,  1, 0, 0,  0, 3, 0,

      0, 0, 1,  0, 0, 0,  0, 6, 8,
      0, 0, 8,  5, 0, 0,  0, 1, 0,
      0, 9, 0,  0, 0, 0,  4, 0, 0,
    ],

    'exp': '\n'.join([
      '-------------------------    -------------------------',
      '| 8 - - | - - - | - - - |    | 8 1 2 | 7 5 3 | 6 4 9 |',
      '| - - 3 | 6 - - | - - - |    | 9 4 3 | 6 8 2 | 1 7 5 |',
      '| - 7 - | - 9 - | 2 - - |    | 6 7 5 | 4 9 1 | 2 8 3 |',
      '|-----------------------|    |-----------------------|',
      '| - 5 - | - - 7 | - - - |    | 1 5 4 | 2 3 7 | 8 9 6 |',
      '| - - - | - 4 5 | 7 - - | -> | 3 6 9 | 8 4 5 | 7 2 1 |',
      '| - - - | 1 - - | - 3 - |    | 2 8 7 | 1 6 9 | 5 3 4 |',
      '|-----------------------|    |-----------------------|',
      '| - - 1 | - - - | - 6 8 |    | 5 2 1 | 9 7 4 | 3 6 8 |',
      '| - - 8 | 5 - - | - 1 - |    | 4 3 8 | 5 2 6 | 9 1 7 |',
      '| - 9 - | - - - | 4 - - |    | 7 9 6 | 3 1 8 | 4 5 2 |',
      '-------------------------    -------------------------',
    ]),
  }]

  # run tests
  for test in tests:
    got = sudoku.pair_to_string(test['grid'], sudoku.solve(test['grid']))
    assert got == test['exp']

def test_string_to_grid():
  """test sudoku.string_to_grid()"""

  # build 10 random grids
  rand_grids = [[random.randint(0, 9) for i in range(81)] for j in range(10)]

  pass_tests = [{
    'val': '012345678' * 9, # input string
    'exp': list(range(9)) * 9 # expected value
  }, {
    'val': '0' * 81, # input string
    'exp': [0] * 81 # expected value
  }] + [{ 'val': ''.join([str(c) for c in g]), 'exp': g } for g in rand_grids]

  # run pass tests
  for test in pass_tests:
    got = sudoku.string_to_grid(test['val'])
    assert got == test['exp']

  fail_tests = [{
    'val': '0', # invalid grid length
    'exp': sudoku.InvalidGrid
  }, {
    'val': 'a' * 81, # invalid cell value
    'exp': sudoku.InvalidCell
  }]

  # run fail tests
  for test in fail_tests:
    try:
      sudoku.string_to_grid(test['val'])
      assert False, 'never reached'
    except (sudoku.InvalidCell, sudoku.InvalidGrid) as err:
      assert isinstance(err, test['exp'])

def test_solve():
  """test sudoku.solve()"""
  tests = [{
    'grid': [
      8, 0, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 3,  6, 0, 0,  0, 0, 0,
      0, 7, 0,  0, 9, 0,  2, 0, 0,

      0, 5, 0,  0, 0, 7,  0, 0, 0,
      0, 0, 0,  0, 4, 5,  7, 0, 0,
      0, 0, 0,  1, 0, 0,  0, 3, 0,

      0, 0, 1,  0, 0, 0,  0, 6, 8,
      0, 0, 8,  5, 0, 0,  0, 1, 0,
      0, 9, 0,  0, 0, 0,  4, 0, 0,
    ],

    'exp': [
      8, 1, 2,  7, 5, 3,  6, 4, 9,
      9, 4, 3,  6, 8, 2,  1, 7, 5,
      6, 7, 5,  4, 9, 1,  2, 8, 3,

      1, 5, 4,  2, 3, 7,  8, 9, 6,
      3, 6, 9,  8, 4, 5,  7, 2, 1,
      2, 8, 7,  1, 6, 9,  5, 3, 4,

      5, 2, 1,  9, 7, 4,  3, 6, 8,
      4, 3, 8,  5, 2, 6,  9, 1, 7,
      7, 9, 6,  3, 1, 8,  4, 5, 2,
    ],
  }]

  # run tests
  for test in tests:
    got = sudoku.solve(test['grid'])
    assert got == test['exp']

# src: https://github.com/t-dillon/tdoku/blob/master/test/test_puzzles
def test_solve_many():
  """test sudoku.solve() with many sample grids"""

  # read grids.json
  with open(os.path.join(os.path.dirname(__file__), 'grids.json')) as f:
    grids = json.loads(f.read())

  # solve grids
  for grid in grids:
    got = sudoku.solve(grid['grid'])
    assert got != None, grid['name']
