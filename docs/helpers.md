# Helpers API Module

The helpers module provides convenience methods that aggregate data from multiple NHL API calls into single results. Access it via `client.helpers` on an `NHLClient` instance.

**Performance warning:** The season-wide methods (`game_ids_by_season`, `all_players`, `all_players_summary_statistics`) make multiple API calls internally (typically 32, one per NHL team) with built-in sleep delays between requests to avoid rate limiting. They are significantly slower than individual API calls. Expect execution times of 30 seconds to several minutes depending on the method and sleep rate. `game_goals` covers one game and makes 2 calls.

**Historical seasons:** The season-wide methods get their team list from `client.teams.teams()`, which returns the current teams. For a historical season it iterates today's teams, so relocated or defunct teams (for example the Quebec Nordiques in 1990-91) are missed. For a season-accurate team list, use `client.stats.team_summary()` for the season's team IDs and `client.teams.all_time_teams()` for their abbreviations and franchise IDs.

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

## Get Every Goal in a Game with game_goals

Returns every goal in one game, ready to plot: both teams, the scorer, assists and goalie by name, rink coordinates, the score after the goal, and who was on the ice. It joins the play-by-play feed with the shift chart, so it makes 2 API calls (about 400 KB). Unlike the season-wide helpers it covers one game and doesn't sleep between calls.

```python
from nhlpy import NHLClient

client = NHLClient()
game = client.helpers.game_goals(game_id="2024020500")

print(f"{game['away_team']['abbr']} @ {game['home_team']['abbr']}")
for goal in game["goals"]:
    scorer = goal["scorer"]
    on_ice = " ".join(f"{p['team_abbr']}#{p['sweater_number']}" for p in goal["on_ice"] or [])
    print(f"P{goal['period']} {goal['time_in_period']} {goal['team_abbr']} #{scorer['sweater_number']} {scorer['last_name']} | {on_ice}")
```

**Parameters:**

- `game_id` (str, required): 10-digit game ID (e.g., "2024020500"). Anything else raises `ValueError`.
- `include_on_ice` (bool, optional): Also fetch the shift chart to fill `on_ice`. Defaults to `True`. Pass `False` to make one API call instead of two.

**Returns:** `dict` with snake_case keys. Unlike the season-wide helpers, which return NHL fields as they come, this helper builds its own shape.

- `game_id` (int): Game ID
- `game_state` (str): `"FUT"`, `"LIVE"`, `"CRIT"`, `"OFF"` or `"FINAL"`. While a game is live, `goals` and `on_ice` can be incomplete.
- `home_team` / `away_team` (dict): `id` (int), `abbr` (str), `logo` (str), `dark_logo` (str)
- `goals` (list): One entry per goal, in game order. Shootout attempts are left out; they're in `client.game_center.play_by_play()` as plays with `periodDescriptor.periodType == "SO"`.

**Goal fields** (any value is `None` when the NHL feed leaves it out):

- `event_id` (int): Play-by-play `eventId`. Pass it to `client.misc.goal_replay()` for the NHL's official `strength` and `goalModifier` (e.g., `"empty-net"`, `"penalty-shot"`).
- `period` (int), `period_type` (str): Period number, and `"REG"` or `"OT"`. Check `period_type` rather than the number: playoff overtime can be period 5 or later.
- `time_in_period` (str): Time elapsed in the period, MM:SS
- `situation_code` (str): Four digits: away goalie (1 in net, 0 pulled), away skaters, home skaters, home goalie. `"1551"` is 5-on-5, `"1451"` a home power play, `"0651"` the away team with its goalie pulled, `"1331"` 3-on-3 overtime, `"1010"` or `"0101"` a penalty shot.
- `team_abbr` (str), `is_home` (bool): Scoring team, and whether it's the home team
- `home_team_defending_side` (str): `"left"` or `"right"`, the end the home team defends in this period
- `x`, `y` (int): Shot location in feet, with (0, 0) at center ice; `x` runs -100 to 100 and `y` -42.5 to 42.5. Teams switch ends each period (see below).
- `zone` (str): `"O"`, `"D"` or `"N"`, from the scoring team's point of view
- `shot_type` (str): e.g., `"wrist"`, `"snap"`, `"tip-in"`
- `scorer` (player): Goal scorer
- `assists` (list of player): 0 to 2 assisting players
- `goalie` (player): Goalie scored on. `None` for an empty-net goal.
- `away_score`, `home_score` (int): Score after the goal
- `highlight_clip_url` (str): Public video of the goal. `None` for older games.
- `ppt_replay_url` (str): The NHL's puck and player tracking file for the goal, 2023-24 onward (`None` before). The NHL only serves these files to nhl.com, so nhlpy doesn't download them.
- `on_ice` (list of player): Skaters and goalies on the ice for the goal, sorted by team, then position. `None` when `include_on_ice=False` or the shift chart has no data for that period yet (common while a game is live).

**Player fields** (shared by `scorer`, `assists`, `goalie` and `on_ice`):

- `player_id` (int): NHL player ID
- `first_name`, `last_name` (str)
- `sweater_number` (int)
- `position` (str): `"C"`, `"L"`, `"R"`, `"D"` or `"G"`
- `team_abbr` (str)
- `headshot` (str): Headshot image URL

A player missing from the game's roster still gets a record with `player_id`. The other fields are `None`, except in `on_ice`, where the name and team come from the shift chart.

**How `on_ice` is worked out:** a player counts as on the ice if their shift started before the goal and ended at or after it. A shift that starts at the goal second is for the faceoff after the goal. For a penalty-shot goal the shift chart still lists the full lines, so `on_ice` shows them rather than just the shooter and goalie.

### Draw every goal toward the same end

Teams switch ends each period. To plot every goal attacking the right end, rotate the ones that attack left:

```python
for goal in game["goals"]:
    if goal["x"] is None:
        continue
    attacks_right = (goal["home_team_defending_side"] == "left") == goal["is_home"]
    x, y = (goal["x"], goal["y"]) if attacks_right else (-goal["x"], -goal["y"])
```

### Get the plays before a goal

`game_goals` doesn't include the build-up to a goal. The play-by-play has it: walk back from the goal to the last faceoff in the same period.

```python
plays = client.game_center.play_by_play(game_id="2024020500")["plays"]
for i, play in enumerate(plays):
    if play["typeDescKey"] != "goal":
        continue
    start = i
    while start > 0 and plays[start - 1]["periodDescriptor"]["number"] == play["periodDescriptor"]["number"]:
        start -= 1
        if plays[start]["typeDescKey"] == "faceoff":
            break
    build_up = plays[start:i]  # faceoff, shots, hits, giveaways... with details.xCoord / details.yCoord
```

### Every goal in a season

`game_goals` fetches one game per call, so pace any loop yourself. A regular season is about 1,300 games: roughly 2,600 requests and 0.5 GB of downloads. `game_ids_by_season` can return the same game ID twice, so dedupe first:

```python
import time

game_ids = sorted(set(client.helpers.game_ids_by_season(season="20242025", game_types=[2])))
games = []
for game_id in game_ids:
    games.append(client.helpers.game_goals(game_id=str(game_id)))
    time.sleep(1)
```
