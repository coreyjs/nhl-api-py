# GameCenter API Reference

The `game_center` module provides access to live and completed NHL game data including boxscores, play-by-play events, shift charts, scoring summaries, and daily scores. All methods are accessed via `client.game_center` on an `NHLClient` instance.

Game IDs follow the format `YYYYTTNNNN` where `YYYY` is the season start year, `TT` is the game type (01=preseason, 02=regular, 03=playoffs), and `NNNN` is the game number (e.g., `2023020280`). Game IDs can be retrieved from any schedule endpoint.

## GameCenter: Get Game Boxscore

Retrieve the full boxscore for a specific NHL game, including team totals and individual player statistics broken down by position group.

```python
from nhlpy import NHLClient

client = NHLClient()
boxscore = client.game_center.boxscore(game_id="2023020280")

# Access team scores
home_score = boxscore["homeTeam"]["score"]
away_score = boxscore["awayTeam"]["score"]

# Access forward stats for the home team
home_forwards = boxscore["playerByGameStats"]["homeTeam"]["forwards"]
for player in home_forwards:
    print(player["name"]["default"], player["goals"], player["assists"])
```

**Parameters:**
- `game_id` (str, required): The NHL game ID (e.g., `"2023020280"`)

**Response top-level fields:**
- `id` (int): Numeric game identifier
- `season` (int): Season identifier (e.g., 20232024)
- `gameType` (int): Game type (1=preseason, 2=regular, 3=playoffs)
- `gameDate` (str): Date in YYYY-MM-DD format
- `venue` (object)
  - `default` (str): Arena name
- `startTimeUTC` (str): ISO 8601 game start time
- `gameState` (str): One of `"FUT"`, `"LIVE"`, `"OFF"`, `"FINAL"`
- `gameScheduleState` (str): Schedule status
- `tvBroadcasts` (list): TV broadcast information

**`awayTeam` / `homeTeam` fields:**
- `id` (int): Team ID
- `commonName` (object)
  - `default` (str): Team common name (e.g., "Sabres")
- `abbrev` (str): Three-letter abbreviation (e.g., "BUF")
- `score` (int): Goals scored
- `sog` (int): Shots on goal
- `logo` (str): URL to team logo
- `darkLogo` (str): URL to dark-mode team logo
- `placeName` (object)
  - `default` (str): City/place name (e.g., "Buffalo")

**`clock` fields:**
- `timeRemaining` (str): Time left in period (e.g., "12:34")
- `secondsRemaining` (int): Seconds left in period
- `running` (bool): Whether the clock is actively running
- `inIntermission` (bool): Whether the game is in intermission

**`playerByGameStats` structure:**
- `awayTeam` (object)
  - `forwards` (list): Forward player stat lines
  - `defense` (list): Defenseman stat lines
  - `goalies` (list): Goalie stat lines
- `homeTeam` (object): Same structure as `awayTeam`

**`gameOutcome` fields:**
- `lastPeriodType` (str): One of `"REG"`, `"OT"`, `"SO"`

## GameCenter: Get Play-by-Play Events

Retrieve detailed play-by-play event data for an NHL game, including every event (shots, goals, faceoffs, penalties, stoppages) with timestamps, players involved, and situational context.

```python
from nhlpy import NHLClient

client = NHLClient()
pbp = client.game_center.play_by_play(game_id="2023020280")

# Iterate over all plays
for play in pbp["plays"]:
    print(play["typeDescKey"], play["timeInPeriod"], play.get("periodDescriptor", {}).get("number"))

# Filter for goals only
goals = [p for p in pbp["plays"] if p["typeDescKey"] == "goal"]
for goal in goals:
    print(f"Goal at {goal['timeInPeriod']} in period {goal['periodDescriptor']['number']}")
```

**Parameters:**
- `game_id` (str, required): The NHL game ID (e.g., `"2023020280"`)

