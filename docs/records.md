# Records API Module

The records module wraps the NHL Records API (`https://records.nhl.com/site/api/`), which holds historical data: franchise history, the draft back to 1963, attendance, venues, and hundreds of record lists such as streaks and fastest goals. Access it via `client.records` on an `NHLClient` instance.

There are two ways in:

- **Curated methods** (e.g. `draft()`, `franchise_totals()`): typed filters, return `List[dict]` (the response's `data` list).
- **`query()`**: reaches any of the ~445 records endpoints by name and returns the raw `{"data": [...], "total": N}` response. See the [endpoint catalog](#endpoint-catalog) below.

## Common Query Parameters

Every records endpoint accepts the same query parameters. `query()` exposes all of them, and curated methods expose the ones that make sense for that endpoint.

- `cayenne_exp` (str): Apache Cayenne filter, e.g. `'franchiseId=7 and gameTypeId=2'`. Quote string values: `'triCode="BUF"'`.
- `sort` (str or list): A property name to sort descending by (e.g. `"points"`), or a list of `(property, "ASC" | "DESC")` pairs.
- `limit` (int): Max rows to return. **Without a limit the API returns every row**, which is large for some endpoints (`draft` is ~8 MB, `draft-prospect` is ~80 MB).
- `start` (int): Row offset, for pagination. Paging past the end returns `data: []` with the real `total`.

Common IDs:

- `franchise_id`: from `franchises()` (e.g. `1` = Montréal Canadiens, `19` = Buffalo Sabres)
- `team_id`: NHL team ID (e.g. `7` = BUF), the same IDs used elsewhere in the library
- `game_type_id`: `2` = regular season, `3` = playoffs
- `season_id`: 8-digit season (e.g. `20232024`)

## Query Any Endpoint with query

```python
from nhlpy import NHLClient

client = NHLClient()

# Longest goalie shutout streaks
streaks = client.records.query("goalie-shutout-streak", limit=10)
print(streaks["total"])

# Buffalo franchise's all-time top regular season scorers
top = client.records.query(
    "skater-career-scoring-regular-season",
    cayenne_exp="franchiseId=19",
    sort="points",
    limit=10,
)
for p in top["data"]:
    print(f"{p['firstName']} {p['lastName']}: {p['points']}")

# Paginate
page2 = client.records.query("draft", cayenne_exp="draftYear=2024", limit=50, start=50)
```

**Parameters:**

- `resource` (str, required): Endpoint path, e.g. `"goalie-shutout-streak"` or `"draft/byTeam/7"`
- `cayenne_exp`, `sort`, `limit`, `start`: see [Common Query Parameters](#common-query-parameters)

**Returns:** `dict` with `data` (List[dict], fields depend on the endpoint) and `total` (int, total matching rows regardless of `limit`/`start`).

## Get All Franchises with franchises

```python
franchises = client.records.franchises()
active = [f for f in franchises if f["lastSeasonId"] is None]
```

**Parameters:** None

**Returns:** `List[dict]`, one per franchise (about 40, active and defunct).

**Fields for each entry:**

- `id` (int): Franchise ID
- `fullName` (str): Franchise name (e.g. "Buffalo Sabres")
- `teamAbbrev` (str): Three-letter abbreviation
- `teamCommonName` (str): Common name (e.g. "Sabres")
- `teamPlaceName` (str): Place name (e.g. "Buffalo")
- `mostRecentTeamId` (int): Team ID of the franchise's current or last team
- `firstSeasonId` (int): First season (e.g. 19701971)
- `lastSeasonId` (int | None): Last season, or `None` if still active

## Get Franchise Details with franchise_detail

Captain, coach and GM history, plus retired numbers.

```python
sabres = client.records.franchise_detail(team_id=7)[0]
print(sabres["teamFullName"], sabres["dateAwarded"])
```

**Parameters:**

- `franchise_id` (int, optional): Filter to one franchise
- `team_id` (int, optional): Filter by the franchise's most recent team ID

**Returns:** `List[dict]`

**Fields for each entry:**

- `id` (int): Franchise ID
- `teamFullName` (str): Franchise name
- `teamAbbrev` (str): Three-letter abbreviation
- `active` (bool): Whether the franchise is active
- `dateAwarded` (str): Date the franchise was awarded
- `firstSeasonId` (int): First season
- `mostRecentTeamId` (int): Current or last team ID
- `captainHistory` (str): HTML list of captains by season
- `coachingHistory` (str): HTML list of head coaches by season
- `generalManagerHistory` (str): HTML list of GMs by season
- `retiredNumbersSummary` (str): HTML list of retired numbers
- `heroImageUrl` (str): Franchise image URL
- `directoryUrl` (str): Front office directory URL

## Get Franchise Totals with franchise_totals

All-time totals per franchise, one row per game type, under the franchise's current identity.

```python
regular = client.records.franchise_totals(game_type_id=2, sort="wins")
for f in regular[:5]:
    print(f"{f['teamName']}: {f['wins']} wins, {f['cups']} Cups")
```

**Parameters:**

- `franchise_id` (int, optional): Filter to one franchise
- `game_type_id` (int, optional): `2` = regular season, `3` = playoffs
- `sort` (str or list, optional): See [Common Query Parameters](#common-query-parameters)

**Returns:** `List[dict]`

**Fields for each entry:**

- `franchiseId` (int), `teamId` (int), `teamName` (str), `teamAbbrev` (str)
- `gameTypeId` (int): `2` = regular season, `3` = playoffs
- `activeFranchise` (int): `1` if active, `0` if not
- `firstSeasonId` (int), `lastSeasonId` (int | None)
- `gamesPlayed`, `wins`, `losses`, `ties`, `overtimeLosses`, `points` (int)
- `homeWins`, `homeLosses`, `homeTies`, `homeOvertimeLosses` (int)
- `roadWins`, `roadLosses`, `roadTies`, `roadOvertimeLosses` (int)
- `goalsFor`, `goalsAgainst`, `shutouts`, `penaltyMinutes` (int)
- `shootoutWins`, `shootoutLosses` (int)
- `gameWinPctg`, `pointPctg` (float)
- `cups` (int): Stanley Cups won
- `playoffSeasons` (int): Seasons with a playoff appearance
- `seriesPlayed`, `seriesWins`, `seriesLosses` (int), `seriesWinPctg` (float): Playoff series record (playoff rows)

## Get Franchise Team Totals with franchise_team_totals

Like `franchise_totals`, but split by team identity within a franchise (e.g. Quebec Nordiques and Colorado Avalanche are separate rows of franchise 27).

```python
for t in client.records.franchise_team_totals(franchise_id=27, game_type_id=2):
    print(t["teamName"], t["wins"])
```

**Parameters:**

- `franchise_id` (int, optional): Filter to one franchise
- `team_id` (int, optional): Filter to one team
- `game_type_id` (int, optional): `2` = regular season, `3` = playoffs
- `sort` (str or list, optional)

**Returns:** `List[dict]`. Same fields as `franchise_totals`, plus:

- `triCode` (str): Team abbreviation
- `activeTeam` (bool): Whether this team identity is current

## Get Season-by-Season Results with franchise_season_results

```python
seasons = client.records.franchise_season_results(franchise_id=19, game_type_id=2, sort="seasonId", limit=5)
for s in seasons:
    print(s["seasonId"], f"{s['wins']}-{s['losses']}", s["points"], s["seriesTitle"])
```

**Parameters:**

- `franchise_id` (int, optional): Filter to one franchise
- `season_id` (int, optional): Filter to one season
- `game_type_id` (int, optional): `2` = regular season, `3` = playoffs
- `sort`, `limit`, `start` (optional)

**Returns:** `List[dict]`, one per franchise per season per game type (~2,900 rows unfiltered).

**Fields for each entry:**

- `franchiseId`, `teamId` (int), `teamName` (str), `triCode` (str)
- `seasonId` (int), `gameTypeId` (int)
- `gamesPlayed`, `wins`, `losses`, `ties`, `overtimeLosses`, `points` (int)
- `homeWins`, `homeLosses`, `homeTies`, `homeOvertimeLosses` (int)
- `roadWins`, `roadLosses`, `roadTies`, `roadOvertimeLosses` (int)
- `goals`, `goalsAgainst`, `shutouts`, `penaltyMinutes` (int)
- `conferenceName`, `conferenceAbbrev`, `divisionName`, `divisionAbbrev` (str | None)
- `leagueSequence`, `conferenceSequence`, `divisionSequence` (int): Finish position
- `inPlayoffs` (bool)
- `playoffRound`, `finalPlayoffRound` (int)
- `seriesTitle` (str), `seriesAbbrev` (str): Last playoff round reached (e.g. "NHL Final")
- `decision` (str): Result of the last series, `"W"` or `"L"`

## Get Playoff Appearances with franchise_playoff_appearances

```python
habs = client.records.franchise_playoff_appearances(franchise_id=1)[0]
print(f"{habs['franchiseName']}: {habs['stanleyCupWins']} Cups in {habs['stanleyCupAppearances']} Finals")
```

**Parameters:**

- `franchise_id` (int, optional): Filter to one franchise

**Returns:** `List[dict]`

**Fields for each entry:**

- `franchiseId` (int), `franchiseName` (str)
- `firstSeasonId` (int)
- `years` (int): Seasons in the league
- `playoffSeasons` (int): Seasons with a playoff appearance
- `stanleyCupAppearances` (int): Stanley Cup Final appearances
- `stanleyCupWins` (int): Stanley Cups won

## Get League Attendance with attendance

```python
season = client.records.attendance(season_id=20232024)[0]
print(season["totalAttendance"])
```

**Parameters:**

- `season_id` (int, optional): Filter to one season

**Returns:** `List[dict]`, one per season.

**Fields for each entry:**

- `seasonId` (int)
- `regularAttendance` (int): Regular season attendance
- `playoffAttendance` (int): Playoff attendance
- `totalAttendance` (int): Combined attendance

## Get Venues with venues

Every venue that has hosted an NHL game (600+).

```python
canadian = client.records.venues(country_code="CAN")
outdoor = [v for v in client.records.venues() if v["outdoor"]]
```

**Parameters:**

- `country_code` (str, optional): Three-letter country code (e.g. `"USA"`, `"CAN"`)

**Returns:** `List[dict]`

**Fields for each entry:**

- `venueId` (int), `venueName` (str)
- `buildingId` (int)
- `city` (str), `stateProvinceCode` (str), `postalCode` (str | None)
- `countryCode` (str): Three-letter code, `shortCountryCode` (str): Two-letter code
- `outdoor` (bool)

## Get Draft Picks with draft

Every NHL draft pick back to 1963. Unfiltered, this is 13,000+ rows (~8 MB), so filter or pass a `limit`.

```python
first_round = client.records.draft(draft_year=2024, round_number=1, sort=[("overallPickNumber", "ASC")])
for p in first_round:
    print(f"{p['overallPickNumber']}. {p['triCode']} - {p['playerName']} ({p['position']}, {p['amateurClubName']})")

sabres_2024 = client.records.draft(draft_year=2024, team_abbr="BUF")
```

**Parameters:**

- `draft_year` (int, optional): Draft year
- `round_number` (int, optional): Round
- `team_abbr` (str, optional): Drafting team's abbreviation (e.g. `"BUF"`)
- `sort`, `limit`, `start` (optional)

**Returns:** `List[dict]`, one per pick.

**Fields for each entry:**

- `playerName` (str), `firstName` (str), `lastName` (str)
- `playerId` (int | None): NHL player ID, if the player has one
- `draftYear` (int), `draftDate` (str)
- `roundNumber` (int), `pickInRound` (int), `overallPickNumber` (int)
- `triCode` (str): Drafting team's abbreviation
- `draftedByTeamId` (int): Drafting team's ID
- `teamPickHistory` (str): Team(s) that held the pick (e.g. "SJS")
- `position` (str): `"C"`, `"L"`, `"R"`, `"D"` or `"G"`
- `shootsCatches` (str): `"L"` or `"R"`
- `height` (int): Inches
- `weight` (int): Pounds
- `birthDate` (str), `birthPlace` (str), `countryCode` (str)
- `ageInYears` (int): Age at the draft
- `amateurClubName` (str), `amateurLeague` (str): Club and league drafted from
- `supplementalDraft` (str): `"Y"` or `"N"`
- `removedOutright` (str), `removedOutrightWhy` (str | None)

## Get a Team's Draft History with draft_by_team

```python
picks = client.records.draft_by_team(team_id=7)
```

**Parameters:**

- `team_id` (int, required): Team ID (e.g. `7` for BUF)

**Returns:** `List[dict]`. Same fields as `draft`.

## Get Draft Lottery Odds with draft_lottery_odds

Lottery format, odds and results by year, from 1995 onward.

```python
lottery = client.records.draft_lottery_odds(draft_year=2024)[0]
```

**Parameters:**

- `draft_year` (int, optional): Draft year

**Returns:** `List[dict]`, one per lottery year.

**Fields for each entry:**

- `draftYear` (int)
- `formatContent` (str): HTML description of the lottery format
- `oddsContent` (str): HTML lottery odds (a table in older years, an embedded image in recent years)
- `resultNotes` (str): Notes on the result

## Endpoint Catalog

Every records endpoint, grouped by prefix, generated from the API's [WADL](https://records.nhl.com/site/api/application.wadl). Pass any of these to `query()`. Replace `{param}` path segments with a value (e.g. `playoff-series/bySeason/20232024`). Some endpoints are website internals and may not be useful.

### Team (82)

- `team`
- `team-affiliate`
- `team-all-time-shootout-records`
- `team-by-game-stats`
- `team-consecutive-series-won`
- `team-game-consecutive-goals`
- `team-game-record-and-scoring`
- `team-game-record-and-scoring-both-teams`
- `team-non-shutout-streak`
- `team-outdoor-fastest-2-goals-from-period-start-one-team`
- `team-outdoor-fastest-2-goals-one-team`
- `team-outdoor-totals-career`
- `team-outdoor-totals-game-both-teams`
- `team-outdoor-totals-game-one-team`
- `team-outdoor-totals-period-both-teams`
- `team-outdoor-totals-period-one-team`
- `team-period-penalties`
- `team-period-scoring`
- `team-period-scoring-both-teams`
- `team-playoff-clinching-game`
- `team-playoff-clinching-game-season`
- `team-playoff-clinching-game-series`
- `team-playoff-clinching-game-totals`
- `team-playoff-elimination-game`
- `team-playoff-elimination-game-season`
- `team-playoff-elimination-game-series`
- `team-playoff-elimination-game-totals`
- `team-playoff-ot-period-scoring-both-teams`
- `team-playoff-ot-period-scoring-one-team`
- `team-playoff-ot-shot-totals-both-teams`
- `team-playoff-ot-shot-totals-one-team`
- `team-playoff-streak-multiple-seasons`
- `team-playoff-win-streak-one-season`
- `team-record-april`
- `team-record-by-month`
- `team-record-december`
- `team-record-february`
- `team-record-january`
- `team-record-march`
- `team-record-november`
- `team-record-october`
- `team-season-home-loss-streak`
- `team-season-home-loss-streak-start-of-season`
- `team-season-home-point-streak`
- `team-season-home-point-streak-start-of-season`
- `team-season-home-undefeated-streak`
- `team-season-home-undefeated-streak-incl-playoffs`
- `team-season-home-undefeated-streak-start-of-season`
- `team-season-home-win-streak`
- `team-season-home-win-streak-incl-playoffs`
- `team-season-home-win-streak-start-of-season`
- `team-season-home-winless-streak`
- `team-season-home-winless-streak-start-of-season`
- `team-season-loss-streak`
- `team-season-loss-streak-start-of-season`
- `team-season-overtime-games`
- `team-season-point-streak`
- `team-season-point-streak-start-of-season`
- `team-season-record-and-scoring`
- `team-season-road-loss-streak`
- `team-season-road-loss-streak-start-of-season`
- `team-season-road-point-streak`
- `team-season-road-point-streak-start-of-season`
- `team-season-road-undefeated-streak`
- `team-season-road-undefeated-streak-incl-playoffs`
- `team-season-road-undefeated-streak-start-of-season`
- `team-season-road-win-streak`
- `team-season-road-win-streak-incl-playoffs`
- `team-season-road-win-streak-start-of-season`
- `team-season-road-winless-streak`
- `team-season-road-winless-streak-start-of-season`
- `team-season-shootout-records`
- `team-season-shutout-streak`
- `team-season-undefeated-streak`
- `team-season-undefeated-streak-incl-playoffs`
- `team-season-undefeated-streak-start-of-season`
- `team-season-win-streak`
- `team-season-win-streak-incl-playoffs`
- `team-season-win-streak-start-of-season`
- `team-season-winless-streak`
- `team-season-winless-streak-start-of-season`
- `team-stats`

### Skater (71)

- `skater-assist-streak`
- `skater-assist-streak-start-of-season`
- `skater-career-scoring-by-position`
- `skater-career-scoring-playoffs`
- `skater-career-scoring-regular-plus-playoffs`
- `skater-career-scoring-regular-season`
- `skater-first-game-scoring`
- `skater-first-season-game-scoring`
- `skater-franchise-totals`
- `skater-game-assists`
- `skater-game-goals`
- `skater-game-penalties`
- `skater-game-penalty-minutes`
- `skater-game-points`
- `skater-game-power-play-goals`
- `skater-game-shorthanded-goals`
- `skater-game-shots`
- `skater-goal-streak`
- `skater-latest-game-tying-goal`
- `skater-latest-go-ahead-goal`
- `skater-latest-goals`
- `skater-latest-series-clinching-goal`
- `skater-most-goals-1st-50-games`
- `skater-multi-assist-games-career`
- `skater-multi-assist-games-season`
- `skater-multi-goal-games-career`
- `skater-multi-goal-games-season`
- `skater-multi-point-games-career`
- `skater-multi-point-games-season`
- `skater-multipoint-games-career-by-position`
- `skater-outdoor-fastest-goal-from-period-start`
- `skater-outdoor-totals-career`
- `skater-outdoor-totals-game`
- `skater-outdoor-totals-period`
- `skater-period-penalties`
- `skater-period-scoring`
- `skater-period-shots`
- `skater-playoff-clinching-game`
- `skater-playoff-clinching-game-season`
- `skater-playoff-clinching-game-series`
- `skater-playoff-clinching-game-totals`
- `skater-playoff-elimination-game`
- `skater-playoff-elimination-game-season`
- `skater-playoff-elimination-game-series`
- `skater-playoff-elimination-game-totals`
- `skater-playoff-scoring`
- `skater-playoff-streak`
- `skater-point-streak`
- `skater-point-streak-multiple-playoffs`
- `skater-point-streak-start-of-career`
- `skater-real-time-stats-career`
- `skater-real-time-stats-game-blocked-shots`
- `skater-real-time-stats-game-faceoffs`
- `skater-real-time-stats-game-giveaways`
- `skater-real-time-stats-game-hits`
- `skater-real-time-stats-game-missed-shots`
- `skater-real-time-stats-game-shifts`
- `skater-real-time-stats-game-takeaways`
- `skater-real-time-stats-game-time-on-ice`
- `skater-real-time-stats-season`
- `skater-regular-plus-playoff-scoring`
- `skater-regular-season-scoring`
- `skater-rookie-game-scoring`
- `skater-scf-career-scoring`
- `skater-scf-game-scoring`
- `skater-scf-series-scoring`
- `skater-scf-streak`
- `skater-youngest-3-point-games`
- `skater-youngest-4-point-games`
- `skater-youngest-5-point-games`
- `skater-youngest-goal-scorers`

### Coach (49)

- `coach`
- `coach-career-records`
- `coach-career-records-regular-plus-playoffs`
- `coach-career-records/{id}`
- `coach-fewest-games-to-100-playoff-wins`
- `coach-fewest-games-to-100-wins`
- `coach-fewest-games-to-1000-wins`
- `coach-fewest-games-to-150-playoff-wins`
- `coach-fewest-games-to-200-wins`
- `coach-fewest-games-to-300-wins`
- `coach-fewest-games-to-400-wins`
- `coach-fewest-games-to-50-playoff-wins`
- `coach-fewest-games-to-500-wins`
- `coach-fewest-games-to-600-wins`
- `coach-fewest-games-to-700-wins`
- `coach-fewest-games-to-800-wins`
- `coach-fewest-games-to-900-wins`
- `coach-first-game`
- `coach-first-series-win`
- `coach-first-stanley-cup-win`
- `coach-first-win`
- `coach-franchise-records`
- `coach-franchise-records-regular-plus-playoffs`
- `coach-franchise-records/{id}`
- `coach-franchise-season-records`
- `coach-franchise-season-records/{id}`
- `coach-game-seven-career`
- `coach-game-seven-franchise`
- `coach-game-seven-streak`
- `coach-most-wins-100-games`
- `coach-most-wins-100-playoff-games`
- `coach-most-wins-1000-games`
- `coach-most-wins-150-playoff-games`
- `coach-most-wins-200-games`
- `coach-most-wins-200-playoff-games`
- `coach-most-wins-300-games`
- `coach-most-wins-400-games`
- `coach-most-wins-50-playoff-games`
- `coach-most-wins-500-games`
- `coach-most-wins-600-games`
- `coach-most-wins-700-games`
- `coach-most-wins-800-games`
- `coach-most-wins-900-games`
- `coach-playoff-series-totals`
- `coach-playoff-streak`
- `coach-stanley-cup-consecutive-streak`
- `coach-stanley-cup-final-streak`
- `coach-stanley-cup-streak`
- `coach/{id}`

### Goalie (46)

- `goalie-career-scoring`
- `goalie-career-stats`
- `goalie-career-totals-by-franchise`
- `goalie-game-scoring`
- `goalie-game-stats`
- `goalie-home-point-streak`
- `goalie-home-win-streak`
- `goalie-outdoor-totals-career`
- `goalie-outdoor-totals-game`
- `goalie-outdoor-totals-period`
- `goalie-playoff-clinching-game`
- `goalie-playoff-clinching-game-season`
- `goalie-playoff-clinching-game-series`
- `goalie-playoff-clinching-game-totals`
- `goalie-playoff-elimination-game`
- `goalie-playoff-elimination-game-season`
- `goalie-playoff-elimination-game-series`
- `goalie-playoff-elimination-game-totals`
- `goalie-playoff-streak`
- `goalie-playoff-win-streak-multiple-seasons`
- `goalie-point-streak`
- `goalie-road-point-streak`
- `goalie-road-win-streak`
- `goalie-scf-career`
- `goalie-scf-game`
- `goalie-scf-period`
- `goalie-scf-series`
- `goalie-scf-series-shutout-sequence`
- `goalie-scf-series-shutout-streak`
- `goalie-scf-shutout-sequence-multiple-seasons`
- `goalie-scf-streak`
- `goalie-scf-win-streak-multiple-seasons`
- `goalie-season-scoring`
- `goalie-season-stats`
- `goalie-shutout-games-streak-playoffs`
- `goalie-shutout-games-streak-regular-season`
- `goalie-shutout-streak`
- `goalie-stats`
- `goalie-undefeated-streak`
- `goalie-undefeated-streak-first-season`
- `goalie-win-plateaus`
- `goalie-win-streak`
- `goalie-youngest-shutouts`
- `goalie-youngest-winners`
- `goalie_career_stats_incl_playoffs`
- `goalie_season_stats_incl_playoffs`

### International (25)

- `international-both-teams-game-record`
- `international-both-teams-period-record`
- `international-fastest-skater-goals`
- `international-fastest-three-goals-both-teams`
- `international-fastest-three-goals-one-skater`
- `international-fastest-three-goals-one-team`
- `international-fastest-two-goals-both-teams`
- `international-fastest-two-goals-one-skater`
- `international-fastest-two-goals-one-team`
- `international-goaltender-career-record`
- `international-goaltender-game-record`
- `international-goaltender-period-record`
- `international-goaltender-tournament-record`
- `international-playoff-series-details`
- `international-skater-career-record`
- `international-skater-game-record`
- `international-skater-penalty-shots`
- `international-skater-period-record`
- `international-skater-short-handed-goals`
- `international-skater-tournament-record`
- `international-team-all-time-record`
- `international-team-game-record`
- `international-team-period-record`
- `international-team-tournament-record`
- `international-tournament-winner`

### Fastest Goals (18)

- `fastest-2-goals`
- `fastest-2-goals-both-teams`
- `fastest-2-goals-from-period-start-both-teams`
- `fastest-2-goals-from-period-start-one-skater`
- `fastest-2-goals-from-period-start-one-team`
- `fastest-2-goals-one-team`
- `fastest-3-assists`
- `fastest-3-goals`
- `fastest-3-goals-both-teams`
- `fastest-3-goals-from-period-start-both-teams`
- `fastest-3-goals-from-period-start-one-team`
- `fastest-3-goals-one-team`
- `fastest-4-goals-both-teams`
- `fastest-4-goals-one-team`
- `fastest-5-goals-both-teams`
- `fastest-5-goals-one-team`
- `fastest-6-goals-both-teams`
- `fastest-goals-start-of-period`

### Franchise (18)

- `franchise`
- `franchise-all-time-game-7-record`
- `franchise-all-time-overtime-record`
- `franchise-detail`
- `franchise-home-point-streak-vs-franchise`
- `franchise-home-win-streak-vs-franchise`
- `franchise-playoff-appearances`
- `franchise-playoff-streak`
- `franchise-point-streak-vs-franchise`
- `franchise-road-point-streak-vs-franchise`
- `franchise-road-win-streak-vs-franchise`
- `franchise-season-opener-standings`
- `franchise-season-results`
- `franchise-stanley-cup-final-appearance-streak`
- `franchise-stanley-cup-final-win-streak`
- `franchise-team-totals`
- `franchise-totals`
- `franchise-win-streak-vs-franchise`

### Draft (14)

- `draft`
- `draft-lottery-odds`
- `draft-lottery-odds-all-time`
- `draft-lottery-picks`
- `draft-master`
- `draft-prospect`
- `draft-prospect/{id}`
- `draft/amateurTeams`
- `draft/byTeam/{teamId}`
- `draft/countries`
- `draft/roundNumbers`
- `draft/teams`
- `draft/year`
- `draft/{id}`

### Playoff (13)

- `playoff-captains`
- `playoff-franchise-game-by-game-records`
- `playoff-franchise-vs-team`
- `playoff-game-overtime-scoring`
- `playoff-goalie-series-stats`
- `playoff-round-robin-game`
- `playoff-series`
- `playoff-series/byFinal`
- `playoff-series/bySeason/{seasonId}`
- `playoff-series/bySeries/{seriesLetter}`
- `playoff-skater-series-stats`
- `playoff-team-series-stats`
- `playoff-team-series-stats-both-teams`

### All-Star (11)

- `all-star-coach-career-stats`
- `all-star-goaltender-career-stats`
- `all-star-goaltender-game-stats`
- `all-star-goaltender-period-stats`
- `all-star-skater-career-stats`
- `all-star-skater-game-stats`
- `all-star-skater-period-stats`
- `all-star-team-game-stats`
- `all-star-team-period-stats`
- `all-time-record-vs-franchise`
- `all_star_team_position_leaders`

### Milestones (11)

- `milestone-100-point-season`
- `milestone-100-point-season/{id}`
- `milestone-1000-point-career`
- `milestone-1000-point-career/{id}`
- `milestone-5-goal-game`
- `milestone-5-goal-game/{id}`
- `milestone-50-goal-season`
- `milestone-50-goal-season/{id}`
- `milestone-500-goal-career`
- `milestone-500-goal-career/{id}`
- `milestone-tracker`

### General Manager (9)

- `general-manager`
- `general-manager-career-records`
- `general-manager-career-records-regular-plus-playoffs`
- `general-manager-franchise-records`
- `general-manager-franchise-records-regular-plus-playoffs`
- `general-manager-franchise-season-records`
- `general-manager-playoff-streak`
- `general-manager-stanley-cup-final-streak`
- `general-manager/{id}`

### Consecutive (8)

- `consecutive-100-point-seasons`
- `consecutive-20-goal-seasons`
- `consecutive-30-goal-seasons`
- `consecutive-30-win-seasons`
- `consecutive-40-goal-seasons`
- `consecutive-40-win-seasons`
- `consecutive-50-goal-seasons`
- `consecutive-60-goal-seasons`

### Trophies & Awards (7)

- `award-details`
- `award-details/trophy/{trophyId}/season/{seasonId}`
- `award-details/{franchiseId}`
- `trophy`
- `trophy/franchise-trophy-categories`
- `trophy/trophy-categories`
- `trophy/trophy-categories/{franchiseId}`

### Games (4)

- `games-played-active-streak-skaters`
- `games-played-streak-goalies`
- `games-played-streak-skaters`
- `games-shutout-streak`

### Hall of Fame (4)

- `hof/office`
- `hof/office/{officeId}`
- `hof/players`
- `hof/players/{officeId}`

### Olympic (4)

- `olympic-goaltender-career-record`
- `olympic-skater-career-record`
- `olympic-team-all-time-record`
- `olympic-tournament-winner`

### Player (4)

- `player`
- `player-stanley-cup-wins`
- `player/byTeam/{teamId}`
- `player/{id}`

### Stanley Cup Final (4)

- `scf-appearances-streak`
- `scf-franchise-totals`
- `scf-situational-records`
- `scf-team-totals`

### Season (4)

- `season/event`
- `season/event/games`
- `season/event/offseason-games-outside-north-america`
- `season/event/preseason-games-outside-north-america`

### Shootout (4)

- `shootout-goalie-career`
- `shootout-goalie-season`
- `shootout-skaters-career`
- `shootout-skaters-season`

### Comebacks (3)

- `comeback-franchise-three-goal-games`
- `comeback-franchise-wins`
- `comeback-league-wins`

### Other (32)

- `attendance`
- `away-team-record`
- `combine`
- `component-season`
- `content-module-by-season/{templateKey}/{seasonId}`
- `expansion-draft-picks`
- `expansion-draft-rules`
- `game-winning-goals-stanley-cup`
- `home-team-record`
- `league-playoff-year-totals`
- `logo`
- `media-three-star`
- `meta-data/{path:.*}`
- `neutral-site-standings`
- `non-shutout-streak-incl-playoffs`
- `officials`
- `officials/{type}`
- `penalty-shots`
- `phwa-all-star-team`
- `record-category`
- `record-meta-details/{path:.*}`
- `record-video-detail`
- `scoring-plateaus`
- `series-situational-records`
- `special-event`
- `three-or-more-goal-games-career`
- `venue`
- `yearly-playoff-series-details`
- `yearly-playoff-series-details/seasons`
- `{franchiseTricode}/content/module/{templateKey}`
- `{franchiseTricode}/menu`
- `{franchiseTricode}/record-detail`
