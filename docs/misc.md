# Misc API Module

The misc module provides utility and reference data endpoints for the NHL API, including glossary definitions, configuration options, country lists, historical season rules, and draft information. Access it via `client.misc` on an `NHLClient` instance.

## Get NHL Glossary with glossary

Returns all 321 NHL statistical term definitions sorted by full name. Useful for building tooltips, data dictionaries, or looking up stat abbreviations programmatically.

```python
from nhlpy import NHLClient

client = NHLClient()
terms = client.misc.glossary()

for term in terms:
    print(f"{term['abbreviation']}: {term['fullName']} - {term['definition']}")
```

**Parameters:** None

**Returns:** `List[dict]` containing 321 glossary entries.

**Fields for each entry:**

- `id` (int): Unique identifier for the glossary term
- `abbreviation` (str): Short abbreviation used in stats (e.g., "G", "A", "PTS", "TOI")
- `definition` (str): Human-readable description of the stat
- `fullName` (str): Full name of the statistic (e.g., "Goals", "Assists", "Points")
- `firstSeasonForStat` (int): The first NHL season this stat was tracked (e.g., 19171918)
- `languageCode` (str): Language code for the definition (e.g., "en")

## Get Stats Configuration with config

Returns available filter and report options for the stats endpoints. Use this to discover which report types, columns, and aggregations are supported when building stats queries.

```python
from nhlpy import NHLClient

client = NHLClient()
config = client.misc.config()

# List available skater report types
for report_type in config["playerReportData"]:
    print(f"Skater report: {report_type}")

# List available goalie report types
for report_type in config["goalieReportData"]:
    print(f"Goalie report: {report_type}")
```

**Parameters:** None

**Returns:** `dict` with the following top-level keys.

**Response structure:**

- `playerReportData` (object): Keys are skater report type names (e.g., "summary", "realtime", "penalties", "powerplay", "penaltykill", "faceoffpercentages", "goalsForAgainst", "shootout", "percentages", "scoringRates", "scoringpergame", "bios", "faceoffwins", "timeonice")
  - Each key maps to an object describing available columns and options for that report type
- `goalieReportData` (object): Keys are goalie report type names (e.g., "summary", "advanced", "savesByStrength", "shootout", "startedVsRelieved", "daysRest", "penaltyShots", "bios")
  - Each key maps to an object describing available columns and options for that report type
- `teamReportData` (object): Keys are team report type names (e.g., "summary", "penalties", "powerplay", "penaltykill", "faceoffpercentages", "goalsForAgainst", "shootout", "percentages", "realtime", "outshootoutshotby", "goalsbyperiod", "leadingtrailing", "scoringfirst")
  - Each key maps to an object describing available columns and options for that report type
- `aggregatedColumns` (list[str]): Column names that can be aggregated across multiple seasons
- `individualColumns` (list[str]): Column names that apply to individual season records

## Get Hockey Nations with countries

Returns a list of 49 countries associated with NHL hockey, including active and historical nations. Useful for filtering players by nationality or building country selector UIs.

```python
from nhlpy import NHLClient

client = NHLClient()
countries = client.misc.countries()

for country in countries:
    if country["hasPlayerStats"]:
        print(f"{country['countryName']} ({country['id']})")
```

**Parameters:** None

**Returns:** `List[dict]` containing 49 country entries.

**Fields for each entry:**

- `id` (str): Three-letter country code used as the primary identifier (e.g., "CAN", "USA", "SWE")
- `country3Code` (str): Three-letter country code (same as id)
- `countryCode` (str): Two-letter country code (e.g., "CA", "US", "SE")
- `countryName` (str): Full country name (e.g., "Canada", "United States", "Sweden")
- `nationalityName` (str): Nationality demonym (e.g., "Canadian", "American", "Swedish")
- `hasPlayerStats` (int): 1 if the country has players with NHL stats, 0 otherwise
- `isActive` (int): 1 if the country is currently active in the NHL, 0 otherwise
- `imageUrl` (str): URL to the country's flag image (full size)
- `thumbnailUrl` (str): URL to the country's flag image (thumbnail size)

