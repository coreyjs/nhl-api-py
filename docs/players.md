# Players API Module

The players module provides methods for retrieving individual player pages (header, home, bio, stats and game log, served from the v2 web API) plus NHL player rosters and prospect information by team. Access it via `client.players` on an `NHLClient` instance.

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

## Get Player Bio with player_bio

Retrieves a player's biographical information: vitals, bio text, transaction notes, draft details, awards, badges, and the player's current team with its full roster. Served from the v2 web API (`https://api-web.nhle.com/v2/player/{player_id}/bio`).

Several top-level sections are optional. `currentTeam` is absent for retired players, `draftDetails` is absent for undrafted players, and `awards` / `badges` appear only when the player has any. Check with `.get()` before reading them.

```python
from nhlpy import NHLClient

client = NHLClient()
bio = client.players.player_bio(player_id="8478402")

vitals = bio["vitals"]
print(f"{bio['bio']['firstName']['default']} {bio['bio']['lastName']['default']}")
print(f"Born {vitals['birthDate']} in {vitals['birthCity']['default']}, {vitals['birthCountry']}")
print(f"{vitals['heightInches']} in, {vitals['weightPounds']} lb, shoots {vitals['shootsCatches']}")

if team := bio.get("currentTeam"):
    print(f"Current team: {team['teamAbbrev']}")
if draft := bio.get("draftDetails"):
    print(f"Drafted {draft['year']} by {draft['teamAbbrev']}, #{draft['overallPick']} overall")
for award in bio.get("awards", []):
    years = [d["yearWon"] for d in award["details"]]
    print(f"{award['name']['default']}: {years}")
```

**Parameters:**

- `player_id` (str, required): NHL player ID (e.g., "8478402")

**Response structure:**

- `vitals` (object): Physical and birth details
  - `shootsCatches` (str): Handedness ("L" or "R")
  - `birthCity` (object):
    - `default` (str): City of birth
  - `birthStateProvince` (object, optional):
    - `default` (str): State or province of birth. Only present for some countries.
  - `birthCountry` (str): Three-letter country code (e.g., "CAN", "USA")
  - `nationality` (str): Three-letter nationality code
  - `nationalityCountry2Code` (str): Two-letter nationality code (e.g., "US")
  - `birthDate` (str): Date of birth in "YYYY-MM-DD" format
  - `age` (int, optional): Current age. Absent for retired players.
  - `actionShot` (str): URL to an action photo of the player
  - `heightInches` (int): Height in inches
  - `weightPounds` (int): Weight in pounds
- `bio` (object): Name and narrative text
  - `firstName` (object):
    - `default` (str): Player's first name
  - `lastName` (object):
    - `default` (str): Player's last name
  - `about` (object):
    - `default` (str): Biography text. Often an empty string.
  - `notesTransactions` (object):
    - `default` (str): Markdown bullet list of signings, trades, and other transactions
- `currentTeam` (object, optional): The player's current team. Absent for retired players.
  - `teamAbbrev` (str): Three-letter team abbreviation
  - `teamCommonName` (object):
    - `default` (str): Team common name (e.g., "Capitals")
  - `teamLogos` (object):
    - `light` (str): URL to the light-background team logo
    - `dark` (str): URL to the dark-background team logo
  - `roster` (object): Current team roster
    - `forwards` (list): Forward player objects
    - `defensemen` (list): Defenseman player objects
    - `goalies` (list): Goalie player objects
- `draftDetails` (object, optional): Draft information. Absent for undrafted players.
  - `year` (int): Draft year
  - `teamAbbrev` (str): Drafting team abbreviation
  - `round` (int): Draft round
  - `pickInRound` (int): Pick number within the round
  - `overallPick` (int): Overall pick number
  - `teamLogos` (object): `light` / `dark` logo URLs of the drafting team
  - `draftedFromTeam` (object):
    - `default` (str): Team the player was drafted from
  - `draftedFromLeagueAbbrev` (object):
    - `default` (str): League the player was drafted from
- `awards` (list, optional): Trophies won by the player
  - `shortName` (object): `default` short trophy name (e.g., "Vezina")
  - `name` (object): `default` full trophy name (e.g., "Vezina Trophy")
  - `slug` (str): Trophy slug (e.g., "vezina-trophy")
  - `grbUrl` (str): URL to the trophy page on records.nhl.com
  - `description` (object): Localized trophy description (`default`, plus other languages)
  - `trophyLogos` (object): `light` / `dark` trophy logo URLs
  - `moduleType` (str): Display module type (e.g., "STANLEY_CUP_BANNER")
  - `details` (list): One entry per time the award was won
    - `yearWon` (int): Year the award was won
    - `team` (object): Team the player was on, including `teamLogos`
