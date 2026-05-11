# Schedule API Reference

The `schedule` module provides access to NHL game schedules at various granularities: daily, weekly, monthly, full-season, and team-specific views. It also covers playoff brackets, series schedules, and calendar-formatted data. All methods are accessed via `client.schedule` on an `NHLClient` instance.

## Schedule: Get Daily Schedule

Retrieve the NHL game schedule for a specific date. This method transforms the raw API response, extracting only the games for the requested date from the weekly data returned by the NHL API and adding a `numberOfGames` count.

```python
from nhlpy import NHLClient

client = NHLClient()

# Get today's schedule
today = client.schedule.daily_schedule()

# Get schedule for a specific date
schedule = client.schedule.daily_schedule(date="2024-01-15")

print(f"Games on {schedule['date']}: {schedule['numberOfGames']}")
for game in schedule.get("games", []):
    away = game["awayTeam"]
    home = game["homeTeam"]
    print(f"{away['abbrev']} @ {home['abbrev']} - {game['startTimeUTC']}")
```

**Parameters:**
- `date` (str, optional): Date in `"YYYY-MM-DD"` format. Defaults to today's date if omitted.

**Response top-level fields:**
- `nextStartDate` (str): Next date with scheduled games
- `previousStartDate` (str): Previous date with scheduled games
- `date` (str): The requested date in YYYY-MM-DD format
- `oddsPartners` (None or list): Odds partner information
- `games` (list): Games scheduled for the specified date
- `numberOfGames` (int): Count of games on this date

**`games[]` item fields:**
- `id` (int): Game ID (format: `YYYYTTNNNN`)
- `season` (int): Season identifier (e.g., 20232024)
- `gameType` (int): Game type (1=preseason, 2=regular, 3=playoffs)
- `venue` (object)
  - `default` (str): Arena name
- `neutralSite` (bool): Whether the game is at a neutral site
- `startTimeUTC` (str): ISO 8601 game start time
- `gameState` (str): One of `"FUT"`, `"LIVE"`, `"OFF"`, `"FINAL"`
- `gameScheduleState` (str): Schedule status
- `tvBroadcasts` (list): TV broadcast details
- `awayTeam` (object)
  - `id` (int): Team ID
  - `commonName` (object) with `default` (str): Team common name
  - `placeName` (object) with `default` (str): City/place name
  - `abbrev` (str): Three-letter abbreviation
  - `logo` (str): URL to team logo
  - `darkLogo` (str): URL to dark-mode team logo
  - `awaySplitSquad` (bool): Whether this is a split-squad game for the away team
  - `score` (int): Goals scored (present for completed/in-progress games)
- `homeTeam` (object): Same structure as `awayTeam` but with `homeSplitSquad` instead of `awaySplitSquad`
- `periodDescriptor` (object): Current or final period information
- `gameOutcome` (object): Outcome data for completed games
- `winningGoalie` (object, completed games only)
  - `playerId` (int): Goalie's player ID
  - `firstInitial` (object) with `default` (str): First initial
  - `lastName` (object) with `default` (str): Last name
- `winningGoalScorer` (object, completed games only): Same structure as `winningGoalie`
- `threeMinRecap` (str): URL to three-minute recap video
- `condensedGame` (str): URL to condensed game video
- `gameCenterLink` (str): Relative link to game center page

## Schedule: Get Weekly Schedule

Retrieve the full NHL schedule for a week, including metadata about preseason, regular season, and playoff date ranges. Unlike `daily_schedule`, this returns the raw API response without transformation.

```python
from nhlpy import NHLClient

client = NHLClient()

# Get current week's schedule
week = client.schedule.weekly_schedule()

# Get a specific week's schedule
week = client.schedule.weekly_schedule(date="2024-01-15")

for day in week["gameWeek"]:
    print(f"{day['date']} ({day['dayAbbrev']}): {day['numberOfGames']} games")
    for game in day["games"]:
        print(f"  {game['awayTeam']['abbrev']} @ {game['homeTeam']['abbrev']}")
```

**Parameters:**
- `date` (str, optional): Date in `"YYYY-MM-DD"` format. Defaults to `"now"` (current week) if omitted.

**Response top-level fields:**
- `nextStartDate` (str): Start date of the next week
- `previousStartDate` (str): Start date of the previous week
- `gameWeek` (list): 7 day objects covering the week
- `preSeasonStartDate` (str): Preseason start date
- `regularSeasonStartDate` (str): Regular season start date
- `regularSeasonEndDate` (str): Regular season end date
- `playoffEndDate` (str): Playoff end date
- `numberOfGames` (int): Total games across the week

