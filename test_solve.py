import sudoku

def test_solve():
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

  for row in tests:
    got = sudoku.solve(row['grid'])
    assert got == row['exp']

# 
# # read grids.json
# with open(pathlib.Path(__file__).parent.joinpath('grids.json')) as f:
#   grids = json.loads(f.read())
# 
# # solve grids
# for grid in grids:
#   solution = sudoku.solve(grid['grid'])
# 
#   if solution:
#     print(grid['name'] + ':')
#     print(sudoku.pair_to_string(grid['grid'], solution))
#   else:
#     print('%s: no solution' % (grid['name']))
# 