- `badges` (list, optional): Honors such as Hall of Fame induction
  - `logoUrl` (object):
    - `default` (str): Badge logo URL
  - `title` (object):
    - `default` (str): Badge title (e.g., "Hockey Hall of Fame")

**Roster player fields within `currentTeam.roster` lists:**

- `id` (int): Unique NHL player identifier
- `headshot` (str): URL to the player's headshot image
- `slug` (str): URL slug (e.g., "alex-ovechkin-8471214")
- `firstName` (object):
  - `default` (str): Player's first name
- `lastName` (object):
  - `default` (str): Player's last name
- `sweaterNumber` (int): Jersey number
- `positionCode` (str): Position code (e.g., "C", "L", "R", "D", "G")

## Get Player Header with player_header

Retrieves the compact player summary shown at the top of every player page on nhl.com: identity, position, size, captaincy and current team. Served from `https://api-web.nhle.com/v2/player/{player_id}/header`.

```python
from nhlpy import NHLClient

client = NHLClient()
header = client.players.player_header(player_id="8478402")

print(f"#{header['sweaterNumber']} {header['firstName']['default']} {header['lastName']['default']} ({header['position']})")
if team := header.get("team"):
    print(team["fullTeamName"]["default"])
```

**Parameters:**

- `player_id` (str, required): NHL player ID (e.g., "8478402")

**Response structure:**

- `playerId` (int): Unique NHL player identifier
- `firstName` (object):
  - `default` (str): Player's first name
- `lastName` (object):
  - `default` (str): Player's last name
- `nationality` (str): Three-letter nationality code
- `nationalityCountry2Code` (str): Two-letter nationality code
- `age` (int, optional): Current age. Absent for retired players.
- `sweaterNumber` (int): Jersey number (last worn, for retired players)
- `position` (str): Position code (e.g., "C", "L", "R", "D", "G")
- `playerSlug` (str): URL slug (e.g., "connor-mcdavid-8478402")
- `headshot` (str): URL to the player's headshot image
- `heightInches` (int): Height in inches
- `weightPounds` (int): Weight in pounds
- `isCaptain` (bool, optional): Whether the player is his team's captain. Absent for retired players.
- `isInactiveNHL` (bool): True if the player is no longer active in the NHL
- `hasEdgeStats` (bool): Whether NHL EDGE tracking stats exist for the player
- `hasHome` (bool): Whether `player_home()` has game data for the player
- `mostRecentSeason` (int): Most recent season the player appeared in (YYYYYYYY)
- `team` (object, optional): Current team. Absent for retired players.
  - `abbrev` (str): Three-letter team abbreviation
  - `fullTeamName` (object): `default` full team name (e.g., "Edmonton Oilers")
  - `commonName` (object): `default` common name (e.g., "Oilers")
  - `placeNameWithPreposition` (object): `default` place name
  - `logo` (str): URL to the light-background team logo
  - `darkLogo` (str): URL to the dark-background team logo
- `badges` (list, optional): Honors such as Hall of Fame induction (`logoUrl`, `title`)

## Get Player Last and Next Game with player_home

Retrieves the player's most recent game (with his stat line), his next scheduled game (with broadcast info and career stats against that opponent), and his current team's roster. Served from `https://api-web.nhle.com/v2/player/{player_id}/home`.

`lastGame` and `nextGame` are only present when such a game exists, and retired players get only `lastName`. Check with `.get()`.

```python
from nhlpy import NHLClient

client = NHLClient()
home = client.players.player_home(player_id="8478402")

if last := home.get("lastGame"):
    line = last["playerStats"]
    print(f"Last game {last['gameDate']}: {line['goals']}G {line['assists']}A in {line['timeOnIce']}")
if nxt := home.get("nextGame"):
    print(f"Next: {nxt['awayTeam']['abbrev']} @ {nxt['homeTeam']['abbrev']} at {nxt['startTimeUTC']}")
```

**Parameters:**

- `player_id` (str, required): NHL player ID (e.g., "8478402")

**Response structure:**

- `lastName` (object):
  - `default` (str): Player's last name