**Response fields (in addition to boxscore-level game metadata):**
- `plays` (list): All play events, typically ~340 items per game
- `rosterSpots` (list): All players on both rosters
- `summary` (object): Game summary data
- `shootoutInUse` (bool): Whether shootout rules apply
- `otInUse` (bool): Whether overtime rules apply

**`plays[]` item fields:**
- `eventId` (int): Unique event identifier
- `periodDescriptor` (object)
  - `number` (int): Period number (1, 2, 3, 4 for OT)
  - `periodType` (str): Period type (e.g., "REG", "OT")
- `timeInPeriod` (str): Time elapsed in period (e.g., "05:32")
- `timeRemaining` (str): Time remaining in period
- `situationCode` (str): Encoded situation (strength, empty net status)
- `typeCode` (int): Numeric event type code
- `typeDescKey` (str): Human-readable event type, one of:
  - `"shot-on-goal"`, `"goal"`, `"period-start"`, `"period-end"`, `"faceoff"`, `"hit"`, `"blocked-shot"`, `"missed-shot"`, `"giveaway"`, `"takeaway"`, `"penalty"`, `"stoppage"`, `"game-end"`
- `sortOrder` (int): Event ordering within the game
- `homeTeamDefendingSide` (str): Which side home team defends (e.g., "left", "right")

**`rosterSpots[]` item fields:**
- `teamId` (int): Team ID
- `playerId` (int): Player ID
- `firstName` (object)
  - `default` (str): First name
- `lastName` (object)
  - `default` (str): Last name
- `sweaterNumber` (int): Jersey number
- `positionCode` (str): Position code (C, L, R, D, G)
- `headshot` (str): URL to player headshot image

## GameCenter: Get Game Matchup and Scoring Summary

Retrieve detailed matchup information for a game, including the scoring summary broken down by period, three stars selections, and penalty summary.

```python
from nhlpy import NHLClient

client = NHLClient()
matchup = client.game_center.match_up(game_id="2023020280")

# Get three stars
for star in matchup["summary"]["threeStars"]:
    print(f"Star #{star['star']}: {star['name']['default']} ({star['teamAbbrev']})")

# Get scoring summary by period
for period in matchup["summary"]["scoring"]:
    for goal in period.get("goals", []):
        print(goal)
```

**Parameters:**
- `game_id` (str, required): The NHL game ID (e.g., `"2023020280"`)

**Response fields (in addition to game metadata):**
- `summary` (object): Contains scoring, three stars, and penalties

**`summary.scoring` structure:**
- List of period objects, each containing:
  - `goals` (list): Goals scored in that period

**`summary.threeStars[]` item fields:**
- `star` (int): Star ranking (1, 2, or 3)
- `playerId` (int): Player ID
- `teamAbbrev` (str): Three-letter team abbreviation
- `headshot` (str): URL to player headshot
- `name` (object)
  - `default` (str): Player full name
- `sweaterNo` (int): Jersey number
- `position` (str): Position code
- `goalsAgainstAverage` (float, goalies only): GAA if the player is a goalie
- `savePctg` (float, goalies only): Save percentage if the player is a goalie

**`summary.penalties` structure:**
- List of period objects, each containing penalty events for that period

## GameCenter: Get Daily Scores

Retrieve scores for all NHL games on a specific date, including goal scorers, game state, and links to recaps. Pass a date string or omit it to get today's scores.

```python
from nhlpy import NHLClient

client = NHLClient()

# Get today's scores
today_scores = client.game_center.daily_scores()

# Get scores for a specific date
scores = client.game_center.daily_scores(date="2024-01-15")

for game in scores["games"]:
    away = game["awayTeam"]
    home = game["homeTeam"]
    print(f"{away['abbrev']} {away['score']} - {home['abbrev']} {home['score']} ({game['gameState']})")
```

**Parameters:**
- `date` (str, optional): Date in `"YYYY-MM-DD"` format. Omit or pass `None` for current day.

