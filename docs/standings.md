# Standings API

The Standings module provides access to NHL league standings and historical season metadata. Access it via `client.standings` on an `NHLClient` instance.

## Standings: Get Current or Historical League Standings

Retrieves NHL standings for the current date, a specific date, or the end of a historical season. Supply either `season` or `date` but not both -- if both are provided, `season` takes precedence. When neither is provided, returns standings for the current date.

```python
from nhlpy import NHLClient

client = NHLClient()

# Current standings
standings = client.standings.league_standings()

# Standings for a specific date
standings = client.standings.league_standings(date="2025-01-15")

# Final standings for a completed season
standings = client.standings.league_standings(season="20232024")
```

- **Parameters**
  - `season` (str, optional): Season identifier in YYYYYYYY format (e.g., "20232024"). When provided, the method looks up the last date of that season via the season manifest and returns final standings. Takes precedence over `date` if both are supplied.
  - `date` (str, optional): Date in YYYY-MM-DD format. Returns standings as of that date. Defaults to "now" (current date) when neither parameter is provided.
- **Returns**: dict with standings metadata and a list of team standing objects
  - `wildCardIndicator` (bool): Whether wildcard standings apply
  - `standings` (list): 32 team standing entries, one per team
- **Team standing fields**
  - `teamName.default` (str): Full team name (e.g., "Winnipeg Jets")
  - `teamCommonName.default` (str): Common name (e.g., "Jets")
  - `teamAbbrev.default` (str): Three-letter abbreviation (e.g., "WPG")
  - `teamLogo` (str): URL to team logo
  - `conferenceAbbrev` (str): Conference abbreviation ("E" or "W")
  - `conferenceName` (str): Conference name ("Eastern" or "Western")
  - `divisionAbbrev` (str): Division abbreviation ("A", "M", "C", or "P")
  - `divisionName` (str): Division name ("Atlantic", "Metropolitan", "Central", or "Pacific")
  - `conferenceSequence` (int): Rank within conference
  - `divisionSequence` (int): Rank within division
  - `leagueSequence` (int): Rank across the entire league
  - `wildcardSequence` (int): Wildcard ranking (0 if not in wildcard position)
  - `date` (str): Standings date
  - `seasonId` (int): Season identifier
  - `placeName.default` (str): City or place name
  - **Record fields**
    - `gamesPlayed` (int)
    - `wins` (int)
    - `losses` (int)
    - `otLosses` (int): Overtime losses
    - `points` (int)
    - `pointPctg` (float): Points percentage
    - `regulationWins` (int)
    - `regulationPlusOtWins` (int): Regulation plus overtime wins (ROW)
    - `goalFor` (int): Total goals scored
    - `goalAgainst` (int): Total goals allowed
    - `goalDifferential` (int): Goal differential
  - **Streak fields**
    - `streakCode` (str): Current streak type ("W" for wins, "L" for losses, "OT" for OT losses)
    - `streakCount` (int): Length of current streak
  - **Home record**
    - `homeWins` (int)
    - `homeLosses` (int)
    - `homePoints` (int)
  - **Road record**
    - `roadWins` (int)
    - `roadLosses` (int)
    - `roadPoints` (int)
  - **Last 10 games**
    - `l10Wins` (int)
    - `l10Losses` (int)
    - `l10Points` (int)
  - **Shootout record**
    - `shootoutWins` (int)
    - `shootoutLosses` (int)
  - **Clinch indicator**
    - `clinchIndicator` (str, optional): Playoff clinch status. Not present during regular season before clinching begins.
      - `"p"` = Clinched Presidents' Trophy
      - `"x"` = Clinched playoff spot
      - `"y"` = Clinched division title
      - `"z"` = Clinched conference title

## Standings: Get Historical Season Metadata

Returns metadata for every NHL season in the standings system. Useful for discovering valid season identifiers, date ranges, and which rules were in effect for each season.

```python
from nhlpy import NHLClient

client = NHLClient()
seasons = client.standings.season_standing_manifest()

# Find a specific season
season_2024 = next(s for s in seasons if s["id"] == 20242025)
print(season_2024["standingsStart"])  # First day of standings
print(season_2024["standingsEnd"])    # Last day of standings
```

- **Parameters**: None
- **Returns**: list of dicts, one per historical season
  - `id` (int): Season identifier in YYYYYYYY format (e.g., 20242025)
  - `conferencesInUse` (bool): Whether conferences were used for standings
  - `divisionsInUse` (bool): Whether divisions were used for standings
  - `pointForOTlossInUse` (bool): Whether a point was awarded for overtime losses
  - `regulationWinsInUse` (bool): Whether regulation wins were tracked separately
  - `rowInUse` (bool): Whether regulation/overtime wins (ROW) tiebreaker was active
  - `standingsStart` (str): First date of standings for the season (YYYY-MM-DD)
  - `standingsEnd` (str): Last date of standings for the season (YYYY-MM-DD)
  - `tiesInUse` (bool): Whether tie games were possible (pre-shootout era)
  - `wildcardInUse` (bool): Whether wildcard playoff format was in effect
