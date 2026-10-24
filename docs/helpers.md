# Helpers API Module

The helpers module provides convenience methods that aggregate data from multiple NHL API calls into single results. Access it via `client.helpers` on an `NHLClient` instance.

**Performance warning:** Every method in this module makes multiple API calls internally (typically 32, one per NHL team) with built-in sleep delays between requests to avoid rate limiting. These methods are significantly slower than individual API calls. Expect execution times of 30 seconds to several minutes depending on the method and sleep rate.

**Historical seasons:** Every method in this module gets its team list from `client.teams.teams()`, which returns the current teams. For a historical season it iterates today's teams, so relocated or defunct teams (for example the Quebec Nordiques in 1990-91) are missed. For a season-accurate team list, use `client.stats.team_summary()` for the season's team IDs and `client.teams.all_time_teams()` for their abbreviations and franchise IDs.

## Get All Game IDs for a Season with game_ids_by_season

Retrieves all unique game IDs for an entire NHL season by iterating through each team's schedule. Makes 32 API calls (one per team) with a configurable sleep delay between each call. Returns approximately 2600 unique game IDs for a standard regular season.

```python
from nhlpy import NHLClient

client = NHLClient()

# Get all regular season game IDs (default)
game_ids = client.helpers.game_ids_by_season(season="20242025")
print(f"Total games: {len(game_ids)}")

# Get playoff game IDs only
playoff_ids = client.helpers.game_ids_by_season(
    season="20242025",
    game_types=[3]
)

# Get both regular season and playoff game IDs
all_ids = client.helpers.game_ids_by_season(
    season="20242025",
    game_types=[2, 3],
    api_sleep_rate=1.5
)
```

**Parameters:**

- `season` (str, required): Season in YYYYYYYY format (e.g., "20242025")
- `game_types` (List[int], optional): List of game types to include. Defaults to `[2]` (regular season only).
  - `1`: Preseason
  - `2`: Regular season
  - `3`: Playoffs
- `api_sleep_rate` (float, optional): Seconds to sleep between API calls. Defaults to `1`. Increase if you encounter rate limiting.

**Returns:** `List[int]` of unique game IDs. Each game ID is an integer (e.g., 2024020001).

**Performance note:** With the default 1-second sleep rate, this method takes at least 32 seconds to complete. The method deduplicates game IDs since games appear in both teams' schedules.

## Get All Players Across All Teams with all_players

Retrieves every player from every team's roster for a given season. Makes 32 API calls (one per team) and returns a single flattened list of all player dictionaries with an added `team` field.

```python
from nhlpy import NHLClient

client = NHLClient()
players = client.helpers.all_players(season="20242025")

print(f"Total players: {len(players)}")
for player in players:
    print(f"{player['firstName']} {player['lastName']} - {player['team']}")
```

**Parameters:**

- `season` (str, required): Season in YYYYYYYY format (e.g., "20242025")
- `api_sleep_rate` (float, optional): Seconds to sleep between API calls. Defaults to `0.5`. Increase if you encounter rate limiting.

**Returns:** `List[dict]` of player objects from all 32 teams combined.

**Player fields:**

- `id` (int): Unique NHL player identifier
- `headshot` (str): URL to the player's headshot image
- `firstName` (str): Player's first name (cleaned from the nested `firstName.default` format)
- `lastName` (str): Player's last name (cleaned from the nested `lastName.default` format)
- `sweaterNumber` (int): Jersey number
- `positionCode` (str): Position code (e.g., "C", "L", "R", "D", "G")
- `shootsCatches` (str): Handedness ("L" or "R")
- `heightInInches` (int): Height in inches
- `weightInPounds` (int): Weight in pounds
- `birthDate` (str): Date of birth in "YYYY-MM-DD" format
- `birthCity` (object):
  - `default` (str): City of birth
- `birthCountry` (str): Three-letter country code (e.g., "CAN", "USA")
- `team` (str): Three-letter team abbreviation (added by the helper method)

**Performance note:** With the default 0.5-second sleep rate, this method takes at least 16 seconds to complete. A progress message is printed to stdout when the method starts.

## Get Summary Statistics for All Players with all_players_summary_statistics

Retrieves summary statistics for every skater in a given season by first fetching all players, then querying stats for each team using the query builder. Makes multiple rounds of API calls (32 for rosters plus 32 for stats) and merges the results.

```python
from nhlpy import NHLClient

client = NHLClient()
stats = client.helpers.all_players_summary_statistics(season="20242025")

for player in stats:
    name = player.get("skaterFullName", f"{player.get('firstName', '')} {player.get('lastName', '')}")
    points = player.get("points", 0)
    print(f"{name}: {points} pts")
```

**Parameters:**

- `season` (str, required): Season in YYYYYYYY format (e.g., "20242025")
- `api_sleep_rate` (float, optional): Seconds to sleep between API calls. Defaults to `1`. Increase if you encounter rate limiting.

**Returns:** `list` of merged player/stats dictionaries. Each entry combines roster data (from `all_players`) with summary statistics (from the stats query builder). Players without matching stats are included from the stats data alone.

**Merged fields include all fields from `all_players` above, plus stats fields such as:**

- `playerId` (int): Player ID from the stats response
- `skaterFullName` (str): Full name from the stats response
- `gamesPlayed` (int): Number of games played
- `goals` (int): Goals scored
- `assists` (int): Assists recorded
- `points` (int): Total points
- `plusMinus` (int): Plus/minus rating
- `penaltyMinutes` (int): Penalty minutes
- `shots` (int): Shots on goal
- `timeOnIcePerGame` (float): Average time on ice per game
- Additional summary stat columns depending on the report type

**Performance note:** This is the slowest helper method. With the default 1-second sleep rate, expect a minimum of 64 seconds (32 roster calls + 32 stats calls). A logging warning is emitted when the method starts. Increase `api_sleep_rate` if you encounter rate limiting.