**`gameWeek[]` item fields:**
- `date` (str): Date in YYYY-MM-DD format
- `dayAbbrev` (str): Day abbreviation (e.g., "MON", "TUE")
- `numberOfGames` (int): Number of games on this day
- `games` (list): Game objects (same structure as `daily_schedule` games)

## Schedule: Get Team Monthly Schedule

Retrieve the schedule for a specific team for a given month. Returns a flat list of game dicts (not wrapped in a top-level object). If no month is provided, defaults to the current month.

```python
from nhlpy import NHLClient

client = NHLClient()

# Get current month's schedule for Buffalo
games = client.schedule.team_monthly_schedule(team_abbr="BUF")

# Get a specific month
games = client.schedule.team_monthly_schedule(team_abbr="TOR", month="2024-01")

for game in games:
    away = game["awayTeam"]
    home = game["homeTeam"]
    print(f"{game['gameDate']}: {away['abbrev']} @ {home['abbrev']} ({game['gameState']})")
```

**Parameters:**
- `team_abbr` (str, required): Three-letter team abbreviation (e.g., `"BUF"`, `"TOR"`, `"NYR"`)
- `month` (str, optional): Month in `"YYYY-MM"` format (e.g., `"2024-01"`). Defaults to current month if omitted.

**Returns:** `List[dict]` -- a list of game dicts (not wrapped in a top-level object).

**Each game dict fields:**
- `id` (int): Game ID
- `season` (int): Season identifier
- `gameType` (int): Game type (1=preseason, 2=regular, 3=playoffs)
- `gameDate` (str): Date in YYYY-MM-DD format
- `venue` (object)
  - `default` (str): Arena name
- `neutralSite` (bool): Whether the game is at a neutral site
- `startTimeUTC` (str): ISO 8601 start time
- `gameState` (str): One of `"FUT"`, `"LIVE"`, `"OFF"`, `"FINAL"`
- `tvBroadcasts` (list): TV broadcast details
- `awayTeam` (object)
  - `commonName` (object) with `default` (str): Team common name
  - `abbrev` (str): Three-letter abbreviation
  - `logo` (str): URL to team logo
  - `score` (int): Goals scored (present for completed games)
- `homeTeam` (object): Same as `awayTeam` plus:
  - `airlineLink` (str): Airline partner link (home games)
  - `airlineDesc` (str): Airline partner description
  - `hotelLink` (str): Hotel partner link (home games)
  - `hotelDesc` (str): Hotel partner description
- `periodDescriptor` (object): Period information
- `gameOutcome` (object): Outcome for completed games
- `winningGoalie` (object): Winning goalie info (playerId, firstInitial, lastName)
- `winningGoalScorer` (object): Winning goal scorer info
- `threeMinRecap` (str): URL to recap video
- `condensedGame` (str): URL to condensed game video
- `gameCenterLink` (str): Relative game center link

## Schedule: Get Team Weekly Schedule

Retrieve the schedule for a specific team for the week containing a given date. Returns a flat list of game dicts. If no date is provided, defaults to the current week.

```python
from nhlpy import NHLClient

client = NHLClient()

# Get current week's games for Edmonton
games = client.schedule.team_weekly_schedule(team_abbr="EDM")

# Get a specific week
games = client.schedule.team_weekly_schedule(team_abbr="EDM", date="2024-03-11")

for game in games:
    print(f"{game['gameDate']}: {game['awayTeam']['abbrev']} @ {game['homeTeam']['abbrev']}")
```

**Parameters:**
- `team_abbr` (str, required): Three-letter team abbreviation (e.g., `"EDM"`, `"BOS"`)
- `date` (str, optional): Date in `"YYYY-MM-DD"` format. Retrieves the week containing this date. Defaults to current week if omitted.

**Returns:** `List[dict]` -- a list of game dicts with the same structure as `team_monthly_schedule` games.

## Schedule: Get Team Full Season Schedule

Retrieve the complete schedule for a team across an entire season, including metadata about adjacent seasons and the team's timezone.

```python
from nhlpy import NHLClient

client = NHLClient()
season_data = client.schedule.team_season_schedule(team_abbr="BUF", season="20232024")

print(f"Timezone: {season_data['clubTimezone']}")
print(f"Total games: {len(season_data['games'])}")

for game in season_data["games"]:
    print(f"{game['gameDate']}: {game['awayTeam']['abbrev']} @ {game['homeTeam']['abbrev']}")
```

