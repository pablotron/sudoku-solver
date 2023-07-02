import hashlib
import hmac
from flask import Flask, abort, request
import math
import sudoku
import time
import os

API_KEY = os.environ['SUDOKU_API_KEY']
app = Flask(__name__)

@app.route("/")
def home():
  return "<p>Hello, World!</p>"

@app.route('/solve', methods=['POST'])
def solve():
  body = request.data
  got_mac = request.headers.get('x-hmac-sha256')
  if got_mac is None:
    abort(402) # fixme: correct error code

  # check mac
  exp_mac = hmac.HMAC(API_KEY.encode(), body, digestmod=hashlib.sha256).hexdigest()
  if got_mac != exp_mac:
    app.logger.error('hmac mismatch: got %s, exp %s' % (got_mac, exp_mac))
    abort(400) # fixme: correct error code

  # decode json body
  data = json.loads(body)

  # check for required keys
  for key in ['time', 'grid']:
    if key not in data:
      app.logger.error('missing property: %s' % (key))
      abort(400)

  # check timestamp
  got_time = data['time']
  exp_time = time.time()
  if math.abs(got_time - exp_time) > 30:
    app.logger.error('time mismatch: got %d, exp %d +/- 30' % (got_time, exp_time))
    abort(400)

  t0 = time.time_ns()
  solution = sudoku.solve(data['grid'])
  t1 = time.time_ns()

  return {
    'time': t1 - t0,
    'grid': solution,
  }

