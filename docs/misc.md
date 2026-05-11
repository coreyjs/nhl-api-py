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
