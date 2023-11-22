[![PyPI version](https://badge.fury.io/py/nhl-api-py.svg)](https://badge.fury.io/py/nhl-api-py)
![nhl-api-py workflow](https://github.com/coreyjs/nhl-api-py/actions/workflows/python-app.yml/badge.svg?branch=main)

# NHL-API-PY


## This is being updated with the new, also undocumented, NHL API.  

More endpoints will be flushed out and completed as they
are discovered. If you find any, please submit a PR.


## About

NHL-api-py is a Python package that provides a simple wrapper around the 
NHL API, allowing you to easily access and retrieve NHL data in your Python 
applications.

Note: This is very early, I created this to help me with some machine learning
projects around the NHL and the NHL data sets.  Special thanks to https://github.com/erunion/sport-api-specifications/tree/master/nhl and https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md.


## Usage
```python
from nhlpy import NHLClient

client = NHLClient()
# OR
client = NHLClient(verbose=True) # a tad more logging such as the URL being called
```


### Schedule Endpoints

```python
client.schedule.get_schedule(date="2021-01-13")
client.schedule.get_schedule()

client.schedule.get_schedule_by_team_by_month(team_abbr="BUF")
client.schedule.get_schedule_by_team_by_month(team_abbr="BUF", month="2021-01")

client.schedule.get_schedule_by_team_by_week(team_abbr="BUF")

client.schedule.get_season_schedule(team_abbr="BUF", season="20212022")

client.schedule.schedule_calendar(date="2023-11-23")
```

### Standings Endpoints

```python
client.standings.get_standings()
client.standings.get_standings(date="2021-01-13")
client.standings.get_standings(season="202222023")

# standings manifest.  This returns a ton of information for every season ever it seems like
# This calls the API for this info, I also cache this in /data/seasonal_information_manifest.json
# for less API calls since this only changes yearly.
client.standings.season_standing_manifest()
```

### Teams Endpoints

```python
client.teams.teams_info() # returns id + abbrevation + name of all teams

client.teams.team_stats_summary(lang="en") # I honestly dont know. This is missing teams and has teams long abandoned.
```


### Game Center
```python
client.game_center.boxscore(game_id="2023020280")

client.game_center.play_by_play(game_id="2023020280")

client.game_center.landing(game_id="2023020280")

client.game_center.score_now()
```


---
### Insomnia Rest Client Export

[Insomnia Rest Client](https://insomnia.rest) is a great tool for testing

nhl_api-{ver}.json in the root folder is an export of the endpoints I have
been working through using the Insomnia Rest Client.  You can import this directly
into the client and use it to test the endpoints.  I will be updating this as I go


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