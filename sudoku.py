"""
Sudoku Solver.

Example: Find Solution
----------------------
Script:

    import sudoku

    # build grid with solution
    grid = [
      8, 0, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 3,  6, 0, 0,  0, 0, 0,
      0, 7, 0,  0, 9, 0,  2, 0, 0,

      0, 5, 0,  0, 0, 7,  0, 0, 0,
      0, 0, 0,  0, 4, 5,  7, 0, 0,
      0, 0, 0,  1, 0, 0,  0, 3, 0,

      0, 0, 1,  0, 0, 0,  0, 6, 8,
      0, 0, 8,  5, 0, 0,  0, 1, 0,
      0, 9, 0,  0, 0, 0,  4, 0, 0
    ]

    # get solution
    solution = sudoku.solve(grid)

    # print result to standard output
    print(sudoku.pair_to_string(grid, solution) if solution else 'no solution')

Output:

    -------------------------    -------------------------
    | 8 - - | - - - | - - - |    | 8 1 2 | 7 5 3 | 6 4 9 |
    | - - 3 | 6 - - | - - - |    | 9 4 3 | 6 8 2 | 1 7 5 |
    | - 7 - | - 9 - | 2 - - |    | 6 7 5 | 4 9 1 | 2 8 3 |
    |-----------------------|    |-----------------------|
    | - 5 - | - - 7 | - - - |    | 1 5 4 | 2 3 7 | 8 9 6 |
    | - - - | - 4 5 | 7 - - | -> | 3 6 9 | 8 4 5 | 7 2 1 |
    | - - - | 1 - - | - 3 - |    | 2 8 7 | 1 6 9 | 5 3 4 |
    |-----------------------|    |-----------------------|
    | - - 1 | - - - | - 6 8 |    | 5 2 1 | 9 7 4 | 3 6 8 |
    | - - 8 | 5 - - | - 1 - |    | 4 3 8 | 5 2 6 | 9 1 7 |
    | - 9 - | - - - | 4 - - |    | 7 9 6 | 3 1 8 | 4 5 2 |
    -------------------------    -------------------------

Example: No Solution
--------------------
Script:

    import sudoku

    # build grid with no solution
    grid = [
      8, 8, 0,  0, 0, 0,  0, 0, 0,
      0, 0, 3,  6, 0, 0,  0, 0, 0,
      0, 7, 0,  0, 9, 0,  2, 0, 0,

      0, 5, 0,  0, 0, 7,  0, 0, 0,
      0, 0, 0,  0, 4, 5,  7, 0, 0,
      0, 0, 0,  1, 0, 0,  0, 3, 0,

      0, 0, 1,  0, 0, 0,  0, 6, 8,
      0, 0, 8,  5, 0, 0,  0, 1, 0,
      0, 9, 0,  0, 0, 0,  4, 0, 0
    ]

    # get solution
    solution = sudoku.solve(grid)

    # print grid and solution
    print(sudoku.pair_to_string(grid, solution) if solution else 'no solution')

Output:

    no solution
"""

import z3

#
# Cells:
#
#    0  1  2 |  3  4  5 |  6  7  8
#    9 10 11 | 12 13 14 | 15 16 17
#   18 19 20 | 21 22 23 | 24 25 26
#   ------------------------------
#   27 28 29 | 30 31 32 | 33 34 35
#   36 37 38 | 39 40 41 | 42 43 44
#   45 46 47 | 48 49 50 | 51 52 53
#   ------------------------------
#   54 55 56 | 57 58 59 | 60 61 62
#   63 64 65 | 66 67 68 | 69 70 71
#   72 73 74 | 75 76 77 | 78 79 80
#
# Subgrids:
#
#   0 | 1 | 2
#   ---------
#   3 | 4 | 5
#   ---------
#   6 | 7 | 8
#

class InvalidGrid(Exception):
  """Invalid grid size (must have 81 cells)."""

