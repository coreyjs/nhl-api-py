[![PyPI version](https://badge.fury.io/py/nhl-api-py.svg)](https://badge.fury.io/py/nhl-api-py)

# NHL-py-api

NHL-py-api is a Python package that provides a simple wrapper around the 
NHL API, allowing you to easily access and retrieve NHL data in your Python 
applications.

Note: This is very early, I created this to help me with some machine learning
projects around the NHL and the NHL data sets.  Special thanks to https://github.com/erunion/sport-api-specifications/tree/master/nhl and https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md.

### Example Notebook:
An example Collab notebook can be found [here at coreyjs/nhl-api-py-examples](https://github.com/coreyjs/nhl-api-py-examples).


## Installation

You can install NHL-py-api using pip:

```shell
pip install nhl-api-py
```

- - -
## Usage

```python
from nhlpy import NHLClient

client = NHLClient()
```

Available methods:
```python
client.teams.all()
client.teams.get_by_id(id=1, roster=False)
client.teams.get_team_next_game(id=1)
client.teams.get_team_previous_game(id=1)
client.teams.get_team_stats(id=1)

# Standings
client.standings.get_standings(season="20222023", detailed_record=False)
client.standings.get_standing_types()

# Player Stats
client.players.get_player_stats(person_id=8477949, season="20222023", stat_type="statsSingleSeason")
client.players.get_player_stats(person_id=8477949, season="20222023", stat_type="goalsByGameSituation")
client.players.get_player_stats(person_id=8477949, season="20222023", stat_type="yearByYear")

```

- - - 

As mentioned at the top, I created a notebook to go over some of the available methods in more detail.  Below is an export md of that notebook, with out cell executions.

```python
pip install nhl-api-py
```


```python
from nhlpy import NHLClient
```

### Getting Started - Create the NHLClient


```python
client = NHLClient()
```

### Team APIs


```python
teams = client.teams.all()
teams
```


```python
buffalo = client.teams.get_by_id(id=7)
buffalo
```


```python
next_buffalo_game = client.teams.get_team_next_game(id=7)
next_buffalo_game
```


```python
prev_buffalo_game = client.teams.get_team_previous_game(id=7)
prev_buffalo_game
```


```python
buffalo_with_stats = client.teams.get_team_with_stats(id=7)
buffalo_with_stats
```


```python
buffalo_roster = client.teams.get_team_roster(id=7)
buffalo_roster
```


```python
buffalo_full_team_stats = client.teams.get_team_stats(id=7)
buffalo_full_team_stats
```

### Standing APIs


```python
# These can be used in conjunction with get_standings_by_standing_type
all_standing_types = client.standings.get_standing_types()
all_standing_types
```


```python
# standings by season
all_standings = client.standings.get_standings(season="20222023", detailed_record=False)
all_standings
```


```python
# same as above but with more detailed information
# standings by season
all_standings = client.standings.get_standings(season="20222023", detailed_record=True)
all_standings
```


```python
# Get standings by type, types can be found via get_standings_by_type, or in the docstring
post_season = client.standings.get_standings_by_standing_type(standing_type="regularSeason")
post_season
```


```python

```

### Players


```python
# APIs to access player information.  Requires person_id, found from `teams.get_team_roster()`
jj = client.players.get_player(person_id=8482175)
jj
```


```python
jj_stats = client.players.get_player_stats(person_id=8482175, season="20222023", stat_type="statsSingleSeason")
jj_stats
```


```python
# Differnt stat types you can access
types = client.players.get_player_stat_types()
types
```


```python

```


- - - 


### Developers

`poetry install --with dev`
