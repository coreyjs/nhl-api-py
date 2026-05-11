# Stats API

The Stats module provides access to player statistics, team statistics, goalie statistics, and advanced query-based stat lookups. Access it via `client.stats` on an `NHLClient` instance.

## Stats: List Game Types Per Season for a Team

Returns every season a team has played along with which game types (regular season, playoffs, etc.) occurred in each season. Useful for discovering which seasons had playoff appearances.

```python
from nhlpy import NHLClient

client = NHLClient()
seasons = client.stats.gametypes_per_season_directory_by_team(team_abbr="TOR")
```

- **Parameters**
  - `team_abbr` (str, required): Three-letter team abbreviation (e.g., "TOR", "BUF", "EDM")
- **Returns**: list of dicts, one per season
  - `season` (int): Season identifier such as 20242025
  - `gameTypes` (list[int]): Game type codes present in that season
    - `2` = Regular season
    - `3` = Playoffs

## Stats: Get Player Career Statistics and Biography

Retrieves a comprehensive player profile including biographical details, career totals, featured stats, recent games, season-by-season totals, and awards.

```python
from nhlpy import NHLClient

client = NHLClient()
player = client.stats.player_career_stats(player_id="8478402")
```

- **Parameters**
  - `player_id` (str, required): Unique NHL player identifier (e.g., "8478402" for Connor McDavid)
- **Returns**: dict with top-level biographical fields and nested stat objects
  - `playerId` (int): Unique player identifier
  - `isActive` (bool): Whether the player is currently active
  - `currentTeamId` (int): Numeric team identifier
  - `currentTeamAbbrev` (str): Three-letter team abbreviation
  - `fullTeamName.default` (str): Full team name (e.g., "Edmonton Oilers")
  - `firstName.default` (str): Player first name
  - `lastName.default` (str): Player last name
  - `sweaterNumber` (int): Jersey number
  - `position` (str): Position code ("C", "L", "R", "D", "G")
  - `headshot` (str): URL to player headshot image
  - `heroImage` (str): URL to player hero image
  - `heightInInches` (int): Height in inches
  - `weightInPounds` (int): Weight in pounds
  - `birthDate` (str): Date of birth
  - `birthCity.default` (str): Birth city
  - `birthCountry` (str): Birth country code
  - `shootsCatches` (str): "L" or "R"
  - `draftDetails` (object): Draft information
    - `year` (int): Draft year
    - `teamAbbrev` (str): Drafting team
    - `round` (int): Draft round
    - `pickInRound` (int): Pick number within the round
    - `overallPick` (int): Overall draft position
  - `playerSlug` (str): URL-safe player name slug
  - `careerTotals.regularSeason` (object): Career regular season totals
    - `gamesPlayed` (int)
    - `goals` (int)
    - `assists` (int)
    - `points` (int)
    - `plusMinus` (int)
    - `pim` (int): Penalty minutes
    - `powerPlayGoals` (int)
    - `powerPlayPoints` (int)
    - `shots` (int)
    - `avgToi` (str): Average time on ice per game
    - `shootingPctg` (float)
    - `gameWinningGoals` (int)
    - `shorthandedGoals` (int)
  - `careerTotals.playoffs` (object): Same fields as regularSeason
  - `featuredStats.season` (int): Season identifier for featured stats
  - `featuredStats.regularSeason.subSeason` (object): Current season stats
  - `featuredStats.regularSeason.career` (object): Career aggregates
  - `last5Games` (list): Most recent five games
    - `gameDate` (str): Game date
    - `gameId` (int): Game identifier
    - `goals` (int)
    - `assists` (int)
    - `points` (int)
    - `plusMinus` (int)
    - `shots` (int)
    - `toi` (str): Time on ice
    - `opponentAbbrev` (str): Opponent team abbreviation
    - `homeRoadFlag` (str): "H" for home, "R" for road
  - `seasonTotals` (list): Per-season stats across all leagues
    - `season` (int): Season identifier
    - `leagueAbbrev` (str): League abbreviation (e.g., "NHL", "AHL")
    - `teamName.default` (str): Team name for that season
    - `gamesPlayed` (int)
    - `goals` (int)
    - `assists` (int)
    - `points` (int)
  - `awards` (list): Player awards history
    - `trophy.default` (str): Trophy name
    - `seasons` (list): Award season details

## Stats: Get Player Game Log for a Season

Returns game-by-game statistics for a specific player in a given season and game type. Each entry represents one game.

