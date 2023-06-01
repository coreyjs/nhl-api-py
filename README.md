# NHL-py-api

NHL-py-api is a Python package that provides a simple wrapper around the 
NHL API, allowing you to easily access and retrieve NHL data in your Python 
applications.

Note: This is very early, I created this to help me with some machine learning
projects around the NHL and the NHL data sets.


## Installation

You can install NHL-py-api using pip:

```shell
pip install nhl-py-api
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
```

- - - 


### Developers

`poetry install --with dev`