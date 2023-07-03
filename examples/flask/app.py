#
# app.py: Web frontend sudoku solver.
#
# Usage:
#
#   cd examples/flask/
#   pipenv run flask run
#
# Then connect to http://localhost:5000/
#

import json, os, sys, time
from flask import Flask, abort, request, render_template

# prepend top-level directory to module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import sudoku

app = Flask(__name__)

@app.route("/")
def home():
  return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
  # decode json body
  data = json.loads(request.data)

  # check for required keys
  for key in ['grid']:
    if key not in data:
      app.logger.error('missing property: %s' % (key))
      abort(400)

  # parse string as grid
  grid = sudoku.string_to_grid(data['grid'])
  app.logger.info('grid: %s' % (grid))

  # find solution, time solve()
  t0 = time.time_ns()
  solution = sudoku.solve(grid)
  t1 = time.time_ns()

  return {
    'time_ns': t1 - t0,
    'solution': ''.join([str(d) for d in solution]) if solution else '',
  }
