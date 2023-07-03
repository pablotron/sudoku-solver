# Sudoku Solver

[Sudoku][] puzzle solver.  Uses [z3][] internally.

## Usage

Use [Pipenv][] to install dependencies and run `examples/solve.py`.

Example:

    > pipenv install
    Installing dependencies from Pipfile.lock (3bdc73)...
    To activate this project's virtualenv, run pipenv shell.
    Alternatively, run a command inside the virtualenv with pipenv run.
    > pipenv run examples/solve.py
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

The built-in API documentation via [pydoc][]:

    > pipenv run python -m pydoc sudoku
    ...

## Tests

Install development dependencies, then use [pytest][] to run the test
suite.

Example:

    > pipenv install --dev && pipenv run pytest -q
    Installing dependencies from Pipfile.lock (3bdc73)...
    Installing dependencies from Pipfile.lock (3bdc73)...
    To activate this project's virtualenv, run pipenv shell.
    Alternatively, run a command inside the virtualenv with pipenv run.
    ....... [100%]
    7 passed in 4.16s

Run [pylint][] from the top-level directory to lint the `sudoku` module:

    pipenv run pylint sudoku.py

[sudoku]: https://en.wikipedia.org/wiki/Sudoku
  "Number placement puzzle."
[z3]: https://github.com/Z3Prover/z3
  "Z3 constraint solver."
[pytest]: https://pytest.org/
  "Python test framework."
[pipenv]: https://pipenv.pypa.io/en/latest/
  "Python development workflow management tool."
[pydoc]: https://docs.python.org/3/library/pydoc.html
  "Python documentation generator."
[pylint]: https://pypi.org/project/pylint/
  "Python static code analyzer."