**Parameters:**
- `team_abbr` (str, required): Three-letter team abbreviation (e.g., `"BUF"`)
- `season` (str, required): Season in `"YYYYYYYY"` format (e.g., `"20232024"`)

**Response top-level fields:**
- `previousSeason` (int): Previous season identifier (e.g., 20222023)
- `currentSeason` (int): Current season identifier (e.g., 20232024)
- `nextSeason` (int): Next season identifier (e.g., 20242025)
- `clubTimezone` (str): Team's timezone (e.g., "US/Eastern")
- `clubUTCOffset` (str): UTC offset (e.g., "-05:00")
- `games` (list): All games for the season (same game structure as `team_monthly_schedule`)

## Schedule: Get Calendar Schedule

Retrieve the schedule in a calendar view format showing all 32 teams. This provides a high-level overview of all teams and their basic information for a given date range.

```python
from nhlpy import NHLClient

client = NHLClient()
calendar = client.schedule.calendar_schedule(date="2024-01-15")

print(f"Schedule from {calendar['startDate']} to {calendar['endDate']}")
for team in calendar["teams"]:
    print(f"{team['abbrev']}: {team['name']['default']}")
```

**Parameters:**
- `date` (str, required): Date in `"YYYY-MM-DD"` format (e.g., `"2024-01-15"`)

**Response top-level fields:**
- `startDate` (str): Start of the calendar range
- `endDate` (str): End of the calendar range
- `nextStartDate` (str): Next calendar period start
- `previousStartDate` (str): Previous calendar period start
- `teams` (list): All 32 NHL teams

**`teams[]` item fields:**
- `id` (int): Team ID
- `seasonId` (int): Season identifier
- `commonName` (object)
  - `default` (str): Team common name (e.g., "Sabres")
- `abbrev` (str): Three-letter abbreviation (e.g., "BUF")
- `name` (object)
  - `default` (str): Full team name (e.g., "Buffalo Sabres")
- `placeName` (object)
  - `default` (str): City/place name
- `logo` (str): URL to team logo
- `darkLogo` (str): URL to dark-mode team logo
- `french` (bool): Whether this is the French-language version

## Schedule: Get Playoff Carousel

Retrieve an overview of all playoff series up to the current round for a given season, including series results, win totals, and team seeding.

```python
from nhlpy import NHLClient

client = NHLClient()
playoffs = client.schedule.playoff_carousel(season="20232024")

print(f"Current round: {playoffs['currentRound']}")
for rnd in playoffs["rounds"]:
    print(f"\n{rnd['roundLabel']} ({rnd['roundAbbrev']}):")
    for series in rnd["series"]:
        print(f"  {series['seriesLabel']}: {series['seriesLetter']}")
```

**Parameters:**
- `season` (str, required): Season in `"YYYYYYYY"` format (e.g., `"20232024"`)

**Response top-level fields:**
- `seasonId` (int): Season identifier
- `currentRound` (int): Current active playoff round number
- `rounds` (list): All playoff rounds

**`rounds[]` item fields:**
- `roundNumber` (int): Round number (1-4)
- `roundLabel` (str): Human-readable round name (e.g., "First Round")
- `roundAbbrev` (str): Round abbreviation (e.g., `"R1"`, `"R2"`, `"R3"`, `"R4"`)
- `series` (list): All series in this round

**`series[]` item fields:**
- `seriesLetter` (str): Series identifier letter (e.g., "A" through "H" for Round 1)
- `seriesLabel` (str): Human-readable series label
- `seriesLink` (str): Link to series details
- `bottomSeed` (object): Lower-seeded team information
- `topSeed` (object): Higher-seeded team information
- `neededToWin` (int): Wins needed to clinch (4 for NHL playoffs)
- `winningTeamId` (int): ID of the series winner (0 if ongoing)
- `losingTeamId` (int): ID of the series loser (0 if ongoing)

## Schedule: Get Playoff Bracket

Retrieve visual playoff bracket data for a given year, including all 15 series across 4 rounds with team seedings, win counts, and logos.

```python
from nhlpy import NHLClient

client = NHLClient()
bracket = client.schedule.playoff_bracket(year="2024")

for series in bracket["series"]:
    top = series["topSeedTeam"]
    bottom = series["bottomSeedTeam"]
    print(f"Round {series['playoffRound']}: "
          f"({series['topSeedRank']}) {top['abbrev']} {series['topSeedWins']} - "
          f"{series['bottomSeedWins']} {bottom['abbrev']} ({series['bottomSeedRank']})")
```