```python
from nhlpy import NHLClient

client = NHLClient()
games = client.stats.player_game_log(
    player_id="8478402",
    season_id="20242025",
    game_type=2
)
```

- **Parameters**
  - `player_id` (str, required): Unique NHL player identifier
  - `season_id` (str, required): Season in YYYYYYYY format (e.g., "20242025")
  - `game_type` (int, required): Type of games to retrieve
    - `1` = Preseason
    - `2` = Regular season
    - `3` = Playoffs
- **Returns**: list of dicts, one per game
  - `gameId` (int): Unique game identifier
  - `teamAbbrev` (str): Player's team abbreviation
  - `homeRoadFlag` (str): "H" for home, "R" for road
  - `gameDate` (str): Date of the game
  - `goals` (int)
  - `assists` (int)
  - `commonName.default` (str): Player's team name
  - `opponentCommonName.default` (str): Opponent team name
  - `points` (int)
  - `plusMinus` (int)
  - `powerPlayGoals` (int)
  - `powerPlayPoints` (int)
  - `gameWinningGoals` (int)
  - `otGoals` (int): Overtime goals
  - `shots` (int)
  - `shifts` (int)
  - `shorthandedGoals` (int)
  - `shorthandedPoints` (int)
  - `opponentAbbrev` (str): Opponent abbreviation
  - `pim` (int): Penalty minutes
  - `toi` (str): Time on ice in "MM:SS" format

## Stats: Get Team Summary Statistics

Retrieves aggregated team statistics for one or more seasons. For a single season, set `start_season` equal to `end_season`. Supports pagination, sorting, and Apache Cayenne filter expressions.

```python
from nhlpy import NHLClient

client = NHLClient()

# Single season
teams = client.stats.team_summary(
    start_season="20242025",
    end_season="20242025"
)

# Multiple seasons, playoffs only
teams = client.stats.team_summary(
    start_season="20222023",
    end_season="20242025",
    game_type_id=3,
    is_aggregate=True
)
```

- **Parameters**
  - `start_season` (str, required): Start of range in YYYYYYYY format (e.g., "20242025")
  - `end_season` (str, required): End of range in YYYYYYYY format
  - `game_type_id` (int, default 2): Game type (1=Preseason, 2=Regular season, 3=Playoffs)
  - `is_game` (bool, default False): API parameter for game-level granularity
  - `is_aggregate` (bool, default False): Whether to aggregate stats across seasons
  - `sort_expr` (list[dict], optional): Sorting criteria. Defaults to points DESC, wins DESC, teamId ASC
  - `start` (int, default 0): Pagination offset
  - `limit` (int, default 50): Maximum results to return
  - `fact_cayenne_exp` (str, default "gamesPlayed>1"): Apache Cayenne filter expression
  - `default_cayenne_exp` (str, optional): Overrides the auto-generated Cayenne expression if provided
- **Returns**: list of dicts, one per team
  - `teamFullName` (str): Full team name
  - `teamId` (int): Team identifier
  - `seasonId` (int): Season identifier
  - `gamesPlayed` (int)
  - `wins` (int)
  - `losses` (int)
  - `otLosses` (int): Overtime losses
  - `points` (int)
  - `pointPct` (float): Points percentage
  - `goalsFor` (int)
  - `goalsAgainst` (int)
  - `goalsForPerGame` (float)
  - `goalsAgainstPerGame` (float)
  - `powerPlayPct` (float)
  - `penaltyKillPct` (float)
  - `shotsForPerGame` (float)
  - `shotsAgainstPerGame` (float)
  - `faceoffWinPct` (float)
  - `regulationAndOtWins` (int)
  - `winsInRegulation` (int)
  - `winsInShootout` (int)
  - `teamShutouts` (int)

## Stats: Get Skater Statistics Leaderboard

Returns league-wide skater statistics with pagination and optional franchise filtering. Results are sorted by points descending by default.

```python
from nhlpy import NHLClient

client = NHLClient()

# Top 25 skaters for 2024-2025
skaters = client.stats.skater_stats_summary(
    start_season="20242025",
    end_season="20242025"
)

# Filter by franchise, larger page
skaters = client.stats.skater_stats_summary(
    start_season="20242025",
    end_season="20242025",
    franchise_id="10",
    limit=50
)
```

