# Teams API

The Teams module provides access to NHL team information, rosters, and franchise data. Access it via `client.teams` on an `NHLClient` instance.

## Teams: List All Current NHL Teams

Returns a list of all 32 current NHL teams with conference, division, and franchise information. For every team past and present (Quebec Nordiques, Hartford Whalers, ...) use `all_time_teams()`. This method transforms the raw API response into a clean, standardized format by combining standings data with franchise metadata.

```python
from nhlpy import NHLClient

client = NHLClient()

# Current teams
teams = client.teams.teams()

# Teams for a specific date (useful during preseason)
teams = client.teams.teams(date="2024-10-04")
```

- **Parameters**
  - `date` (str, default "now"): Date in YYYY-MM-DD format. The NHL API resolves "now" to the current date, but during preseason this may return previous-season data. Supply a specific date at the start of the upcoming season to get accurate results (e.g., "2024-10-04" for the 2024-2025 season).
- **Returns**: list of dicts, one per team (32 entries for current NHL)
  - `name` (str): Full team name (e.g., "Toronto Maple Leafs")
  - `common_name` (str): Common team name (e.g., "Maple Leafs")
  - `abbr` (str): Three-letter abbreviation (e.g., "TOR")
  - `logo` (str): URL to the team logo SVG
  - `franchise_id` (int): Franchise identifier, joined from the franchises endpoint
  - `conference` (object): Conference details
    - `abbr` (str): Conference abbreviation (e.g., "E", "W")
    - `name` (str): Conference name (e.g., "Eastern", "Western")
  - `division` (object): Division details
    - `abbr` (str): Division abbreviation (e.g., "A", "M", "C", "P")
    - `name` (str): Division name (e.g., "Atlantic", "Metropolitan", "Central", "Pacific")

## Teams: Get Team Roster by Season

Returns the full roster for a team in a given season, grouped by position category.

```python
from nhlpy import NHLClient

client = NHLClient()
roster = client.teams.team_roster(team_abbr="TOR", season="20242025")

# Access by position group
forwards = roster["forwards"]
defensemen = roster["defensemen"]
goalies = roster["goalies"]
```

- **Parameters**
  - `team_abbr` (str, required): Three-letter team abbreviation (e.g., "BUF", "TOR", "EDM")
  - `season` (str, required): Season in YYYYYYYY format (e.g., "20242025")
- **Returns**: dict with three keys, each containing a list of player dicts
  - `forwards` (list): Forward players
  - `defensemen` (list): Defensemen
  - `goalies` (list): Goaltenders
- **Player fields** (same for all position groups)
  - `id` (int): Unique player identifier
  - `headshot` (str): URL to player headshot image
  - `firstName.default` (str): Player first name
  - `lastName.default` (str): Player last name
  - `sweaterNumber` (int): Jersey number
  - `positionCode` (str): Position code
    - `"L"` = Left wing
    - `"R"` = Right wing
    - `"C"` = Center
    - `"D"` = Defenseman
    - `"G"` = Goaltender
  - `shootsCatches` (str): "L" or "R"
  - `heightInInches` (int): Height in inches
  - `weightInPounds` (int): Weight in pounds
  - `heightInCentimeters` (int): Height in centimeters
  - `weightInKilograms` (int): Weight in kilograms
  - `birthDate` (str): Date of birth
  - `birthCity.default` (str): Birth city
  - `birthCountry` (str): Three-letter country code (e.g., "CAN", "USA", "SWE")
  - `birthStateProvince.default` (str, optional): Birth state or province, not present for all players

## Teams: List All NHL Franchises Including Historical

Returns all NHL franchises, including historical and defunct teams. The current league has 32 active teams, but there are approximately 40 franchise records total.

```python
from nhlpy import NHLClient

client = NHLClient()
franchises = client.teams.franchises()
```

- **Parameters**: None
- **Returns**: list of dicts, one per franchise (approximately 40 entries)
  - `id` (int): Franchise identifier, used as `franchise_id` in stats API filters
  - `fullName` (str): Full franchise name (e.g., "Toronto Maple Leafs", "Montreal Wanderers")
  - `teamCommonName` (str): Common name (e.g., "Maple Leafs", "Wanderers")
  - `teamPlaceName` (str): Place name (e.g., "Toronto", "Montreal")

## Teams: List All-Time NHL Teams with Franchise IDs

Returns every NHL team past and present, including relocated and defunct teams, with the franchise it belongs to. Use `teams()` instead for the current 32 teams with conference and division. Unlike `teams()`, this returns the NHL's raw field names (`triCode`, `franchiseId`). A franchise can have several teams over time: the Quebec Nordiques (team 32) and Colorado Avalanche (team 21) are both franchise 27. Team IDs are the `teamId` values used by game feeds and the stats API, so this is the lookup from a team ID or abbreviation in a given season to its franchise.

```python
from nhlpy import NHLClient

client = NHLClient()
teams = client.teams.all_time_teams()

# Team ID -> franchise ID
franchise_by_team = {t["id"]: t["franchiseId"] for t in teams}
franchise_by_team[32]  # 27 (Quebec Nordiques)
```

- **Parameters**: None
- **Returns**: list of dicts, one per team (about 60 entries), returned as the NHL publishes them
  - `id` (int): Team identifier (e.g., 32 for the Quebec Nordiques)
  - `franchiseId` (int or None): Franchise identifier. `None` for placeholder entries such as "To be determined" (id 70) and "NHL" (id 99)
  - `fullName` (str): Full team name (e.g., "Quebec Nordiques")
  - `triCode` (str): Three-letter abbreviation (e.g., "QUE"). Abbreviations are reused over time (e.g., "UTA" is both team 59 and team 68), so match them within one season's teams
  - `rawTricode` (str): Raw three-letter abbreviation
  - `leagueId` (int): League identifier

Example response entry:

```json
{"id": 32, "franchiseId": 27, "fullName": "Quebec Nordiques", "leagueId": 133, "rawTricode": "QUE", "triCode": "QUE"}
```

To list the teams that played in a specific season, combine it with `client.stats.team_summary(start_season="19901991", end_season="19901991")`, which returns that season's `teamId`s.