**Response top-level fields:**
- `prevDate` (str): Previous date with games
- `currentDate` (str): Requested date
- `nextDate` (str): Next date with games
- `gameWeek` (list): 7-day schedule window
- `oddsPartners` (list): Odds partner information
- `games` (list): All games for the date

**`games[]` item fields:**
- `id` (int): Game ID
- `season` (int): Season identifier
- `gameType` (int): Game type (1=preseason, 2=regular, 3=playoffs)
- `gameDate` (str): Date in YYYY-MM-DD format
- `venue` (object)
  - `default` (str): Arena name
- `startTimeUTC` (str): ISO 8601 start time
- `gameState` (str): One of `"FUT"`, `"LIVE"`, `"OFF"`, `"FINAL"`
- `awayTeam` (object)
  - `id` (int): Team ID
  - `name` (object) with `default` (str): Team name
  - `abbrev` (str): Three-letter abbreviation
  - `score` (int): Goals scored
  - `sog` (int): Shots on goal
  - `logo` (str): URL to team logo
- `homeTeam` (object): Same structure as `awayTeam`
- `gameCenterLink` (str): Relative link to game center page
- `threeMinRecap` (str): URL to three-minute recap video
- `condensedGame` (str): URL to condensed game video
- `clock` (object): Clock state (see boxscore clock fields)
- `periodDescriptor` (object): Current period info
- `gameOutcome` (object): Outcome info if game is final

**`goals[]` item fields (nested within each game):**
- `period` (int): Period number
- `timeInPeriod` (str): Time of goal in period
- `playerId` (int): Scoring player's ID
- `name` (object)
  - `default` (str): Scorer's name
- `goalModifier` (str): Modifier (e.g., empty net, penalty shot)
- `assists` (list): List of assisting players
- `teamAbbrev` (str): Scoring team abbreviation
- `goalsToDate` (int): Scorer's season goal total
- `awayScore` (int): Away team score after this goal
- `homeScore` (int): Home team score after this goal
- `strength` (str): One of `"ev"` (even strength), `"pp"` (power play), `"sh"` (shorthanded)

## GameCenter: Get Shift Chart Data

Retrieve shift-by-shift data for every player in a game, useful for building shift charts or analyzing time-on-ice patterns. By default, `eventDetails` are excluded from the response.

```python
from nhlpy import NHLClient

client = NHLClient()

# Get shift data with default exclusions
shifts = client.game_center.shift_chart_data(game_id="2023020280")

print(f"Total shifts: {shifts['total']}")
for shift in shifts["data"][:5]:
    print(f"{shift['firstName']} {shift['lastName']} - Period {shift['period']}, "
          f"{shift['startTime']}-{shift['endTime']} ({shift['duration']})")

# Get shift data without any exclusions
shifts_full = client.game_center.shift_chart_data(game_id="2023020280", excludes=[])
```

**Parameters:**
- `game_id` (str, required): The NHL game ID (e.g., `"2023020280"`)
- `excludes` (List[str], optional): Fields to exclude from the response. Defaults to `["eventDetails"]`. Pass an empty list to include all fields.

**Response top-level fields:**
- `data` (list): All shift records, typically ~740 items per game
- `total` (int): Total number of shift records

**`data[]` item fields:**
- `id` (int): Shift record ID
- `duration` (str): Shift duration in `"MM:SS"` format
- `endTime` (str): Shift end time in period
- `startTime` (str): Shift start time in period
- `firstName` (str): Player first name
- `lastName` (str): Player last name
- `gameId` (int): Game ID
- `period` (int): Period number
- `playerId` (int): Player ID
- `shiftNumber` (int): Sequential shift number for this player
- `teamAbbrev` (str): Three-letter team abbreviation
- `teamId` (int): Team ID
- `teamName` (str): Full team name
- `typeCode` (int): Shift type code
- `hexValue` (str): Team color hex code (e.g., "#003087")

## GameCenter: Get Season Series and Game Stats

Retrieve the season series between two teams, linescore, per-period shot totals, team comparison stats, and game report URLs for a specific game. This corresponds to the "right rail" data on the NHL website.