## Get Historical Season Rules with season_specific_rules_and_info

Returns configuration and rules for all 108 historical NHL seasons, from the league's founding to the present. Includes game counts, date ranges, and which rules were in effect for each season.

```python
from nhlpy import NHLClient

client = NHLClient()
seasons = client.misc.season_specific_rules_and_info()

for season in seasons:
    ties = "Yes" if season["tiesInUse"] else "No"
    print(f"{season['formattedSeasonId']}: {season['numberOfGames']} games, Ties: {ties}")
```

**Parameters:** None

**Returns:** `List[dict]` containing 108 season entries.

**Fields for each entry:**

- `id` (int): Season identifier in YYYYYYYY format (e.g., 20242025)
- `formattedSeasonId` (str): Human-readable season format (e.g., "2024-25")
- `numberOfGames` (int): Number of regular season games per team
- `startDate` (str): Season start date
- `regularSeasonEndDate` (str): Last day of the regular season
- `conferencesInUse` (int): 1 if the conference structure was active, 0 otherwise
- `divisionsInUse` (int): 1 if divisions were active, 0 otherwise
- `pointForOTLossInUse` (int): 1 if teams received a point for overtime losses, 0 otherwise
- `tiesInUse` (int): 1 if games could end in a tie, 0 otherwise
- `wildcardInUse` (int): 1 if the wildcard playoff format was active, 0 otherwise
- `totalPlayoffGames` (int): Total number of playoff games played that season
- `totalRegularSeasonGames` (int): Total number of regular season games across all teams
- `olympicsParticipation` (int): 1 if the NHL paused for Olympic participation, 0 otherwise

## Get Draft Years and Rounds with draft_year_and_rounds

Returns a list of all 63 NHL draft years with the number of rounds held in each. Useful for building draft history browsers or validating draft-related queries.

```python
from nhlpy import NHLClient

client = NHLClient()
drafts = client.misc.draft_year_and_rounds()

for draft in drafts:
    print(f"{draft['draftYear']}: {draft['rounds']} rounds")
```

**Parameters:** None

**Returns:** `List[dict]` containing 63 draft year entries.

**Fields for each entry:**

- `id` (int): Unique identifier for the draft year record
- `draftYear` (int): The calendar year of the draft (e.g., 2024)
- `rounds` (int): Number of rounds held in that draft

## Get Where to Watch a Game with how_to_watch

Returns the viewing guide for a game: which broadcasters and streaming services carry it in each country or market. This is the data behind the "How to Watch" modal on nhl.com.

```python
from nhlpy import NHLClient

client = NHLClient()
guide = client.misc.how_to_watch(game_id="2026020220")
print(guide["title"]["default"])
for panel in guide["panels"]:
    # Regional Sports Network panels list broadcasters under homeTeam/awayTeam instead
    print(panel["market"], [b["title"]["default"] for b in panel.get("broadcasters", [])])
```

**Parameters:** `game_id` (str): Game ID. Unknown games return 404 (`ResourceNotFoundException`).

**Response structure:**

- `title` (object): Matchup title (e.g., `{"default": "Oilers @ Islanders"}`)
- `countrySelector` (object): Localized label for the country picker
- `countries` (list): Countries with a viewing guide, each with `id`, `abbr` and localized `name`
- `panels` (list): One panel per market
  - `categoryId` (int): Panel category
  - `market` (str): Market name (e.g., "All Other Countries")
  - `countries` (list[str]): Country codes the panel applies to
  - `title` / `description` (object): Localized text
  - `broadcasters` (list, optional): Broadcasters and streaming options, each with `id`, `desc`, localized `title`, `countryCode` and `weblink`
  - `homeTeam` / `awayTeam` (object, optional): Present on "Regional Sports Network" panels instead of `broadcasters`; each team's regional broadcasters

## Get the NHL Network TV Schedule with tv_schedule

Returns NHL Network programming for a window of dates around the requested date (about two weeks either side).

