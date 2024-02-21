[![PyPI version](https://badge.fury.io/py/nhl-api-py.svg)](https://badge.fury.io/py/nhl-api-py)
![nhl-api-py workflow](https://github.com/coreyjs/nhl-api-py/actions/workflows/python-app.yml/badge.svg?branch=main)

# NHL-API-PY


## About

NHL-api-py is a Python package that provides a simple wrapper around the 
NHL API, allowing you to easily access and retrieve NHL data in your Python 
applications.

Note: This is ~~very early~~ maturing, I created this to help me with some machine learning
projects around the NHL and the NHL data sets.  Special thanks to https://github.com/erunion/sport-api-specifications/tree/master/nhl and https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md.

### Developer Note: This is being updated with the new, also undocumented, NHL API.  

More endpoints will be flushed out and completed as they
are discovered. If you find any, open a ticket or post in the discussions tab.   I would love to hear more.


---
## Contact
Im available on [Bluesky](https://bsky.app/profile/coreyjs.dev) for any questions or just general chats about enhancements.

---



# Usage
```python
from nhlpy import NHLClient

client = NHLClient()
# Fore more verbose logging
client = NHLClient(verbose=True)
# OR Other available configurations:
client = NHLClient(verbose={bool}, timeout={int}, ssl_verify={bool}, follow_redirects={bool})
```
---
## Stats with QueryBuilder

The skater stats endpoint can be accessed using the new query builder.  It should make
creating and understanding the queries a bit easier.  Filters are being added as I go, and will match up
to what the NHL API will allow.

The idea is to easily, and programatically, build up more complex queries using the query filters.  A quick example below:
```python
filters = [
    GameTypeQuery(game_type="2"),
    DraftQuery(year="2020", draft_round="2"),
    SeasonQuery(season_start="20202021", season_end="20232024"),
    PositionQuery(position=PositionTypes.ALL_FORWARDS)
]
```



### Sorting
The sorting is a list of dictionaries similar to below.  You can supply your own, otherwise it will
default to the default sort properties that the stat dashboard uses.  All sorting defaults are found
in the `nhl-api-py/nhlpy/api/query/sorting/sorting_options.py` file.

<details>
<summary>Default Sorting</summary>

```python
skater_summary_default_sorting = [
    {"property": "points", "direction": "DESC"},
    {"property": "gamesPlayed", "direction": "ASC"},
    {"property": "playerId", "direction": "ASC"},
]
```
</details>

---

### Report Types
The following report types are available.  These are used to build the request url.  So `/summary`, `/bios`, etc.

```bash
summary
bios
faceoffpercentages
faceoffwins
goalsForAgainst
realtime
penalties
penaltykill
penaltyShots
powerplay
puckPossessions
summaryshooting
percentages
scoringRates
scoringpergame
shootout
shottype
timeonice
```

### Available Filters

```python
from nhlpy.api.query.filters.franchise import FranchiseQuery
from nhlpy.api.query.filters.shoot_catch import ShootCatchesQuery
from nhlpy.api.query.filters.draft import DraftQuery
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.game_type import GameTypeQuery
from nhlpy.api.query.filters.position import PositionQuery, PositionTypes
from nhlpy.api.query.filters.status import StatusQuery
from nhlpy.api.query.filters.opponent import OpponentQuery
from nhlpy.api.query.filters.home_road import HomeRoadQuery
from nhlpy.api.query.filters.experience import ExperienceQuery
from nhlpy.api.query.filters.decision import DecisionQuery

filters = [
    GameTypeQuery(game_type="2"),
    DraftQuery(year="2020", draft_round="2"),
    SeasonQuery(season_start="20202021", season_end="20232024"),
    PositionQuery(position=PositionTypes.ALL_FORWARDS),
    ShootCatchesQuery(shoot_catch="L"),
    HomeRoadQuery(home_road="H"),
    FranchiseQuery(franchise_id="1"),
    StatusQuery(is_active=True) #for active players OR for HOF players StatusQuery(is_hall_of_fame=True),
    OpponentQuery(opponent_franchise_id="2"),
    ExperienceQuery(is_rookie=True), # for rookies || ExperienceQuery(is_rookie=False) #for veteran
    DecisionQuery(decision="W") # OR DecisionQuery(decision="L") OR DecisionQuery(decision="O")
]
```


### Example
```python
from nhlpy.api.query.builder import QueryBuilder, QueryContext
from nhlpy.nhl_client import NHLClient
from nhlpy.api.query.filters.draft import DraftQuery
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.game_type import GameTypeQuery
from nhlpy.api.query.filters.position import PositionQuery, PositionTypes

client = NHLClient(verbose=True)

filters = [
    GameTypeQuery(game_type="2"),
    DraftQuery(year="2020", draft_round="2"),
    SeasonQuery(season_start="20202021", season_end="20232024"),
    PositionQuery(position=PositionTypes.ALL_FORWARDS)
]

query_builder = QueryBuilder()
query_context: QueryContext = query_builder.build(filters=filters)

data = client.stats.skater_stats_with_query_context(
    report_type='summary',
    query_context=query_context,
    aggregate=True
)
```

### Granular Filtering
Each API request uses an additional query parameter called `factCayenneExp`.  This defaults to `gamesPlayed>=1`
but can be overridden by setting the `fact_query` parameter in the `QueryContextObject` object.  These can
be combined together with `and` to create a more complex query.  It supports `>`, `<`, `>=`, `<=`.  For example: `shootingPct>=0.01 and timeOnIcePerGame>=60 and faceoffWinPct>=0.01 and shots>=1`


This should support the following filters:

- `gamesPlayed`
- `points`
- `goals`
- `pointsPerGame`
- `penaltyMinutes`
- `plusMinus`
- `ppGoals` # power play goals
- `evGoals` # even strength goals
- `pointsPerGame`
- `penaltyMinutes`
- `evPoints` # even strength points
- `ppPoints` # power play points
- `gameWinningGoals`
- `otGoals`
- `shPoints` # short handed points
- `shGoals` # short handed goals
- `shootingPct`
- `timeOnIcePerGame`
- `faceoffWinPct`
- `shots`

```python
.....
query_builder = QueryBuilder()
query_context: QueryContext = query_builder.build(filters=filters)

query_context.fact_query = "gamesPlayed>=1 and goals>=10"  # defaults to gamesPlayed>=1

data = client.stats.skater_stats_with_query_context(
    report_type='summary',
    query_context=query_context,
    aggregate=True
)
```


### Invalid Query / Errors

The `QueryContext` object will hold the result of the built query with the supplied queries.
In the event of an invalid query (bad data, wrong option, etc), the `QueryContext` object will
hold all the errors that were encountered during the build process.  This should help in debugging.

You can quickly check the `QueryContext` object for errors by calling `query_context.is_valid()`.  Any "invalid" filters
will be removed from the output query, but anything that is still valid will be included.

```python
...
query_context: QueryContext = query_builder.build(filters=filters)
query_context.is_valid() # False if any of the filters fails its validation check
query_context.errors
```

---

## Additional Stats Endpoints (In development)

```python

client.stats.club_stats_season(team_abbr="BUF") # kinda weird endpoint.

client.stats.player_career_stats(player_id="8478402")

# Team Summary Stats.
#   These have lots of available parameters.  You can also tap into the apache cayenne expressions to build custom
#   queries, if you have that knowledge.
client.stats.team_summary(start_season="20202021", end_season="20212022", game_type_id=2)
client.stats.team_summary(start_season="20202021", end_season="20212022")


# Skater Summary Stats.
#   Queries for skaters for year ranges, filterable down by franchise.
client.stats.skater_stats_summary(start_season="20232024", end_season="20232024")
client.stats.skater_stats_summary(franchise_id=10, start_season="20232024", end_season="20232024")
```
---


## Schedule Endpoints

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

---

## Standings Endpoints

```python
client.standings.get_standings()
client.standings.get_standings(date="2021-01-13")
client.standings.get_standings(season="202222023")

# standings manifest.  This returns a ton of information for every season ever it seems like
# This calls the API for this info, I also cache this in /data/seasonal_information_manifest.json
# for less API calls since this only changes yearly.
client.standings.season_standing_manifest()
```
---

## Teams Endpoints

```python
client.teams.teams_info() # returns id + abbrevation + name of all teams

client.teams.team_stats_summary(lang="en") # I honestly dont know. This is missing teams and has teams long abandoned.
```

---

## Game Center
```python
client.game_center.boxscore(game_id="2023020280")

client.game_center.play_by_play(game_id="2023020280")

client.game_center.landing(game_id="2023020280")

client.game_center.score_now()
```

---

## Misc Endpoints
```python
client.misc.glossary()

client.misc.config()

client.misc.countries()

client.misc.season_specific_rules_and_info()

client.misc.draft_year_and_rounds()
```

---
## Insomnia Rest Client Export

[Insomnia Rest Client](https://insomnia.rest) is a great tool for testing

nhl_api-{ver}.json in the root folder is an export of the endpoints I have
been working through using the Insomnia Rest Client.  You can import this directly
into the client and use it to test the endpoints.  I will be updating this as I go


- - - 


## Developers

1) Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

`curl -sSL https://install.python-poetry.org | python3 -`

or using pipx

`pipx install poetry`


2) `poetry install --with dev`

3) `poetry shell`


### Build Pipeline
The build pipeline will run `black`, `ruff`, and `pytest`.  Please make sure these are passing before submitting a PR.

```python

$ poetry shell

# You can then run the following
$ pytest
$ ruff .
$ black .

```
