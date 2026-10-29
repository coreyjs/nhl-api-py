# Draft API Module

The draft module provides NHL draft data from nhl.com's draft pages: NHL Central Scouting prospect rankings, the picks made in each draft, and the live draft tracker. Access it via `client.draft` on an `NHLClient` instance.

For historical draft data (every pick since 1963, filterable by team, player and so on), see the Records module (`client.records.draft()`). For the number of rounds in each draft year, see `client.misc.draft_year_and_rounds()`.

## Get Central Scouting Prospect Rankings with rankings

Returns NHL Central Scouting's ranking list for a draft class. There are four lists: North American and International skaters, and North American and International goalies.

```python
from nhlpy import NHLClient

client = NHLClient()

# Upcoming/most recent draft, North American skaters
rankings = client.draft.rankings()

# 2025 draft, International goalies
rankings = client.draft.rankings(year="2025", category=4)

for prospect in rankings["rankings"][:5]:
    print(f"{prospect['finalRank']}. {prospect['firstName']} {prospect['lastName']} ({prospect['lastAmateurClub']})")
```

**Parameters:**

- `year` (str, optional): Draft year (e.g., "2025"). Defaults to the upcoming or most recent draft.
- `category` (int, optional): Ranking list, default `1`. It's only used when `year` is given; without a year the API always returns category 1. Invalid values raise `ValueError`.
  - `1`: North American Skater
  - `2`: International Skater
  - `3`: North American Goalie
  - `4`: International Goalie

**Response structure:**

- `draftYear` (int): Draft year of the rankings
- `categoryId` (int): Ranking category ID
- `categoryKey` (str): Category slug (e.g., "north-american-skater")
- `draftYears` (list[int]): Draft years with rankings, newest first
- `categories` (list): All categories, each with `id`, `name` and `consumerKey`
- `rankings` (list): Ranked prospects
  - `firstName` / `lastName` (str): Prospect name (plain strings, not localized objects)
  - `finalRank` (int): Final ranking
  - `midtermRank` (int): Midterm ranking
  - `positionCode` (str): Position code
  - `shootsCatches` (str): Handedness
  - `heightInInches` / `weightInPounds` (int): Size
  - `birthDate` (str): Date of birth, YYYY-MM-DD
  - `birthCity` / `birthStateProvince` (str): Birthplace
  - `birthCountry` (str): Three-letter country code
  - `lastAmateurClub` / `lastAmateurLeague` (str): Current amateur team and league

## Get Draft Picks with picks

Returns the picks made in an NHL draft, for one round or all of them.

```python
from nhlpy import NHLClient

client = NHLClient()

# Most recent draft
draft = client.draft.picks()

# Every pick in 2024
draft = client.draft.picks(year="2024")

# First round of 2024
first_round = client.draft.picks(year="2024", draft_round=1)
for pick in first_round["picks"][:3]:
    print(f"{pick['overallPick']}. {pick['teamAbbrev']} - {pick['firstName']['default']} {pick['lastName']['default']}")
```

**Parameters:**

- `year` (str, optional): Draft year (e.g., "2024"). Defaults to the current or most recent draft.
- `draft_round` (int | str, optional): Round `1`-`7`, or `"all"`, default `"all"`. It's only used when `year` is given; without a year the API returns its default round. Invalid values raise `ValueError`.

**Response structure:**

- `draftYear` (int): Draft year
- `draftYears` (list[int]): Every draft year available
- `selectableRounds` (list[int]): Rounds in this draft
- `state` (str): Draft state (e.g., "over")
- `broadcastStartTimeUTC` (str): Broadcast start time
- `picks` (list): Picks in order
  - `overallPick` (int): Overall pick number
  - `round` (int): Round
  - `pickInRound` (int): Pick number within the round
  - `teamId` (int) / `teamAbbrev` (str): Drafting team
  - `teamName` / `teamCommonName` / `teamPlaceNameWithPreposition` (object): Localized team names
  - `teamLogoLight` / `teamLogoDark` (str): Team logo URLs
  - `displayAbbrev` (object): Pick label
  - `teamPickHistory` (str): Chain of teams that held the pick (for traded picks)
  - `firstName` / `lastName` (object): `default` name of the drafted player
  - `positionCode` (str): Position code
  - `countryCode` (str): Three-letter country code
  - `height` (int): Height in inches
  - `weight` (int): Weight in pounds
  - `amateurClubName` (str): Amateur team
  - `amateurLeague` (str): Amateur league

## Get the Live Draft Tracker with tracker

Returns the data behind the draft tracker widget on nhl.com: the picks in the draft's current round. During a draft it follows the round in progress; once a draft is over it shows round 1. Use `picks()` to get any round of a past draft.

```python
from nhlpy import NHLClient

client = NHLClient()
tracker = client.draft.tracker()
print(f"Round {tracker['round']} ({tracker['state']})")
for pick in tracker["picks"]:
    print(f"{pick['overallPick']}. {pick['teamAbbrev']} - {pick['firstName']['default']} {pick['lastName']['default']}")

# The tracker for a past draft
tracker_2025 = client.draft.tracker(year="2025")
```

**Parameters:**

- `year` (str, optional): Draft year (e.g., "2025"). Defaults to the current or most recent draft.

**Response structure:**

- `currentDraftDate` (str): Date of the draft day, YYYY-MM-DD
- `broadcastStartTimeUTC` (str): Broadcast start time
- `tvBroadcasts` (list): Broadcasts of the draft
- `logoUrl` / `logoFrUrl` (str): Draft logo URLs
- `uiAccentColor` (str): Accent color used by the widget
- `round` (int): Round shown
- `state` (str): Draft state (e.g., "over")
- `picks` (list): Picks in the round
  - `overallPick` / `pickInRound` (int): Pick numbers
  - `state` (str): Pick state
  - `teamId` (int) / `teamAbbrev` (str): Drafting team
  - `teamFullName` / `teamCommonName` / `teamPlaceNameWithPreposition` (object): Localized team names
  - `teamLogoLight` / `teamLogoDark` (str): Team logo URLs
  - `firstName` / `lastName` (object): `default` name of the drafted player
  - `positionCode` (str): Position code