**Parameters:**
- `year` (str, required): Calendar year the playoffs take place (e.g., `"2024"`)

**Response top-level fields:**
- `bracketLogo` (str): URL to the playoff bracket logo
- `series` (list): All 15 playoff series

**`series[]` item fields:**
- `seriesUrl` (str): URL to series detail page
- `seriesTitle` (str): Human-readable series title
- `seriesAbbrev` (str): Series abbreviation
- `seriesLetter` (str): Series letter identifier
- `playoffRound` (int): Round number (1-4)
- `topSeedRank` (int): Higher seed's rank in their conference
- `topSeedWins` (int): Higher seed's wins in the series
- `bottomSeedRank` (int): Lower seed's rank in their conference
- `bottomSeedWins` (int): Lower seed's wins in the series
- `winningTeamId` (int): ID of the series winner (0 if ongoing)
- `losingTeamId` (int): ID of the series loser (0 if ongoing)
- `topSeedTeam` (object)
  - `id` (int): Team ID
  - `abbrev` (str): Three-letter abbreviation
  - `name` (object) with `default` (str): Full team name
  - `logo` (str): URL to team logo
- `bottomSeedTeam` (object): Same structure as `topSeedTeam`

## Schedule: Get Playoff Series Schedule (Games, Results, Series Status)

Retrieve the full schedule and results for a specific playoff series, including every game with scores, series status after each game, and team seeding info.

**Method**: `client.schedule.playoff_series_schedule(season: str, series: str) -> dict`

**Parameters:**
- `season` (str, required): Season in `"YYYYYYYY"` format (e.g., `"20252026"`)
- `series` (str, required): Series letter identifier (lowercase). `"a"`-`"h"` for Round 1, `"i"`-`"l"` for Round 2, `"m"`-`"n"` for Conference Finals, `"o"` for Stanley Cup Final.

**Response shape:**
- `round` (int): Playoff round number (1-4)
- `roundAbbrev` (str): Round abbreviation (e.g., "R1")
- `roundLabel` (str): Round label (e.g., "1st-round")
- `seriesLetter` (str): Series letter (e.g., "B")
- `neededToWin` (int): Wins required to advance (4)
- `length` (int): Total games played in the series
- `topSeedTeam` (object): Higher-seeded team
  - `id` (int): Team ID
  - `abbrev` (str): Team abbreviation (e.g., "TBL")
  - `name.default` (str): Team name (e.g., "Lightning")
  - `seed` (int): Seed number
  - `record` (str): Series record (e.g., "3-4")
  - `seriesWins` (int): Series wins
  - `logo` (str): Team logo URL
  - `conference.name` (str): Conference name
  - `divisionAbbrev` (str): Division abbreviation
- `bottomSeedTeam` (object): Lower-seeded team (same structure as topSeedTeam)
- `games` (list): List of game objects in the series
  - `id` (int): Game ID (e.g., 2025030121)
  - `gameNumber` (int): Game number within the series (1-7)
  - `ifNecessary` (bool): Whether the game was an "if necessary" game
  - `gameState` (str): "FUT", "LIVE", "OFF"
  - `gameType` (int): Always 3 (playoffs)
  - `season` (int): Season ID
  - `startTimeUTC` (str): ISO 8601 start time
  - `venue.default` (str): Arena name
  - `awayTeam` (object): Away team with abbrev, commonName.default, score
  - `homeTeam` (object): Home team with abbrev, commonName.default, score
  - `seriesStatus` (object): Series state after this game
    - `topSeedWins` (int): Top seed wins after this game
    - `bottomSeedWins` (int): Bottom seed wins after this game
  - `gameOutcome.lastPeriodType` (str): "REG", "OT"
  - `gameCenterLink` (str): Relative URL to game center
  - `tvBroadcasts` (list): TV broadcast info
- `seriesLogo` (str): URL of the playoff series logo
- `fullCoverageUrl` (object): Localized URLs keyed by language code (en, fr, etc.)

**Example:**
```python
from nhlpy import NHLClient

client = NHLClient()
series = client.schedule.playoff_series_schedule(season="20252026", series="b")
top = series["topSeedTeam"]
bot = series["bottomSeedTeam"]
print(f"{top['abbrev']} ({top['record']}) vs {bot['abbrev']} ({bot['record']})")
for game in series["games"]:
    print(f"Game {game['gameNumber']}: {game['awayTeam']['abbrev']} {game['awayTeam']['score']} @ {game['homeTeam']['abbrev']} {game['homeTeam']['score']}")
```
