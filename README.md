[![PyPI version](https://badge.fury.io/py/nhl-api-py.svg)](https://badge.fury.io/py/nhl-api-py)
![nhl-api-py workflow](https://github.com/coreyjs/nhl-api-py/actions/workflows/python-app.yml/badge.svg?branch=main)

# NHL-API-PY


## This is being updated with the new, also undocumented, NHL API.  

More endpoints will be flushed out and completed as they
are discovered. If you find any, please submit a PR.


NHL-api-py is a Python package that provides a simple wrapper around the 
NHL API, allowing you to easily access and retrieve NHL data in your Python 
applications.

Note: This is very early, I created this to help me with some machine learning
projects around the NHL and the NHL data sets.  Special thanks to https://github.com/erunion/sport-api-specifications/tree/master/nhl and https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md.



- - - 


### Developers

1) Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

`curl -sSL https://install.python-poetry.org | python3 -`

or using pipx

`pipx install poetry`


2) `poetry install --with dev`

3) `poetry shell`

```python

$ poetry shell

# You can then run the following
$ pytest
$ ruff .
$ black .

```