class InvalidCell(Exception):
  """Invalid cell value (must be between 0 and 9, inclusive)."""

def _check_grid(grid: list[int]) -> None:
  """Check grid length and cell values.  Raises exception on error."""

  # check grid size
  if len(grid) != 81:
    raise InvalidGrid("grid length must equal 81")

  # check cells
  for i in range(81):
    if grid[i] < 0 or grid[i] > 9:
      raise InvalidCell('invalid cell value: %d' % (grid[i]))

def _subgrid(grid: list[z3.Int], i: int) -> list[z3.Int]:
  """
  Get Nth subgrid of grid.

  Used by solve() to build subgrid constraints.
  """
  return [grid[9 * (3 * (i // 3) + (j // 3)) + 3 * (i % 3) + (j % 3)] for j in range(9)]

def solve(grid: list[int]) -> list[int] | None:
  """
  Solve grid and return first solution, or None of there is no solution.

  Example
  -------
  >>> grid = [
  ...   8, 0, 0,  0, 0, 0,  0, 0, 0,
  ...   0, 0, 3,  6, 0, 0,  0, 0, 0,
  ...   0, 7, 0,  0, 9, 0,  2, 0, 0,
  ...
  ...   0, 5, 0,  0, 0, 7,  0, 0, 0,
  ...   0, 0, 0,  0, 4, 5,  7, 0, 0,
  ...   0, 0, 0,  1, 0, 0,  0, 3, 0,
  ...
  ...   0, 0, 1,  0, 0, 0,  0, 6, 8,
  ...   0, 0, 8,  5, 0, 0,  0, 1, 0,
  ...   0, 9, 0,  0, 0, 0,  4, 0, 0
  ... ]
  >>> sudoku.solve(grid)
  [8, 1, 2, 7, 5, 3, 6, 4, 9, ... (omitted) ..., 7, 9, 6, 3, 1, 8, 4, 5, 2]
  """

  _check_grid(grid)

  # create solver
  s = z3.Solver()

  # build 9x9 grid of cells
  # cells = [z3.Int('c%d' % (i)) for i in range(81)]
  cells = z3.IntVector('c', 81)

  # cells must be between 1 and 9 (inclusive)
  s.add([z3.And(c >= 1, c <= 9) for c in cells])

  # row cells must be distinct
  s.add([z3.Distinct([cells[9 * y + x] for x in range(9)]) for y in range(9)])

  # column cells must be distinct
  s.add([z3.Distinct([cells[9 * y + x] for y in range(9)]) for x in range(9)])

  # subgrid cells must be distinct
  s.add([z3.Distinct(_subgrid(cells, i)) for i in range(9)])

  # add known cells
  for i in range(len(grid)):
    if grid[i] != 0:
      s.add(cells[i] == grid[i])

  # is there a solution?
  if s.check() == z3.sat:
    # yes, build solution from model
    m = s.model()
    return [m[cells[i]].as_long() for i in range(81)]
  else:
    # no, return None
    return None

def _grid_to_rows(grid: list[int]) -> list[str]:
  """
  Return printable list of grid rows.

  Used by grid_to_string() and pair_to_string().
  """

  _check_grid(grid)

  # declare rows with header
  rows = ['-' * 25]
  for y in range(9):
    row = []

    for x in range(9):
      # get value
      v = grid[9 * y + x]

      # append to row
      row.append(str(v) if v != 0 else '-')

      # append subgrid delimiter
      if x > 0 and x < 8 and ((x + 1) % 3 == 0):
        row.append('|')

    # append row to rows
    rows.append('| ' + ' '.join(row) + ' |')

    # append subgrid delimiter
    if y > 0 and y < 8 and ((y + 1) % 3 == 0):
      rows.append('|' + ('-' * 23) + '|')

  # append footer
  rows.append('-' * 25)

  # return result
  return rows

def grid_to_string(grid: list[int]) -> str:
  """
  Return printable string of grid.

  Example
  -------
  >>> print(sudoku.grid_to_string([random.randint(0, 9) for i in range(81)]))
  -------------------------
  | 5 7 1 | 4 - 9 | 9 7 9 |
  | - 7 4 | 1 4 8 | 5 6 5 |
  | 2 8 9 | 1 7 - | 6 5 9 |
  |-----------------------|
  | 6 4 - | - 8 3 | 2 8 6 |
  | 8 3 3 | 3 - 8 | 6 8 7 |
  | 2 6 4 | 2 2 5 | 6 2 2 |
  |-----------------------|
  | 3 - 9 | 3 3 8 | 5 4 4 |
  | 9 4 6 | 8 1 1 | 6 8 4 |
  | 1 8 5 | 7 4 6 | 6 1 9 |
  -------------------------
  """
  return "\n".join(_grid_to_rows(grid))

def _row_delim(i: int) -> str:
  """
  Return delimiter for given output row.

  Used by pair_to_string() to delimit input and output.
  """
  return ' -> ' if i == 6 else '    '

def pair_to_string(src: list[int], dst: list[int]) -> str:
  """
  Return printable string of grid and solution.

  Example
  -------
  >>> grid = # ... omitted
  >>> print(sudoku.pair_to_string(grid, sudoku.solve(grid)))
  -------------------------    -------------------------
  | 8 - - | - - - | - - - |    | 8 1 2 | 7 5 3 | 6 4 9 |
  | - - 3 | 6 - - | - - - |    | 9 4 3 | 6 8 2 | 1 7 5 |
  | - 7 - | - 9 - | 2 - - |    | 6 7 5 | 4 9 1 | 2 8 3 |
  |-----------------------|    |-----------------------|
  | - 5 - | - - 7 | - - - |    | 1 5 4 | 2 3 7 | 8 9 6 |
  | - - - | - 4 5 | 7 - - | -> | 3 6 9 | 8 4 5 | 7 2 1 |
  | - - - | 1 - - | - 3 - |    | 2 8 7 | 1 6 9 | 5 3 4 |
  |-----------------------|    |-----------------------|
  | - - 1 | - - - | - 6 8 |    | 5 2 1 | 9 7 4 | 3 6 8 |
  | - - 8 | 5 - - | - 1 - |    | 4 3 8 | 5 2 6 | 9 1 7 |
  | - 9 - | - - - | 4 - - |    | 7 9 6 | 3 1 8 | 4 5 2 |
  -------------------------    -------------------------
  """

  # convert to rows
  src = _grid_to_rows(src)
  dst = _grid_to_rows(dst)

  # build and return output string
  return "\n".join([f'{src[i]}{_row_delim(i)}{dst[i]}' for i in range(len(src))])

def string_to_grid(s: str) -> list[int]:
  """
  Parse given string as grid.  String must contain 81 characters in the
  range 0-9, inclusive.

  Raises an exception if the given string is invalid.

  Example
  -------
  >>> grid = sudoku.string_to_grid('012345678' * 9)
  >>> print(sudoku.grid_to_string(grid))
  -------------------------
  | - 1 2 | 3 4 5 | 6 7 8 |
  | - 1 2 | 3 4 5 | 6 7 8 |
  | - 1 2 | 3 4 5 | 6 7 8 |
  |-----------------------|
  | - 1 2 | 3 4 5 | 6 7 8 |
  | - 1 2 | 3 4 5 | 6 7 8 |
  | - 1 2 | 3 4 5 | 6 7 8 |
  |-----------------------|
  | - 1 2 | 3 4 5 | 6 7 8 |
  | - 1 2 | 3 4 5 | 6 7 8 |
  | - 1 2 | 3 4 5 | 6 7 8 |
  -------------------------
  """
  grid = [ord(s[i]) - 48 for i in range(len(s))]
  _check_grid(grid)
  return grid
