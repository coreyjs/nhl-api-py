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


### Stats Endpoints (In development)

```python

client.club_stats_season(team_abbr="BUF") # kinda weird endpoint.

client.player_career_stats(player_id=8478402)

# Team Summary Stats.
# These have lots of available parameters.  You can also tap into the apache cayenne expressions to build custom
# queries, if you have that knowledge.
client.stats.team_summary(start_season="20202021", end_season="20212022", game_type_id=2)
client.stats.team_summary(start_season="20202021", end_season="20212022")

###
# Skater Summary Stats.
# Queries for skaters for year ranges, filterable down by franchise.
client.stats.skater_stats_summary(start_season="20232024", end_season="20232024")
client.stats.skater_stats_summary(franchise_id=10, start_season="20232024", end_season="20232024")

 # skater_stats_summary_by_expression is more advanced method.  It allows for more direct manipulation of the query and
 # the cayenne expression clauses.
 sort_expr = [
                {"property": "points", "direction": "DESC"},
                {"property": "gamesPlayed", "direction": "ASC"},
                {"property": "playerId", "direction": "ASC"},
            ]
expr = "gameTypeId=2 and seasonId<=20232024 and seasonId>=20222023"
client.stats.skater_stats_summary_by_expression(default_cayenne_exp=expr, sort_expr=sort_expr)

###

```


### Schedule Endpoints

```python
client.schedule.get_schedule(date="2021-01-13")
client.schedule.get_schedule()

client.schedule.get_schedule_by_team_by_month(team_abbr="BUF")
client.schedule.get_schedule_by_team_by_month(team_abbr="BUF", month="2021-01")

client.schedule.get_schedule_by_team_by_week(team_abbr="BUF")
client.schedule.get_schedule_by_team_by_week(team_abbr="BUF", date="2024-01-01")

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


### Misc Endpoints
```python
client.misc.glossary()

client.misc.config()

client.misc.countries()

client.misc.season_specific_rules_and_info()

client.misc.draft_year_and_rounds()
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