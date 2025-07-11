[![PyPI version](https://badge.fury.io/py/nhl-api-py.svg)](https://badge.fury.io/py/nhl-api-py)
![nhl-api-py workflow](https://github.com/coreyjs/nhl-api-py/actions/workflows/python-app.yml/badge.svg?branch=main)

# NHL API & NHL Edge Stats

## Table of Contents
- [About](#about)
- [Installation & Quick Start](#installation--quick-start)
- [Configuration](#configuration)
- [API Modules](#api-modules)
  - [Teams](#teams)
  - [Schedule](#schedule)
  - [Stats](#stats)
  - [Standings](#standings)
  - [Game Center](#game-center)
  - [Misc](#misc)
- [Advanced Usage](#advanced-usage)
  - [Query Builder](#stats-with-querybuilder)
- [Examples & Wiki](#examples--wiki)
- [Development](#developers)
- [Contact](#contact)

## About

NHL-api-py is a Python package that provides a simple wrapper around the 
NHL API, allowing you to easily access and retrieve NHL data in your Python 
applications.

Note: I created this to help me with some machine learning
projects around the NHL and the NHL data sets.  Special thanks to https://github.com/erunion/sport-api-specifications/tree/master/nhl,
https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md and https://github.com/Zmalski/NHL-API-Reference.

### Developer Note: This is being updated with the new, also undocumented, NHL API.  

This started as a project around the old NHL API, that got deprecated in 2023(?). This project has evolved 
to adopt the new NHL API(s) which are undocumented but discoverable via the NHL platforms.  Some endpoints
are still being added, and some are still being discovered.  The goal is to have a complete wrapper around the NHL API.

If you find any, open a ticket or post in the discussions tab.   I would love to hear more.

## Installation & Quick Start

```bash
pip install nhl-api-py
```

```python
from nhlpy import NHLClient

# Basic usage
client = NHLClient()

# Get all teams
teams = client.teams.teams()

# Get current standings
standings = client.standings.league_standings()

# Get today's games
games = client.schedule.daily_schedule()
```

## Configuration

```python
from nhlpy import NHLClient

# Default configuration
client = NHLClient()

# With debug logging
client = NHLClient(debug=True)

# All available configurations
client = NHLClient(
    debug=True,           # Enable debug logging
    timeout=30,           # Request timeout in seconds
    ssl_verify=True,      # SSL certificate verification
    follow_redirects=True # Follow HTTP redirects
)
```

## Examples & Wiki
*These need to updated with `v3` updates*

More in depth examples can be found in the wiki, feel free to add more: [Examples](https://github.com/coreyjs/nhl-api-py/wiki/Example-Use-Cases)

## Contact

Im available on [Bluesky](https://bsky.app/profile/coreyjs.dev) or the [twit](https://x.com/corey_builds) for any questions or just general chats about enhancements.

## API Modules

This project is organized into several sub modules, each representing a different endpoint of the NHL API.  
They are grouped by function to make the library easier to navigate and use.  The main modules are:

- **`teams`**: Contains endpoints related to NHL teams, including team information and rosters. You can find team_id(s) here along with franchise_id(s) needed for some of the stats queries.
- **`schedule`**: Contains endpoints related to the NHL schedule, including game dates, weekly schedules, and team schedules.
- **`stats`**: Contains endpoints related to player and team statistics. This will have your basic stats, summary stats and more advanced stats using the new query builder, which allows for more complex queries to be built up programmatically.
- **`standings`**: Contains endpoints related to NHL standings, including current standings and historical standings.
- **`game_center`**: Contains endpoints related to game center data, including box scores, play-by-play data, and game summaries.
- **`misc`**: Contains miscellaneous endpoints that don't fit into the other categories, such as glossary terms, configuration data, and country information.

### Helpers Module
- **`helpers`**: Contains helper functions and utilities for working with the NHL API, such as getting game IDs by season or calculating player statistics. These are experimental and often times make many requests, can return DataFrames or do calculations. Stuff I find myself doing over and over I tend to move into helpers for convenience. They are often cross domain, involve many sub requests, may integrate more machine learning techniques, or just make it easier to get the data you want. These will have built in sleeping to avoid hitting the API too hard, but you can override this by setting the `sleep` parameter to `False` in the function call.


Do you have a specific use case or cool code snippet you use over and over?  If its helpful to others please open a PR and add a helper.
# Teams

Get information about NHL teams, rosters, and franchises.

## Get All Teams
```python
# Get current teams
teams = client.teams.teams()

# Get teams from a specific date
teams = client.teams.teams(data="2024-10-04")
```

## Get Team Roster
```python
# Get current season roster
roster = client.teams.team_roster(team_abbr="BUF", season="20242025")
```

## Get Franchise Information
```python
# Get all franchises (current and historical)
franchises = client.teams.franchises()
```

### Example: Finding Team Information
```python
from nhlpy import NHLClient

client = NHLClient()

# Get all current teams
teams = client.teams.teams()

# Find a specific team
for team in teams:
    if team['abbr'] == 'TOR':
        print(f"Team: {team['name']}")
        print(f"Division: {team['division']['name']}")
        print(f"Franchise ID: {team['franchise_id']}")
        break

# Get that team's roster
roster = client.teams.team_roster(team_abbr="TOR", season="20242025")
print(f"Forwards: {len(roster['forwards'])}")
print(f"Defensemen: {len(roster['defensemen'])}")
print(f"Goalies: {len(roster['goalies'])}")
```

<details>
<summary>📋 Full Response Examples</summary>

**teams() response:**
```json

```

**team_roster() response:**
```json

```

**franchises() response:**
```json

```
</details>

# Schedule

Get NHL game schedules - daily, weekly, or team-specific schedules.

## Get Daily Schedule
```python
# Get today's games
games = client.schedule.daily_schedule()

# Get games for a specific date
games = client.schedule.daily_schedule(date="2024-01-01")
```

## Get Weekly Schedule
```python
# Get this week's games
week_games = client.schedule.weekly_schedule()

# Get games for a specific week
week_games = client.schedule.weekly_schedule(date="2024-01-01")
```

## Get Team Schedule
```python
# Get team's games for a specific month
team_schedule = client.schedule.team_monthly_schedule(team_abbr="BUF", month="2024-10")
```

## Get Team Weekly Schedule
```python
# Defaults to 'now'
weekly_schedule = client.schedule.team_weekly_schedule(team_abbr="BUF")

weekly_schedule = client.schedule.team_weekly_schedule(team_abbr="BUF", date="2024-01-01")
```

## Get Team Season Schedule
```python
full_schedule = client.schedule.team_season_schedule(team_abbr="BUF", season="20242025")
```

## Get Calendar Schedule
*Note: This is an endpoint available from the NHL but why it exists is a different story.  
I seems to return the same data as the above endpoints*

```python
cal = client.schedule.calendar_schedule(date="2024-01-01")
```

## Playoff Schedule
```python
games = client.schedule.playoff_carousel(season="20242025")
```

## Playoff Schedule by Series
```python
series = client.schedule.playoff_series_schedule(season="20242025",  series="a")
```

## Playoff Bracket
```python
bracket = client.schedule.playoff_bracket(year="2024")
```

### Example: Finding Tonight's Games
```python
from nhlpy import NHLClient

client = NHLClient()

# Get games by date.  Leave date blank to get today's games
games = client.schedule.daily_schedule(date="2024-10-08")

# Show what's on tonight
for game in games.get('games', []):
    away_team = game['awayTeam']['abbrev']
    home_team = game['homeTeam']['abbrev']
    game_time = game['startTimeUTC']
    print(f"{away_team} @ {home_team} - {game_time}")
```

<details>
<summary>📋 Full Response Examples</summary>

**daily_schedule() response:**
```json

```
</details>



# Stats

Get player and team statistics - from basic season stats to advanced analytics.

## Get Player Career Stats
```python
# Get a player's full career statistics
career_stats = client.stats.player_career_stats(player_id="8478402")  # Connor McDavid
```

## Get Player Game Log
```python
# Get game-by-game stats for a player
game_log = client.stats.player_game_log(
    player_id="8478402", 
    season_id="20232024", 
    game_type=2  # Regular season
)
```

## Get Team Statistics
```python
# Get team stats for a season
team_stats = client.stats.team_summary(
    start_season="20232024", 
    end_season="20232024"
)
```

## Get Skater Statistics
```python
# Get basic skater stats
skater_stats = client.stats.skater_stats_summary(
    start_season="20232024", 
    end_season="20232024"
)

# Filter by franchise (team)
skater_stats = client.stats.skater_stats_summary(
    start_season="20232024", 
    end_season="20232024",
    franchise_id="10"  # Toronto Maple Leafs
)
```

## Get Advanced Skater Statistics
See [Query Builder](#stats-with-querybuilder) for more advanced queries.



## Get Goalie Statistics
```python
# Get basic goalie stats
goalie_stats = client.stats.goalie_stats_summary(
    start_season="20232024", 
    end_season="20232024"
)

# Get advanced goalie stats
goalie_stats = client.stats.goalie_stats_summary(
    start_season="20232024",
    end_season="20232024",
    stats_type="advanced"
)
```

### Example: Finding Top Scorers
```python
from nhlpy import NHLClient

client = NHLClient()

# Get current season skater stats
stats = client.stats.skater_stats_summary(
    start_season="20242025", 
    end_season="20242025"
)

# Show top 5 scorers
for i, player in enumerate(stats[:5]):
    print(f"{i+1}. {player['skaterFullName']}: {player['points']} points")
```

<details>
<summary>📋 Full Response Examples</summary>

**player_career_stats() response:**
```json

```

**skater_stats_summary_simple() response:**
```json

```
</details>

# Standings

Get current league standings or standings from any point in NHL history.

## Get Current Standings
```python
# Get current league standings
standings = client.standings.league_standings()
```

## Get Historical Standings
```python
# Get standings from a specific date
standings = client.standings.league_standings(date="2024-01-01")

# Get final standings for a completed season
standings = client.standings.league_standings(season="20232024")
```

## Get Season Information
```python
# Get metadata about seasons (dates, rules, etc.)
season_info = client.standings.season_standing_manifest()
```

### Example: Finding Division Leaders
```python
from nhlpy import NHLClient

client = NHLClient()

# Get current standings
standings = client.standings.league_standings()

# Find division leaders
divisions = {}
for team in standings['standings']:
    division = team['divisionName']
    if division not in divisions:
        divisions[division] = team
    elif team['points'] > divisions[division]['points']:
        divisions[division] = team

# Display division leaders
for division, team in divisions.items():
    print(f"{division}: {team['teamName']['default']} ({team['points']} pts)")
```

<details>
<summary>📋 Full Response Examples</summary>

**league_standings() response:**
```json

```
</details>

# Game Center

Get detailed game data - boxscores, play-by-play, and live game information.

## Get Game Boxscore
```python
# Get complete boxscore for a game
boxscore = client.game_center.boxscore(game_id="2023020280")
```

## Get Play-by-Play
```python
# Get detailed play-by-play data
play_by_play = client.game_center.play_by_play(game_id="2023020280")
```

## Get Game Overview
```python
# Get game matchup info and key stats
game_info = client.game_center.match_up(game_id="2023020280")
```

## Get Game Scores
```python
# Get today's scores
scores = client.game_center.daily_scores()

# Get scores for a specific date
scores = client.game_center.daily_scores(date="2024-01-01")
```

## Get Advanced Game Data
```python
# Get shift chart data
shifts = client.game_center.shift_chart_data(game_id="2023020280")

# Get additional game stats
stats = client.game_center.season_series_matchup(game_id="2023020280")

# Get game story/recap
story = client.game_center.game_story(game_id="2023020280")
```

### Example: Game Analysis
```python
from nhlpy import NHLClient

client = NHLClient()

# Get a game's complete data
game_id = "2023020280"
boxscore = client.game_center.boxscore(game_id)
play_by_play = client.game_center.play_by_play(game_id)

# Analyze the game
away_team = boxscore['awayTeam']['abbrev']
home_team = boxscore['homeTeam']['abbrev']
away_score = boxscore['awayTeam']['score']
home_score = boxscore['homeTeam']['score']

print(f"Final: {away_team} {away_score} - {home_team} {home_score}")

# Count shots by period
shots_by_period = {}
for play in play_by_play.get('plays', []):
    if play['typeDescKey'] == 'shot-on-goal':
        period = play['periodDescriptor'].get('number', 'Unknown')
        if period not in shots_by_period:
            shots_by_period[period] = 0
        shots_by_period[period] += 1

for period, shots in shots_by_period.items():
    print(f"Period {period}: {shots} shots")
```

<details>
<summary>📋 Full Response Examples</summary>

**boxscore() response:**
```json

```

**play_by_play() response:**
```json

```
</details>

# Misc

Utility endpoints for NHL reference data and configuration information.

## Get NHL Glossary
```python
# Get definitions of NHL terms and statistics
glossary = client.misc.glossary()
```

## Get API Configuration
```python
# Get available filter options and API configuration
config = client.misc.config()
```

## Get Country Data
```python
# Get list of countries in NHL data
countries = client.misc.countries()
```

## Get Season Information
```python
# Get season-specific rules and information
season_info = client.misc.season_specific_rules_and_info()
```

## Get Draft Information
```python
# Get draft years and round information
draft_info = client.misc.draft_year_and_rounds()
```

### Example: Understanding NHL Terms
```python
from nhlpy import NHLClient

client = NHLClient()

# Get NHL glossary
glossary = client.misc.glossary()

# Find specific stats definitions
stat_terms = ["BENCH", "BKS", "A", "ENA", "EV GA"]
for term in stat_terms:
    for entry in glossary:
        if entry['abbreviation'].upper() == term:
            print(f"{term}: {entry['definition']}")
            continue
```

<details>
<summary>📋 Full Response Examples</summary>

**glossary() response:**
```json

```

**countries() response:**
```json

```
</details>

---
# Advanced Usage

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
    StatusQuery(is_active=True),#for active players OR for HOF players StatusQuery(is_hall_of_fame=True),
    OpponentQuery(opponent_franchise_id="2"),
    ExperienceQuery(is_rookie=True), # for rookies || ExperienceQuery(is_rookie=False) #for veteran
    DecisionQuery(decision="W") # OR DecisionQuery(decision="L") OR DecisionQuery(decision="O")
]
```


### Example

#### The Story:
Show me all players, during the regular season (`game_type=2`), that were drafted in 2020 (`DraftQuery`)
 for the 2020-2021 season through 2023-2024 season (`SeasonQuery`) that play forward: LW, C, RW (`PositionQuery`). Use 
`summary` statistics and aggregate (`aggregate=True`) all the years together.

```python
from nhlpy.api.query.builder import QueryBuilder, QueryContext
from nhlpy.nhl_client import NHLClient
from nhlpy.api.query.filters.draft import DraftQuery
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.game_type import GameTypeQuery
from nhlpy.api.query.filters.position import PositionQuery, PositionTypes

client = NHLClient(debug=True)

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


### pypi test net
```
poetry build
poetry publish -r test-pypi
```


#### Poetry version management
```
# View current version
poetry version

# Bump version
poetry version patch  # 0.1.0 -> 0.1.1
poetry version minor  # 0.1.0 -> 0.2.0
poetry version major  # 0.1.0 -> 1.0.0

# Set specific version
poetry version 2.0.0

# Set pre-release versions
poetry version prepatch  # 0.1.0 -> 0.1.1-alpha.0
poetry version preminor  # 0.1.0 -> 0.2.0-alpha.0
poetry version premajor  # 0.1.0 -> 1.0.0-alpha.0

# Specify pre-release identifier
poetry version prerelease  # 0.1.0 -> 0.1.0-alpha.0
poetry version prerelease beta  # 0.1.0-alpha.0 -> 0.1.0-beta.0
```