```python
from nhlpy import NHLClient

client = NHLClient()
rail = client.game_center.season_series_matchup(game_id="2023020280")

# Season series wins
wins = rail["seasonSeriesWins"]
print(f"Away wins: {wins['awayTeamWins']}, Home wins: {wins['homeTeamWins']}")

# Team comparison stats
for stat in rail["teamGameStats"]:
    print(f"{stat['category']}: Away={stat['awayValue']} Home={stat['homeValue']}")

# Access game report URLs
reports = rail["gameReports"]
print(f"Game summary PDF: {reports['gameSummary']}")
```

**Parameters:**
- `game_id` (str, required): The NHL game ID (e.g., `"2023020280"`)

**Response top-level fields:**
- `seasonSeries` (list): Previous matchup games between the two teams this season
- `seasonSeriesWins` (object)
  - `awayTeamWins` (int): Away team's wins in the season series
  - `homeTeamWins` (int): Home team's wins in the season series
- `gameInfo` (object)
  - `referees` (list): Referee names
  - `linesmen` (list): Linesman names
  - `scratches` (object): Healthy scratches for both teams
  - `headCoach` (object): Head coaches for both teams
- `gameVideo` (object): Video links
- `linescore` (object)
  - `byPeriod` (list): Score by period
  - `totals` (object): Final score totals
- `shotsByPeriod` (list): Shot counts per period for each team

**`teamGameStats[]` item fields:**
- `category` (str): Stat category, one of:
  - `"sog"` (shots on goal)
  - `"faceoffWinningPctg"` (faceoff win percentage)
  - `"powerPlay"` (power play results, e.g., "1/3")
  - `"pim"` (penalty minutes)
  - `"hits"`, `"blockedShots"`, `"giveaways"`, `"takeaways"`
- `awayValue` (int or str): Away team's value for this stat
- `homeValue` (int or str): Home team's value for this stat

**`gameReports` fields:**
- `gameSummary` (str): URL to game summary PDF
- `eventSummary` (str): URL to event summary PDF
- `playByPlay` (str): URL to play-by-play PDF
- `faceoffSummary` (str): URL to faceoff summary PDF
- `faceoffComparison` (str): URL to faceoff comparison PDF
- `rosters` (str): URL to game rosters PDF
- `shotSummary` (str): URL to shot summary PDF
- `shiftChart` (str): URL to shift chart PDF
- `toiAway` (str): URL to away team time-on-ice PDF
- `toiHome` (str): URL to home team time-on-ice PDF

## GameCenter: Get Game Story and Recap

Retrieve the game story/recap including a scoring summary, three stars, team comparison stats, and shootout data if applicable. Similar to the matchup endpoint but includes team game stats and shootout information.

```python
from nhlpy import NHLClient

client = NHLClient()
story = client.game_center.game_story(game_id="2023020280")

# Team comparison stats
for stat in story["summary"]["teamGameStats"]:
    print(f"{stat['category']}: {stat['awayValue']} vs {stat['homeValue']}")

# Three stars (note: uses simple name string, not object)
for star in story["summary"]["threeStars"]:
    print(f"Star #{star['star']}: {star['name']}")
```

**Parameters:**
- `game_id` (str, required): The NHL game ID (e.g., `"2023020280"`)

**Response fields (in addition to game metadata):**
- `summary` (object): Contains all recap data

**`summary` sub-fields:**
- `scoring` (list): Scoring summary by period
- `threeStars` (list): Three stars of the game
  - Note: Uses a simple `name` string (not an object like `match_up`)
- `penalties` (list): Penalty summary by period
- `teamGameStats` (list): Team comparison stats
  - `category` (str): Stat name (e.g., `"sog"`, `"faceoffWinningPctg"`, `"powerPlay"`)
  - `awayValue` (int or str): Away team's value
  - `homeValue` (int or str): Home team's value
- `shootout` (list): Shootout attempts if the game went to a shootout
