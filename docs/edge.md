# Edge API Module (NHL EDGE Tracking)

The edge module provides access to NHL EDGE puck and player tracking data, including shot speed, skating speed, distance skated, zone time, and shot location analytics for skaters, goalies, and teams. Access it via `client.edge` on an `NHLClient` instance. EDGE data is only available from the 2021-2022 season onward.

## Common Parameters for All EDGE Methods

All EDGE methods share a consistent set of parameters. Player methods accept `player_id`, team methods accept `team_id`, and landing page methods accept neither.

- `player_id` (str): NHL player ID (e.g., "8478402" for Connor McDavid)
- `team_id` (str): NHL team ID (e.g., "10" for Toronto Maple Leafs)
- `season` (str, optional): Season in YYYYYYYY format (e.g., "20242025"). When omitted, defaults to the current season using the `/now` endpoint variant.
- `game_type` (int, optional): Type of games to include. Defaults to `2`.
  - `1`: Preseason
  - `2`: Regular season
  - `3`: Playoffs

All responses include a `seasonsWithEdgeStats` field listing the seasons that have EDGE data available for the given player or team.

The top 10 leaderboard methods (`*_top_10`) take extra filter arguments. They return a list of 10 rows instead of a dict with `seasonsWithEdgeStats`. See [Top 10 Leaderboards](#top-10-leaderboards-shared-parameters-and-allowed-values).

## Get Comprehensive Skater EDGE Profile with skater_detail

Returns the full EDGE tracking profile for a skater, including shot speed, skating speed, distance traveled, shot locations, and zone time data. Every stat includes a league-average comparison and percentile ranking.

```python
from nhlpy import NHLClient

client = NHLClient()

# Current season (uses /now endpoint)
detail = client.edge.skater_detail(player_id="8478402")

# Specific season and game type
detail = client.edge.skater_detail(
    player_id="8478402",
    season="20242025",
    game_type=2
)

print(f"Top shot speed: {detail['topShotSpeed']['imperial']} mph")
print(f"Max skating speed: {detail['skatingSpeed']['speedMax']['imperial']} mph")
```

**Response structure:**

- `player` (object): Player identification and basic stats
  - `id` (int): Player ID
  - `firstName` (object): `default` (str) first name
  - `lastName` (object): `default` (str) last name
  - `sweaterNumber` (int): Jersey number
  - `position` (str): Position played
  - `headshot` (str): URL to headshot image
  - `goals` (int): Goals scored
  - `assists` (int): Assists recorded
  - `points` (int): Total points
  - `gamesPlayed` (int): Games played
  - `team` (object): `abbrev` (str) team abbreviation
- `topShotSpeed` (object): Hardest shot recorded
  - `imperial` (float): Speed in mph
  - `metric` (float): Speed in km/h
  - `percentile` (float): League percentile (0-1)
  - `leagueAvg` (object): `imperial` (float) league average in mph
  - `overlay` (object): Game context for the top shot
- `skatingSpeed` (object): Skating speed metrics
  - `speedMax` (object): `imperial` (float), `metric` (float), `percentile` (float)
  - `burstsOver20` (object): `value` (int) number of 20+ mph bursts, `percentile` (float)
- `totalDistanceSkated` (object): Total distance metrics
  - `imperial` (float): Distance in miles
  - `metric` (float): Distance in kilometers
  - `percentile` (float): League percentile
- `sogSummary` (list): Shots on goal by location zone
  - `locationCode` (str): Zone identifier ("all", "high", "mid", "low")
  - `shots` (int): Shot count
  - `shotsPercentile` (float): Percentile for shot count
  - `goals` (int): Goals scored from this zone
  - `goalsPercentile` (float): Percentile for goal count
  - `shootingPctg` (float): Shooting percentage
- `sogDetails` (list): Shots on goal by specific area
  - `area` (str): Specific area name (e.g., "Slot", "Behind the Net", "Inner Slot", "Point")
  - `shots` (int): Shot count from this area
  - `shotsPercentile` (float): Percentile for shot count
- `zoneTimeDetails` (object): Time spent in each zone
  - `offensiveZonePctg` (float): Percentage of time in offensive zone
  - `offensiveZonePercentile` (float): League percentile
  - `neutralZonePctg` (float): Percentage of time in neutral zone
  - `defensiveZonePctg` (float): Percentage of time in defensive zone
  - Even-strength variants: `offensiveZoneEvPctg`, `offensiveZoneEvPercentile`, etc.
  - `leagueAvg` (object): League averages for each zone metric

## Get Skater Shot Speed Breakdown with skater_shot_speed_detail

Returns detailed shot speed data for a specific skater, including speed distributions and game-by-game breakdowns.

```python
from nhlpy import NHLClient

client = NHLClient()
shot_speed = client.edge.skater_shot_speed_detail(player_id="8478402")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Skater Skating Speed Stats with skater_skating_speed_detail

Returns skating speed statistics for a specific skater, including top speed, burst counts, and speed distributions.

```python
from nhlpy import NHLClient

client = NHLClient()
skating_speed = client.edge.skater_skating_speed_detail(player_id="8478402")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Skater Shot Locations with skater_shot_location_detail

Returns shot location data for a specific skater, including shooting patterns from different ice areas.

```python
from nhlpy import NHLClient

client = NHLClient()
shot_locations = client.edge.skater_shot_location_detail(player_id="8478402")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Skater Distance Traveled with skater_skating_distance_detail

Returns distance skated statistics for a specific skater, including per-game and per-shift breakdowns.

```python
from nhlpy import NHLClient

client = NHLClient()
distance = client.edge.skater_skating_distance_detail(player_id="8478402")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Compare Skater Against League with skater_comparison

Returns comparison statistics for a skater against league averages across all EDGE metrics.

```python
from nhlpy import NHLClient

client = NHLClient()
comparison = client.edge.skater_comparison(player_id="8478402", season="20242025")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Skater Zone Time Breakdown with skater_zone_time

Returns time spent in offensive, defensive, and neutral zones for a specific skater.

```python
from nhlpy import NHLClient

client = NHLClient()
zone_time = client.edge.skater_zone_time(player_id="8478402")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get League-Wide Skater EDGE Leaders with skater_landing

Returns the league leaders across all skater EDGE categories. This is a league-wide overview, not specific to any single player.

```python
from nhlpy import NHLClient

client = NHLClient()

# Current season leaders
leaders = client.edge.skater_landing()

# Specific season leaders
leaders = client.edge.skater_landing(season="20242025", game_type=2)
```

**Parameters:** `season` (str, optional), `game_type` (int, default 2)

**Response structure:**

- `leaders` (object): League leaders by category
  - `hardestShot` (list): Players with the hardest shots, each with player info and stat values
  - `maxSkatingSpeed` (list): Players with highest skating speeds
  - `totalDistanceSkated` (list): Players with most distance skated
  - `highDangerSOG` (list): Players with most high-danger shots on goal
  - `offensiveZoneTime` (list): Players with most offensive zone time
  - `defensiveZoneTime` (list): Players with most defensive zone time
  - Each leader entry includes player identification fields and the relevant stat value

## Get Compact Skater EDGE Profile with cat_skater_detail

Returns a compact version of the skater EDGE detail using the CAT (Catch All Tracking) endpoint. Contains the same categories as `skater_detail` in a more condensed format.

```python
from nhlpy import NHLClient

client = NHLClient()
cat_detail = client.edge.cat_skater_detail(player_id="8478402")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Comprehensive Goalie EDGE Profile with goalie_detail

Returns the full EDGE tracking profile for a goalie, including save percentages by location, goals against metrics, and performance comparisons.

```python
from nhlpy import NHLClient

client = NHLClient()

# Current season
detail = client.edge.goalie_detail(player_id="8476945")

# Specific season
detail = client.edge.goalie_detail(
    player_id="8476945",
    season="20242025",
    game_type=2
)

print(f"Save percentage: {detail['player']['savePctg']}")
```

**Response structure:**

- `player` (object): Goalie identification and basic stats
  - `id` (int): Player ID
  - `firstName` (object): `default` (str) first name
  - `lastName` (object): `default` (str) last name
  - `wins` (int): Wins
  - `losses` (int): Losses
  - `overtimeLosses` (int): Overtime losses
  - `goalsAgainstAvg` (float): Goals against average
  - `savePctg` (float): Save percentage
  - `gamesPlayed` (int): Games played
  - `team` (object): `abbrev` (str) team abbreviation
- `stats` (object): Advanced goalie metrics
  - `goalsAgainstAvg` (object): `value` (float), `percentile` (float), `leagueAvg` (float)
  - `gamesAbove900` (object): Count of games with save percentage above .900
  - `goalDifferentialPer60` (object): Goal differential per 60 minutes
  - `goalSupportAvg` (object): Average goal support from the team
  - `pointPctg` (object): Point percentage
- `shotLocationSummary` (list): Save stats by shot location zone
  - `locationCode` (str): Zone identifier
  - `goalsAgainst` (int): Goals allowed from this zone
  - `saves` (int): Saves made from this zone
  - `savePctg` (float): Save percentage for this zone
  - Each field has `percentile` (float) and `leagueAvg` (float) variants
- `shotLocationDetails` (list): Save stats by specific area
  - `area` (str): Specific area name
  - `saves` (int): Save count
  - `savesPercentile` (float): Percentile for saves
  - `savePctg` (float): Save percentage
  - `savePctgPercentile` (float): Percentile for save percentage

## Get Goalie Shot Location Saves with goalie_shot_location_detail

Returns detailed shot location data faced by a specific goalie, including save percentages by zone.

```python
from nhlpy import NHLClient

client = NHLClient()
shot_locations = client.edge.goalie_shot_location_detail(player_id="8476945")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Goalie 5v5 Performance with goalie_5v5_detail

Returns five-on-five performance statistics and save percentages for a specific goalie.

```python
from nhlpy import NHLClient

client = NHLClient()
fivevfive = client.edge.goalie_5v5_detail(player_id="8476945")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Compare Goalie Against League with goalie_comparison

Returns comparison statistics for a goalie relative to league averages across all EDGE metrics.

```python
from nhlpy import NHLClient

client = NHLClient()
comparison = client.edge.goalie_comparison(player_id="8476945")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Goalie Save Percentage Breakdown with goalie_save_percentage_detail

Returns detailed save percentage breakdowns by situation, shot type, and location for a specific goalie.

```python
from nhlpy import NHLClient

client = NHLClient()
sv_pct = client.edge.goalie_save_percentage_detail(player_id="8476945")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get League-Wide Goalie EDGE Leaders with goalie_landing

Returns the league leaders across all goalie EDGE categories. This is a league-wide overview, not specific to any single goalie.

```python
from nhlpy import NHLClient

client = NHLClient()
leaders = client.edge.goalie_landing()
leaders = client.edge.goalie_landing(season="20242025", game_type=2)
```

**Parameters:** `season` (str, optional), `game_type` (int, default 2)

## Get Compact Goalie EDGE Profile with cat_goalie_detail

Returns a compact version of the goalie EDGE detail using the CAT (Catch All Tracking) endpoint.

```python
from nhlpy import NHLClient

client = NHLClient()
cat_detail = client.edge.cat_goalie_detail(player_id="8476945")
```

**Parameters:** `player_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Comprehensive Team EDGE Profile with team_detail

Returns the full EDGE tracking profile for a team, including shot speed, skating speed, distance skated, shot locations, and zone time. Team responses use league rank instead of percentile for comparisons.

```python
from nhlpy import NHLClient

client = NHLClient()

# Current season
detail = client.edge.team_detail(team_id="10")

# Specific season
detail = client.edge.team_detail(
    team_id="10",
    season="20242025",
    game_type=2
)

print(f"Top shot speed: {detail['shotSpeed']['topShotSpeed']['imperial']} mph")
print(f"Shot speed rank: {detail['shotSpeed']['topShotSpeed']['rank']}")
```

**Response structure:**

- `team` (object): Team identification and record
  - `id` (int): Team ID
  - `commonName` (object): `default` (str) team name
  - `abbrev` (str): Team abbreviation
  - `teamLogo` (object): `light` (str) and `dark` (str) logo URLs
  - `conference` (str): Conference name
  - `division` (str): Division name
  - `wins` (int): Wins
  - `losses` (int): Losses
  - `otLosses` (int): Overtime losses
  - `gamesPlayed` (int): Games played
  - `points` (int): Points in standings
- `shotSpeed` (object): Team shot speed metrics
  - `shotAttemptsOver90` (object): `value` (int) shots over 90 mph, `rank` (int) league rank
  - `topShotSpeed` (object): `imperial` (float) mph, `metric` (float) km/h, `rank` (int) league rank
- `skatingSpeed` (object): Team skating speed metrics
  - `burstsOver22` (object): `value` (int) bursts over 22 mph, `rank` (int)
  - `burstsOver20` (object): `value` (int), `rank` (int)
  - `speedMax` (object): `imperial` (float), `metric` (float), `rank` (int)
- `distanceSkated` (object): Team distance metrics
  - `total` (object): `imperial` (float) miles, `metric` (float) km, `rank` (int) league rank
- `sogSummary` (list): Shots on goal by location zone
  - `locationCode` (str): Zone identifier
  - `shots` (int): Shot count
  - `shotsRank` (int): League rank for shots
  - `shootingPctg` (float): Shooting percentage
  - `shootingPctgRank` (int): League rank for shooting percentage
  - `goals` (int): Goals scored
  - `goalsRank` (int): League rank for goals
- `zoneTimeDetails` (object): Zone time with league rankings
  - `offensiveZonePctg` (float): Percentage of time in offensive zone
  - `offensiveZoneRank` (int): League rank for offensive zone time
  - `neutralZonePctg` (float): Neutral zone time percentage
  - `defensiveZonePctg` (float): Defensive zone time percentage
  - `defensiveZoneRank` (int): League rank for defensive zone time

## Get Team Skating Distance Stats with team_skating_distance_detail

Returns skating distance statistics for a specific team, including per-game and per-player breakdowns.

```python
from nhlpy import NHLClient

client = NHLClient()
distance = client.edge.team_skating_distance_detail(team_id="10")
```

**Parameters:** `team_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Team Zone Time Breakdown with team_zone_time_details

Returns time spent in offensive, defensive, and neutral zones for a specific team.

```python
from nhlpy import NHLClient

client = NHLClient()
zone_time = client.edge.team_zone_time_details(team_id="10")
```

**Parameters:** `team_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Team Shot Location Stats with team_shot_location_detail

Returns shot location data for a specific team, including shooting patterns from different ice areas.

```python
from nhlpy import NHLClient

client = NHLClient()
shot_locations = client.edge.team_shot_location_detail(team_id="10")
```

**Parameters:** `team_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get League-Wide Team EDGE Leaders with team_landing

Returns the league leaders and rankings across all team EDGE categories.

```python
from nhlpy import NHLClient

client = NHLClient()
leaders = client.edge.team_landing()
leaders = client.edge.team_landing(season="20242025", game_type=2)
```

**Parameters:** `season` (str, optional), `game_type` (int, default 2)

## Get Team Shot Speed Stats with team_shot_speed_detail

Returns shot speed statistics for a specific team, including maximum and average speeds.

```python
from nhlpy import NHLClient

client = NHLClient()
shot_speed = client.edge.team_shot_speed_detail(team_id="10")
```

**Parameters:** `team_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Get Team Skating Speed Stats with team_skating_speed_detail

Returns skating speed statistics for a specific team, including burst speed counts and averages.

```python
from nhlpy import NHLClient

client = NHLClient()
skating_speed = client.edge.team_skating_speed_detail(team_id="10")
```

**Parameters:** `team_id` (str), `season` (str, optional), `game_type` (int, default 2)

## Compare Team Against League with team_comparison

Returns a team's EDGE stats in the shape used by the team view of nhl.com's EDGE comparison tool: shot speed, skating speed, distance skated (including the last 10 games), shot locations, zone time against league average, and shot differential.

```python
from nhlpy import NHLClient

client = NHLClient()
comparison = client.edge.team_comparison(team_id="22")  # Edmonton
zone = comparison["zoneTimeDetails"]
print(f"OZ time {zone['offensiveZonePctg']:.1%} (league {zone['offensiveZoneLeagueAvg']:.1%})")
```

**Parameters:** `team_id` (str), `season` (str, optional), `game_type` (int, default 2)

**Response structure:**

- `team` (object): `id`, `abbrev`, `commonName{default}`, `placeNameWithPreposition{default}`, `teamLogo`, `slug`
- `seasonsWithEdgeStats` (list): Seasons with EDGE data
- `shotSpeedDetails` (object): `topShotSpeed`, `avgShotSpeed`, `shotAttemptsOver100`, `shotAttempts90To100`, `shotAttempts80To90`, `shotAttempts70To80`
- `skatingSpeedDetails` (object): `maxSkatingSpeed`, `burstsOver22`, `bursts20To22`, `bursts18To20`
- `skatingDistanceDetails` (object): `distanceTotal`, `distancePer60`, `distanceMaxGame`, `distanceMaxPeriod`
- `skatingDistanceLast10` (list): Distance skated in each of the last 10 games
- `shotLocationDetails` (list): Shot stats for each rink area
- `shotLocationTotals` (list): Shot totals by area group (all, high danger, mid range, long range)
- `zoneTimeDetails` (object): `offensiveZonePctg`, `neutralZonePctg` and `defensiveZonePctg`, each with a matching `...LeagueAvg`
- `shotDifferential` (object): `shotAttemptDifferential`, `sogDifferential`

## Top 10 Leaderboards: Shared Parameters and Allowed Values

The `*_top_10` methods return the league's top 10 skaters, goalies, or teams for an EDGE metric. They are the leaderboards on nhl.com's EDGE pages.

- Each method returns `List[dict]` with 10 rows.
- Skater and goalie rows have a `player` object; team rows have a `team` object. The metric fields are listed in each method's section.
- Every method also accepts `season` (str, optional; defaults to the current season) and `game_type` (int, default 2).
- Invalid values raise `ValueError` before any request is made. The API itself would return a 404 for an unknown sort, or an empty list for an unknown position group.
- The allowed values are importable from `nhlpy.api.edge` (for example `from nhlpy.api.edge import SKATING_SPEED_SORTS`).

| Argument | Allowed values | Constant |
|---|---|---|
| `position_group` | `"all"`, `"forwards"`, `"defense"` | `POSITION_GROUPS` |
| `strength` | `"all"`, `"es"` (even strength), `"pp"` (power play), `"pk"` (penalty kill) | `STRENGTHS` |
| `sort` (skating speed) | `"max"`, `"over-22"`, `"20-22"`, `"18-20"` (mph bursts) | `SKATING_SPEED_SORTS` |
| `sort` (shot speed) | `"max"`, `"over-100"`, `"90-99"`, `"80-89"`, `"70-79"` (mph attempts) | `SHOT_SPEED_SORTS` |
| `sort` (skating distance) | `"total"`, `"per-60"`, `"max-game"`, `"max-period"` | `SKATING_DISTANCE_SORTS` |
| `sort` (zone time) | `"offensive"`, `"neutral"`, `"defensive"` | `ZONE_TIME_SORTS` |
| `category` (skater/team shot location) | `"sog"`, `"goals"`, `"shooting-pctg"` | `SHOT_LOCATION_CATEGORIES` |
| `category` (goalie shot location) | `"save-pctg"`, `"saves"`, `"goals-against"`, `"shots-against"` | `GOALIE_SHOT_LOCATION_CATEGORIES` |
| `area` (shot location) | `"all"`, `"high"` (high danger), `"mid"` (mid range), `"long"` (long range) | `SHOT_LOCATION_AREAS` |
| `sort` (goalie 5v5) | `"save-pctg"`, `"save-pctg-close"`, `"shots"`, `"shots-per-60"` | `GOALIE_5V5_SORTS` |
| `sort` (goalie save %) | `"pctg"`, `"games"` | `GOALIE_SAVE_PCTG_SORTS` |

The first value listed is each argument's default.

**`player` object (skater and goalie rows):**

- `firstName` / `lastName` (object): `default` name
- `slug` (str): URL slug (e.g., "philip-broberg-8481598")
- `headshot` (str): Headshot image URL
- `position` (str): Position code
- `sweaterNumber` (int): Jersey number
- `team` (object): `abbrev`, `commonName{default}`, `placeNameWithPreposition{default}`, `teamLogo{light,dark}`
- `id` (int, `goalie_shot_location_top_10` only): Player ID. Other leaderboards don't include a player ID; use `slug`, which ends in the ID

**`team` object (team rows):** `abbrev`, `commonName{default}`, `placeNameWithPreposition{default}`, `slug`, `teamLogo{light,dark}`, and on some leaderboards `id`

Speed and distance metrics are objects with `imperial` (mph or miles) and `metric` (km/h or km) values. Single-best metrics (top speed, hardest shot, max per game or period) also have an `overlay` object describing the game, and the player for team rows, where it happened.

```python
from nhlpy import NHLClient

client = NHLClient()
fastest = client.edge.skater_skating_speed_top_10(position_group="defense")
for row in fastest:
    p = row["player"]
    print(f"{p['firstName']['default']} {p['lastName']['default']} ({p['team']['abbrev']}): {row['maxSpeed']['imperial']:.2f} mph")
```

## Get Top 10 Skaters by Skating Speed with skater_skating_speed_top_10

**Parameters:** `position_group` (default "all"), `sort` (skating speed, default "max"), `season`, `game_type`

**Row fields:** `player`, `maxSpeed` (`imperial`/`metric`/`overlay`), `burstsOver22`, `bursts20To22`, `bursts18To20` (int)

## Get Top 10 Skaters by Shot Speed with skater_shot_speed_top_10

**Parameters:** `position_group` (default "all"), `sort` (shot speed, default "max"), `season`, `game_type`

**Row fields:** `player`, `hardestShot` (`imperial`/`metric`/`overlay`), `shotAttemptsOver100`, `shotAttempts90To100`, `shotAttempts80To90`, `shotAttempts70To80` (int)

## Get Top 10 Skaters by Distance Skated with skater_skating_distance_top_10

**Parameters:** `position_group` (default "all"), `strength` (default "all"), `sort` (skating distance, default "total"), `season`, `game_type`

**Row fields:** `player`, `distanceTotal`, `distancePer60` (`imperial`/`metric`), `distanceMaxPerGame`, `distanceMaxPerPeriod` (`imperial`/`metric`/`overlay`)

## Get Top 10 Skaters by Zone Time with skater_zone_time_top_10

**Parameters:** `position_group` (default "all"), `strength` (default "all"), `sort` (zone time, default "offensive"), `season`, `game_type`

**Row fields:** `player`, `offensiveZoneTime`, `neutralZoneTime`, `defensiveZoneTime` (float, 0-1 share of ice time)

## Get Top 10 Skaters by Shot Location with skater_shot_location_top_10

**Parameters:** `position_group` (default "all"), `category` (default "sog"), `area` (default "all"), `season`, `game_type`

**Row fields:** `player`, `all`, `highDanger`, `midRange`, `longRange`. Each is the `category` value from that area: counts for `"sog"` and `"goals"`, fractions for `"shooting-pctg"`. Rows are ranked by the `area` column.

```python
client.edge.skater_shot_location_top_10(category="goals", area="high")  # most high-danger goals
```

## Get Top 10 Goalies by 5v5 Stats with goalie_5v5_top_10

**Parameters:** `sort` (goalie 5v5, default "save-pctg"), `season`, `game_type`

**Row fields:** `player`, `savePctg` (float), `savePctgClose` (float, close games), `shots` (int), `shotsPer60` (float)

## Get Top 10 Goalies by .900+ Games with goalie_save_percentage_top_10

**Parameters:** `sort` (goalie save %, default "pctg"), `season`, `game_type`

**Row fields:** `player`, `gamesOver900` (int, games with a save percentage over .900), `pctgGamesOver900` (float, share of games)

## Get Top 10 Goalies by Shot Location with goalie_shot_location_top_10

**Parameters:** `category` (goalie shot location, default "save-pctg"), `area` (default "all"), `season`, `game_type`

**Row fields:** `player`, `all`, `highDanger`, `midRange`, `longRange`. Each is the `category` value from that area: fractions for `"save-pctg"`, counts otherwise.

## Get Top 10 Teams by Skating Speed with team_skating_speed_top_10

**Parameters:** `position_group` (default "all"), `sort` (skating speed, default "max"), `season`, `game_type`

**Row fields:** `team`, `maxSkatingSpeed` (`imperial`/`metric`/`overlay`), `burstsOver22`, `bursts20To22`, `bursts18To20` (int)

## Get Top 10 Teams by Shot Speed with team_shot_speed_top_10

**Parameters:** `position_group` (default "all"), `sort` (shot speed, default "max"), `season`, `game_type`

**Row fields:** `team`, `hardestShot` (`imperial`/`metric`/`overlay`), `shotAttemptsOver100`, `shotAttempts90To100`, `shotAttempts80To90`, `shotAttempts70To80` (int)

## Get Top 10 Teams by Distance Skated with team_skating_distance_top_10

**Parameters:** `position_group` (default "all"), `strength` (default "all"), `sort` (skating distance, default "total"), `season`, `game_type`

**Row fields:** `team`, `distanceTotal`, `distancePer60` (`imperial`/`metric`), `distanceMaxPerGame`, `distanceMaxPerPeriod` (`imperial`/`metric`/`overlay`)

## Get Top 10 Teams by Zone Time with team_zone_time_top_10

**Parameters:** `strength` (default "all"), `sort` (zone time, default "offensive"), `season`, `game_type`. There is no position group.

**Row fields:** `team`, `offensiveZoneTime`, `neutralZoneTime`, `defensiveZoneTime` (float, 0-1 share of ice time)

## Get Top 10 Teams by Shot Location with team_shot_location_top_10

**Parameters:** `position_group` (default "all"), `category` (default "sog"), `area` (default "all"), `season`, `game_type`

**Row fields:** `team`, `all`, `highDanger`, `midRange`, `longRange`. Each is the `category` value from that area.