- `teamAbbrev` (str, optional): Current team abbreviation
- `lastGame` (object, optional): The player's most recent game
  - `id` (int): Game ID
  - `gameType` (int): 1 = preseason, 2 = regular season, 3 = playoffs
  - `gameState` (str): Game state (e.g., "OFF" for final)
  - `gameScheduleState` (str): Schedule state (e.g., "OK")
  - `gameDate` (str): Date in "YYYY-MM-DD" format
  - `gameCenterLink` (str): Relative nhl.com game center path
  - `threeMinRecap` / `condensedGame` (str, optional): Relative nhl.com video paths (plus `...Fr` variants)
  - `gameVideo` (object, optional): Numeric video IDs for the recap and condensed game
  - `winningTeamId` (int): ID of the winning team
  - `periodDescriptor` (object): `number`, `periodType` ("REG", "OT", "SO"), `maxRegulationPeriods`
  - `homeTeam` / `awayTeam` (object): `id`, `abbrev`, `name{default}`, `teamLogo{light,dark}`, `score`, `sog`
  - `playerStats` (object): The player's line, e.g. `goals`, `assists`, `points`, `shotsOnGoal`, `timeOnIce`
- `nextGame` (object, optional): The player's next scheduled game
  - `id` (int): Game ID
  - `gameType` (int): Game type
  - `gameState` (str): Game state (e.g., "FUT")
  - `gameDate` (str): Date in "YYYY-MM-DD" format
  - `startTimeUTC` (str): Start time in ISO 8601 UTC
  - `venueTimezone` (str): IANA time zone of the venue
  - `ticketsLink` / `ticketsLinkFr` (str, optional): Ticket purchase URLs
  - `gameCenterLink` (str): Relative nhl.com game center path
  - `tvBroadcasts` (list): `id`, `market`, `countryCode`, `network`, `sequenceNumber`, `logoUrls`
  - `isHomeGame` (bool): Whether the player's team is at home
  - `homeTeam` / `awayTeam` (object): `id`, `abbrev`, `name{default}`, `teamLogo{light,dark}`, `record` (e.g., "9-2-2")
  - `matchupStats` (object): Player's stats vs. this opponent; `context` (e.g., "careerVsOpponent"), `gamesPlayed`, `goals`, `assists`, `points`, `avgTimeOnIce`
- `currentTeam` (object, optional): `teamCommonName{default}` and `roster{forwards,defensemen,goalies}` (same roster entry fields as `player_bio()`)

## Get Player Stats with player_stats

Retrieves the data behind the stats tab of a player page: a ranked stat line, the last 5 games, career totals and season-by-season totals. Served from `https://api-web.nhle.com/v2/player/{player_id}/player-stats`.

Field sets differ between skaters and goalies: skaters have `goals`, `points`, `shots`, `faceoffWinningPctg`, and so on, while goalies have `wins`, `savePctg`, `goalsAgainstAvg`, `shutouts`, and so on.

```python
from nhlpy import NHLClient

client = NHLClient()
stats = client.players.player_stats(player_id="8478402")

career = stats["careerTotals"]["regularSeason"]
print(f"Career: {career['gamesPlayed']}GP {career['goals']}G {career['assists']}A {career['points']}P")

points = stats["statline"]["regularSeason"].get("current", {}).get("points")
if points:
    print(f"This season: {points['value']} points (league rank {points.get('rank')})")
```

**Parameters:**

- `player_id` (str, required): NHL player ID (e.g., "8478402")

**Response structure:**

- `currentGameTypeId` (int): Game type currently in progress (2 = regular season, 3 = playoffs)
- `statline` (object): Headline stats with league ranks
  - `isPlayerActive` (bool): Whether the player is active
  - `careerSpan` (str): First and last season years (e.g., "2015-2027")
  - `regularSeason` (object):
    - `current` (object, optional): Current-season stats. Only for active players.
    - `career` (object): Career stats
  - `playoffs` (object, optional): Same shape as `regularSeason`, when the player has playoff data
  - Each stat inside `current` / `career` (e.g., `goals`, `assists`, `points`, `pim`, `toi`, `gamesPlayed`; goalies get `wins`, `losses`, `otLosses`, `savePctg`, `goalsAgainstAvg`, `shutouts`) is an object:
    - `value` (number | str): Stat value
    - `rank` (int, optional): League rank
    - `isTied` (bool, optional): Whether the rank is tied
    - `rankType` (str, optional): Rank scope (e.g., "league")
    - `rankLinks` (object, optional): Localized nhl.com / records.nhl.com URLs for the leaderboard
  - `gameTypeId` (int) and `seasonId` (int) are plain values alongside the stats
- `last5` (object):
  - `games` (list): The player's last 5 games; empty for retired players. Each has `gameId`, `gameTypeId`, `seasonId`, `gameDate`, `homeTeam{id,abbrev}`, `awayTeam{id,abbrev}`, `homeScore`, `awayScore`, `homeRoadFlag`, `periodDescriptor`, `gameCenterLink`, and the player's line (`toi`, `goals`, `assists`, `points`, `plusMinus`, `pim`, `powerPlayGoals`, `shorthandedGoals`, `shots`, `shifts`; goalies get `gamesStarted`, `saves`, `shotsAgainst`, `goalsAgainst`, `savePctg`)
  - `totals` (object, optional): Totals across those games. Skaters: `goals`, `assists`, `points`, `plusMinus`, `pim`, `powerPlayGoals`, `shorthandedGoals`, `shots`, `shifts`, `toi`. Goalies: `gamesStarted`, `record` (e.g., "3-1-0"), `shotsAgainst`, `saves`, `goalsAgainst`, `savePctg`, `shutouts`.
