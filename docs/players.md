# Players API Module

The players module provides methods for retrieving NHL player rosters and prospect information by team. Access it via `client.players` on an `NHLClient` instance.

## Get Team Prospects with prospects_by_team

Retrieves all prospects for a given NHL team, grouped by position. Returns forwards, defensemen, and goalies in separate lists.

```python
from nhlpy import NHLClient

client = NHLClient()
prospects = client.players.prospects_by_team(team_abbr="BUF")

for forward in prospects["forwards"]:
    print(f"{forward['firstName']['default']} {forward['lastName']['default']}")
```

**Parameters:**

- `team_abbr` (str, required): Three-letter team abbreviation (e.g., "BUF", "TOR", "EDM")

**Response structure:**

- `forwards` (list): List of forward prospect objects
- `defensemen` (list): List of defensemen prospect objects
- `goalies` (list): List of goalie prospect objects

**Player fields within each list:**

- `id` (int): Unique NHL player identifier
- `headshot` (str): URL to the player's headshot image
- `firstName` (object):
  - `default` (str): Player's first name
- `lastName` (object):
  - `default` (str): Player's last name
- `positionCode` (str): Position code (e.g., "C", "L", "R", "D", "G")
- `shootsCatches` (str): Handedness ("L" or "R")
- `heightInInches` (int): Height in inches
- `weightInPounds` (int): Weight in pounds
- `heightInCentimeters` (int): Height in centimeters
- `weightInKilograms` (int): Weight in kilograms
- `birthDate` (str): Date of birth in "YYYY-MM-DD" format
- `birthCity` (object):
  - `default` (str): City of birth
- `birthCountry` (str): Three-letter country code (e.g., "CAN", "USA")
- `sweaterNumber` (int, optional): Jersey number. Not all prospects have one assigned.
- `birthStateProvince` (object, optional):
  - `default` (str): State or province of birth. Only present for some countries.

## Get Team Roster with players_by_team

Retrieves the full roster for a given team and season. This is an alias for `client.teams.team_roster()` and returns the same data structure. Use whichever access pattern fits your code organization.

```python
from nhlpy import NHLClient

client = NHLClient()
roster = client.players.players_by_team(team_abbr="TOR", season="20242025")

for player in roster["forwards"]:
    print(f"#{player['sweaterNumber']} {player['firstName']['default']} {player['lastName']['default']}")
```

**Parameters:**

- `team_abbr` (str, required): Three-letter team abbreviation (e.g., "BUF", "TOR", "EDM")
- `season` (str, required): Season in YYYYYYYY format (e.g., "20242025")

**Response structure:**

- `forwards` (list): List of forward player objects
- `defensemen` (list): List of defensemen player objects
- `goalies` (list): List of goalie player objects

**Player fields within each list:**

- `id` (int): Unique NHL player identifier
- `headshot` (str): URL to the player's headshot image
- `firstName` (object):
  - `default` (str): Player's first name
- `lastName` (object):
  - `default` (str): Player's last name
- `sweaterNumber` (int): Jersey number
- `positionCode` (str): Position code (e.g., "C", "L", "R", "D", "G")
- `shootsCatches` (str): Handedness ("L" or "R")
- `heightInInches` (int): Height in inches
- `weightInPounds` (int): Weight in pounds
- `heightInCentimeters` (int): Height in centimeters
- `weightInKilograms` (int): Weight in kilograms
- `birthDate` (str): Date of birth in "YYYY-MM-DD" format
- `birthCity` (object):
  - `default` (str): City of birth
- `birthCountry` (str): Three-letter country code (e.g., "CAN", "USA")
- `birthStateProvince` (object, optional):
  - `default` (str): State or province of birth. Only present for some countries.