- **Parameters**
  - `start_season` (str, required): Start of range in YYYYYYYY format
  - `end_season` (str, required): End of range in YYYYYYYY format
  - `franchise_id` (str, optional): Filter to a specific franchise (note: franchise IDs differ from team IDs)
  - `game_type_id` (int, default 2): Game type (1=Preseason, 2=Regular season, 3=Playoffs)
  - `aggregate` (bool, default False): Combine multiple seasons per player when True
  - `sort_expr` (list[dict], optional): Sorting criteria. Defaults to points DESC, gamesPlayed ASC, playerId ASC
  - `start` (int, default 0): Pagination offset
  - `limit` (int, default 25): Maximum results to return
  - `fact_cayenne_exp` (str, default "gamesPlayed>=1"): Apache Cayenne filter expression
  - `default_cayenne_exp` (str, optional): Overrides auto-generated Cayenne expression
- **Returns**: list of dicts, one per skater
  - `skaterFullName` (str): Full player name
  - `playerId` (int): Unique player identifier
  - `lastName` (str)
  - `positionCode` (str): "C", "L", "R", or "D"
  - `teamAbbrevs` (str): Team abbreviation
  - `seasonId` (int)
  - `gamesPlayed` (int)
  - `goals` (int)
  - `assists` (int)
  - `points` (int)
  - `plusMinus` (int)
  - `pointsPerGame` (float)
  - `evGoals` (int): Even-strength goals
  - `evPoints` (int): Even-strength points
  - `ppGoals` (int): Power play goals
  - `ppPoints` (int): Power play points
  - `shGoals` (int): Shorthanded goals
  - `shPoints` (int): Shorthanded points
  - `gameWinningGoals` (int)
  - `otGoals` (int): Overtime goals
  - `shots` (int)
  - `shootingPct` (float)
  - `penaltyMinutes` (int)
  - `faceoffWinPct` (float)
  - `timeOnIcePerGame` (float): Time on ice per game in seconds
  - `shootsCatches` (str): "L" or "R"

## Stats: Advanced Skater Stats with QueryBuilder

Uses the QueryBuilder system to construct complex filtered queries for skater statistics. Supports multiple report types and filter combinations including draft class, position, nationality, and more.

```python
from nhlpy import NHLClient
from nhlpy.api.query.builder import QueryBuilder, QueryContext
from nhlpy.api.query.filters.game_type import GameTypeQuery
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.draft import DraftQuery
from nhlpy.api.query.filters.position import PositionQuery, PositionTypes

client = NHLClient()

filters = [
    GameTypeQuery(game_type="2"),
    DraftQuery(year="2020", draft_round="2"),
    SeasonQuery(season_start="20202021", season_end="20242025"),
    PositionQuery(position=PositionTypes.ALL_FORWARDS),
]

query_builder = QueryBuilder()
query_context: QueryContext = query_builder.build(filters=filters)

data = client.stats.skater_stats_with_query_context(
    report_type="summary",
    query_context=query_context,
    aggregate=True
)
```

- **Parameters**
  - `query_context` (QueryContext, required): Built from QueryBuilder with one or more filters
  - `report_type` (str, required): Type of statistical report. Options:
    - `"summary"` -- General stats overview
    - `"bios"` -- Biographical information
    - `"faceoffpercentages"` -- Faceoff statistics
    - `"faceoffwins"` -- Faceoff win counts
    - `"goalsForAgainst"` -- Goals for/against breakdown
    - `"realtime"` -- Real-time tracking stats
    - `"penalties"` -- Penalty statistics
    - `"penaltykill"` -- Penalty kill stats
    - `"penaltyShots"` -- Penalty shot stats
    - `"powerplay"` -- Power play stats
    - `"puckPossessions"` -- Puck possession metrics
    - `"summaryshooting"` -- Shooting summary
    - `"percentages"` -- Percentage-based stats
    - `"scoringRates"` -- Scoring rate stats
    - `"scoringpergame"` -- Per-game scoring
    - `"shootout"` -- Shootout stats
    - `"shottype"` -- Shot type breakdown
    - `"timeonice"` -- Time on ice breakdown
  - `sort_expr` (list[dict], optional): Custom sorting criteria
  - `aggregate` (bool, default False): Combine multiple seasons per player
  - `start` (int, default 0): Pagination offset
  - `limit` (int, default 25): Maximum results
- **Returns**: dict with a `"data"` key containing a list of skater stat dicts

**Important: Response fields vary by `report_type`.** The only fields common across all report types are:
- `playerId` (int): Unique player identifier
- `skaterFullName` (str): Full display name
- `teamAbbrevs` (str): Three-letter team abbreviation(s)
- `seasonId` (int): Season identifier
- `gamesPlayed` (int): Total games played

