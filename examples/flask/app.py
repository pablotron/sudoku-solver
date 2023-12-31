#
# app.py: Minimal sudoku solver web interface.
#
# Usage:
#
# Install the development dependencies, then run flask via `pipenv` in
# the `examples/flask/` directory.  Example:
#
#   pipenv install --dev # install development dependencies
#   cd examples/flask/
#   pipenv run flask run # run flask
#
# Finally, point your browser at the following URL:
#
# http://localhost:5000/
#
# Note: This application is not secure and should not be run in a
# production environment.
#

import hashlib, htmlmin, json, os, sys, time
from flask import Flask, abort, request, render_template

# prepend top-level directory to module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import sudoku

# default grid
DEFAULT_GRID = [
  8, 0, 0,  0, 0, 0,  0, 0, 0,
  0, 0, 3,  6, 0, 0,  0, 0, 0,
  0, 7, 0,  0, 9, 0,  2, 0, 0,

  0, 5, 0,  0, 0, 7,  0, 0, 0,
  0, 0, 0,  0, 4, 5,  7, 0, 0,
  0, 0, 0,  1, 0, 0,  0, 3, 0,

  0, 0, 1,  0, 0, 0,  0, 6, 8,
  0, 0, 8,  5, 0, 0,  0, 1, 0,
  0, 9, 0,  0, 0, 0,  4, 0, 0,
];

# action buttons
BUTTONS = [{
  'id': 'solve',
  'name': 'Solve',
  'help': 'Solve grid.',
}, {
  'id': 'download',
  'name': 'Download',
  'help': 'Download grid as text file.',
}, {
  'id': 'reset',
  'name': 'Reset',
  'help': 'Reset grid.',
}, {
  'id': 'clear',
  'name': 'Clear',
  'help': 'Clear grid.',
}]

# create app
app = Flask(__name__)

@app.route("/")
def home():
  return htmlmin.minify(render_template('index.html',
    title = 'Solve-o-Matic',
    buttons = BUTTONS,
    reset_grid = ''.join([str(d) for d in DEFAULT_GRID]),
  ))

@app.route('/solve', methods=['POST'])
def solve():
  # decode json body
  data = json.loads(request.data)

  # parse string as grid
  grid = sudoku.string_to_grid(data['grid'])
  app.logger.info('grid: %s' % (grid))

  # find solution, time solve()
  t0 = time.time_ns()
  solution = sudoku.solve(grid)
  t1 = time.time_ns()

  return {
    'time': t1 - t0,
    'grid': ''.join([str(d) for d in solution]) if solution else '',
  }

def file_name(body: str) -> str:
  """Get name of downloadable text file."""

  # build filename suffix by from shake128 "digest" of body
  # (used to generate downloadable filename suffix)
  suffix = hashlib.shake_128(body.encode()).hexdigest(8)

  # return filename
  return f"grid-{suffix}.txt"

@app.route('/download', methods=['GET'])
def download():
  # get grid request parameter, convert to grid
  grid_s = request.args.get('grid', '')
  grid = sudoku.string_to_grid(grid_s)

  # build text file name and body
  name = file_name(grid_s)
  body = sudoku.grid_to_string(grid)

  # download text file
  return (body, {
    'content-disposition': f'attachment; filename="{name}"',
    'content-type': 'text/plain',
    'content-length': str(len(body)),
  })