- `careerTotals` (object):
  - `regularSeason` (object): Skaters: `gamesPlayed`, `goals`, `assists`, `points`, `plusMinus`, `pim`, `powerPlayGoals`, `powerPlayPoints`, `shorthandedGoals`, `shorthandedPoints`, `gameWinningGoals`, `otGoals`, `shots`, `shootingPctg`, `faceoffWinningPctg`, `avgToi`. Goalies: `gamesPlayed`, `gamesStarted`, `wins`, `losses`, `otLosses`, `goalsAgainst`, `goalsAgainstAvg`, `saves`, `shotsAgainst`, `savePctg`, `shutouts`, `timeOnIce`, `goals`, `assists`, `pim`.
  - `playoffs` (object, optional): Same fields as `regularSeason`
- `seasonTotals` (list): One entry per season, league and game type, including non-NHL leagues
  - `season` (int): Season in YYYYYYYY format
  - `gameTypeId` (int): 2 = regular season, 3 = playoffs
  - `leagueAbbrev` (object): `default` league abbreviation (e.g., "NHL", "OHL")
  - `teamName` / `teamCommonName` / `teamPlaceNameWithPreposition` (object): Localized team names
  - `sequence` (int): Order within the season, for players on multiple teams
  - Plus the same stat fields as `careerTotals.regularSeason`

## Get Player Game Log with player_game_log

Retrieves a player's game-by-game log from `https://api-web.nhle.com/v2/player/{player_id}/game-log/{season}/{game_type}`, or `/game-log/now` for the current season.

This is the v2 counterpart of `client.stats.player_game_log()`. There are two differences:
- Each game includes both teams, the final score, the period the game ended in and the team result (`decision`).
- The full response is returned rather than just the `gameLog` list, so `playerStatsSeasons` tells you which seasons and game types have data.

```python
from nhlpy import NHLClient

client = NHLClient()
log = client.players.player_game_log(player_id="8478402", season="20242025", game_type=2)

for game in log["gameLog"][:5]:
    print(f"{game['gameDate']} {game['awayTeam']['abbrev']} {game['awayScore']} @ "
          f"{game['homeTeam']['abbrev']} {game['homeScore']}: {game['goals']}G {game['assists']}A")

# Current season, no arguments needed
current = client.players.player_game_log(player_id="8478402")
```

**Parameters:**

- `player_id` (str, required): NHL player ID (e.g., "8478402")
- `season` (str, optional): Season in YYYYYYYY format (e.g., "20242025"). Defaults to the current season.
- `game_type` (int, optional): 1 = preseason, 2 = regular season (default), 3 = playoffs. Ignored when `season` is not set.

**Response structure:**

- `seasonId` (int): Season the log covers
- `gameTypeId` (int): Game type the log covers
- `playerStatsSeasons` (list): Seasons with data for this player
  - `season` (int): Season in YYYYYYYY format
  - `gameTypes` (list[int]): Game types with data in that season
- `gameLog` (list): One entry per game, most recent first
  - `id` (int): Game ID
  - `gameTypeId` (int): Game type
  - `gameDate` (str): Date in "YYYY-MM-DD" format
  - `homeRoadFlag` (str): "H" or "R" from the player's perspective
  - `homeTeam` / `awayTeam` (object): `id`, `abbrev`, `commonName{default}`
  - `homeScore` / `awayScore` (int): Final score
  - `decision` (str, optional): Result for the player's team: "W", "L" or "O" (overtime/shootout loss)
  - `periodDescriptor` (object): `number`, `periodType`, `maxRegulationPeriods`
  - `gameCenterLink` (str): Relative nhl.com game center path
  - `toi` (str): Time on ice in "MM:SS"
  - Skater fields: `goals`, `assists`, `points`, `plusMinus`, `pim`, `powerPlayGoals`, `powerPlayPoints`, `shorthandedGoals`, `shorthandedPoints`, `gameWinningGoals`, `otGoals`, `shots`, `shifts`
  - Goalie fields: `gamesStarted`, `shotsAgainst`, `saves`, `goalsAgainst`, `savePctg`, `shutouts`, `goals`, `assists`, `pim`