For example, `"summary"` returns goals/assists/points/shots, `"realtime"` returns hits/blocks/giveaways, `"penalties"` returns minorPenalties/majorPenalties. Use `client.misc.config()` to discover the available fields for each report type via the `playerReportData` key.

## Stats: Available Query Filters for QueryBuilder

The QueryBuilder accepts a list of filter objects that each implement `QueryBase`. Combine any number of these filters to construct precise queries.

```python
from nhlpy.api.query.filters.game_type import GameTypeQuery
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.position import PositionQuery, PositionTypes
from nhlpy.api.query.filters.draft import DraftQuery
from nhlpy.api.query.filters.franchise import FranchiseQuery
from nhlpy.api.query.filters.nationality import NationalityQuery
```

- **GameTypeQuery(game_type: str)**: Filter by game type ("1"=Preseason, "2"=Regular season, "3"=Playoffs)
- **SeasonQuery(season_start: str, season_end: str)**: Filter by season range (e.g., "20202021", "20242025")
- **PositionQuery(position: PositionTypes)**: Filter by position
  - `PositionTypes.ALL_FORWARDS` ("F") -- All forward positions
  - `PositionTypes.CENTER` ("C")
  - `PositionTypes.LEFT_WING` ("L")
  - `PositionTypes.RIGHT_WING` ("R")
  - `PositionTypes.DEFENSE` ("D")
- **DraftQuery(year: str, draft_round: str = None)**: Filter by draft year and optionally round
- **FranchiseQuery(franchise_id: str)**: Filter by franchise identifier
- **NationalityQuery(nation_code: str)**: Filter by country code (e.g., "CAN", "USA", "SWE", "FIN", "CZE")

## Stats: Get Goalie Statistics Leaderboard

Returns league-wide goalie statistics with multiple report types, pagination, and optional franchise filtering.

```python
from nhlpy import NHLClient

client = NHLClient()

# Default summary stats
goalies = client.stats.goalie_stats_summary(
    start_season="20242025"
)

# Advanced goalie stats for a specific franchise
goalies = client.stats.goalie_stats_summary(
    start_season="20242025",
    stats_type="advanced",
    franchise_id="10"
)
```

- **Parameters**
  - `start_season` (str, required): Start of range in YYYYYYYY format
  - `end_season` (str, optional): End of range. Defaults to `start_season` if not provided
  - `stats_type` (str, default "summary"): Report type. Options:
    - `"summary"` -- General goalie stats
    - `"advanced"` -- Advanced metrics
    - `"bios"` -- Biographical data
    - `"daysrest"` -- Stats by days of rest
    - `"penaltyShots"` -- Penalty shot performance
    - `"savesByStrength"` -- Saves by game situation
    - `"shootout"` -- Shootout performance
    - `"startedVsRelieved"` -- Starter vs. reliever stats
  - `game_type_id` (int, default 2): Game type (1=Preseason, 2=Regular season, 3=Playoffs)
  - `franchise_id` (str, optional): Filter to a specific franchise
  - `aggregate` (bool, default False): Combine multiple seasons per goalie
  - `sort_expr` (list[dict], optional): Custom sorting. Uses NHL Edge defaults per report type
  - `start` (int, default 0): Pagination offset
  - `limit` (int, default 25): Maximum results
  - `fact_cayenne_exp` (str, optional): Apache Cayenne filter expression
  - `default_cayenne_exp` (str, optional): Overrides auto-generated Cayenne expression
- **Returns**: list of dicts, one per goalie (summary report fields shown)
  - `goalieFullName` (str): Full goalie name
  - `playerId` (int): Unique player identifier
  - `lastName` (str)
  - `seasonId` (int)
  - `teamAbbrevs` (str): Team abbreviation
  - `gamesPlayed` (int)
  - `gamesStarted` (int)
  - `wins` (int)
  - `losses` (int)
  - `otLosses` (int): Overtime losses
  - `savePct` (float): Save percentage
  - `goalsAgainstAverage` (float)
  - `saves` (int)
  - `shotsAgainst` (int)
  - `shutouts` (int)
  - `timeOnIce` (int): Time on ice in seconds
  - `goals` (int)
  - `assists` (int)
  - `points` (int)
  - `penaltyMinutes` (int)
  - `shootsCatches` (str): "L" or "R"