```python
from nhlpy import NHLClient

client = NHLClient()
schedule = client.misc.tv_schedule()               # around today
schedule = client.misc.tv_schedule(date="2025-01-07")
for show in schedule["broadcasts"][:5]:
    print(show["startTime"], show["title"])
```

**Parameters:** `date` (str, optional): Date in YYYY-MM-DD format. Defaults to `"now"`.

**Response structure:**

- `date` (str): Requested date
- `startDate` / `endDate` (str): First and last date in the returned window
- `broadcasts` (list): Programs
  - `title` (str): Program title
  - `description` (str): Program description
  - `startTime` / `endTime` (str): Start and end time (ISO 8601, no time zone)
  - `durationSeconds` (int): Length in seconds
  - `broadcastStatus` (str): `"LIVE"` for live programs, otherwise empty
  - `broadcastType` (str): Program type
  - `broadcastImageUrl` (str): Program image
  - `houseNumber` (str): Network program ID

## Get Featured Players with player_spotlight

Returns the players currently featured in the nhl.com player spotlight (the player search landing page).

```python
from nhlpy import NHLClient

client = NHLClient()
for player in client.misc.player_spotlight():
    print(f"{player['name']['default']} ({player['teamTriCode']})")
```

**Parameters:** None

**Returns:** `List[dict]`, in display order:

- `playerId` (int): Player ID
- `name` (object): `default` player name
- `playerSlug` (str): URL slug
- `position` (str): Position code
- `sweaterNumber` (int): Jersey number
- `teamId` (int) / `teamTriCode` (str): Team
- `headshot` (str): Headshot image URL
- `teamLogo` (str): Team logo URL
- `sortId` (int): Display order

## Get a Goal's Tracking Replay with goal_replay

Returns the puck and player tracking (PPT) replay details for a goal: scorer, assists, situation and links to the replay data and highlight clip. `event_id` is the play-by-play `eventId` of a goal. For an event that isn't a goal, the response only contains the game details and has no `goal` key.

```python
from nhlpy import NHLClient

client = NHLClient()
pbp = client.game_center.play_by_play(game_id="2024020641")
goal_event = next(p for p in pbp["plays"] if p["typeDescKey"] == "goal")

replay = client.misc.goal_replay(game_id="2024020641", event_id=goal_event["eventId"])
goal = replay["goal"]
print(f"{goal['firstName']['default']} {goal['lastName']['default']} at {goal['timeInPeriod']} ({goal['shotType']})")
```

**Parameters:**

- `game_id` (str): Game ID
- `event_id` (str): Play-by-play `eventId` of the goal

**Response structure:**

- `id` (int): Game ID
- `gameDate` (str): Game date, YYYY-MM-DD
- `gameState` (str) / `gameType` (int): Game state and type
- `awayTeam` / `homeTeam` (object): Teams, with `id`, `abbrev`, localized `name` and `placeName`
- `goal` (object, only for goal events):
  - `eventId` (int): Play-by-play event ID
  - `playerId` (int), `firstName` / `lastName` / `name` (object), `sweaterNumber` (int), `headshot` (str): Scorer
  - `teamAbbrev` (object): Scoring team
  - `periodDescriptor` (object): Period of the goal
  - `timeInPeriod` (str): Time of the goal, MM:SS
  - `situationCode` (str) / `strength` (str): Game situation (e.g., "ev")
  - `shotType` (str): Shot type (e.g., "wrist")
  - `goalModifier` (str): Goal modifier (e.g., "none", "empty-net")
  - `goalsToDate` (int): Scorer's goals this season
  - `assists` (list): Assisting players
  - `awayScore` / `homeScore` (int): Score after the goal
  - `leadingTeamAbbrev` (object): Team leading after the goal
  - `isHome` (bool): Whether the scorer's team is at home
  - `homeTeamDefendingSide` (str): Side the home team defends
  - `pptReplayUrl` (str): URL of the tracking replay data
  - `highlightClip` / `highlightClipFr` (int): Highlight video IDs
  - `highlightClipSharingUrl` / `highlightClipSharingUrlFr` (str): Highlight share URLs
  - `logoUrl` (str): Scoring team logo

