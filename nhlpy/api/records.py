import json
from typing import List, Optional, Tuple, Union

from nhlpy.http_client import Endpoint, HttpClient

# A property name (sorted descending) or a list of (property, "ASC" | "DESC") pairs.
Sort = Union[str, List[Tuple[str, str]]]


class Records:
    """NHL Records API (https://records.nhl.com/site/api/).

    Historical records data: franchises, draft history, awards, Hall of Fame, milestones,
    and hundreds of record lists. Every endpoint returns ``{"data": [...], "total": N}`` and
    accepts the same ``cayenneExp``, ``sort``, ``limit`` and ``start`` query parameters.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    @staticmethod
    def _cayenne(**filters) -> Optional[str]:
        """Builds a Cayenne expression from keyword filters, skipping None values.

        Strings are quoted, everything else is used as-is, e.g.
        ``_cayenne(draftYear=2024, triCode="BUF")`` -> ``draftYear=2024 and triCode="BUF"``.
        """
        clauses = []
        for key, value in filters.items():
            if value is None:
                continue
            if isinstance(value, str):
                value = f'"{value}"'
            clauses.append(f"{key}={value}")
        return " and ".join(clauses) or None

    @staticmethod
    def _params(
        cayenne_exp: Optional[str] = None,
        sort: Optional[Sort] = None,
        limit: Optional[int] = None,
        start: Optional[int] = None,
    ) -> dict:
        params = {}
        if cayenne_exp:
            params["cayenneExp"] = cayenne_exp
        if sort:
            if isinstance(sort, str):
                sort = [(sort, "DESC")]
            params["sort"] = json.dumps([{"property": prop, "direction": direction} for prop, direction in sort])
        if limit is not None:
            params["limit"] = limit
        if start is not None:
            params["start"] = start
        return params

    def _data(self, resource: str, **kwargs) -> List[dict]:
        return self.query(resource, **kwargs).get("data", [])

    def query(
        self,
        resource: str,
        cayenne_exp: Optional[str] = None,
        sort: Optional[Sort] = None,
        limit: Optional[int] = None,
        start: Optional[int] = None,
    ) -> dict:
        """Queries any NHL Records API endpoint by name.

        Use this to reach any of the ~450 records endpoints, including the ones without a
        dedicated method (streaks, fastest goals, international records, etc.). Without a
        ``limit`` the API returns every row, which can be very large for some endpoints.

        Args:
            resource (str): Endpoint path, e.g. "goalie-shutout-streak" or "draft/byTeam/7".
                See the endpoint catalog in docs/records.md.
            cayenne_exp (str, optional): Apache Cayenne filter, e.g. 'franchiseId=7 and gameTypeId=2'.
                Quote string values: 'triCode="BUF"'.
            sort (str | List[Tuple[str, str]], optional): A property name to sort descending by,
                or a list of (property, "ASC"/"DESC") pairs.
            limit (int, optional): Max rows to return.
            start (int, optional): Row offset, for pagination.

        Returns:
            dict: The raw response with ``data`` and ``total``.

        Key Response Fields:
            data (List[dict]): Matching rows. Fields depend on the endpoint.
            total (int): Total matching rows, regardless of limit/start.

        Response Docs:
            docs/records.md

        Example:
            client.records.query("goalie-shutout-streak", limit=10)
            client.records.query("skater-career-scoring-regular-season", cayenne_exp="franchiseId=7", sort="points", limit=10)
        """
        return self.client.get(
            endpoint=Endpoint.API_RECORDS,
            resource=resource,
            query_params=self._params(cayenne_exp=cayenne_exp, sort=sort, limit=limit, start=start),
        ).json()

    def franchises(self) -> List[dict]:
        """Gets every NHL franchise, active and defunct.

        Returns:
            List[dict]: One entry per franchise (about 40).

        Key Response Fields:
            id (int): Franchise ID, used as ``franchise_id`` across the records API.
            fullName (str): Franchise name, e.g. "Buffalo Sabres".
            teamAbbrev (str): Three-letter abbreviation.
            mostRecentTeamId (int): Team ID of the franchise's current/last team.
            firstSeasonId (int): First season, e.g. 19701971.
            lastSeasonId (int | None): Last season, or None if still active.

        Response Docs:
            docs/records.md

        Example:
            client.records.franchises()
        """
        return self._data("franchise")

    def franchise_detail(self, franchise_id: Optional[int] = None, team_id: Optional[int] = None) -> List[dict]:
        """Gets franchise details: captain, coach and GM history, retired numbers.

        Args:
            franchise_id (int, optional): Filter to one franchise.
            team_id (int, optional): Filter by the franchise's most recent team ID (e.g. 7 for BUF).

        Returns:
            List[dict]: Franchise detail entries. History fields are HTML strings.

        Key Response Fields:
            id (int): Franchise ID.
            teamFullName (str): Franchise name.
            teamAbbrev (str): Three-letter abbreviation.
            captainHistory (str): HTML list of captains by season.
            coachingHistory (str): HTML list of head coaches by season.
            generalManagerHistory (str): HTML list of GMs by season.
            retiredNumbersSummary (str): HTML list of retired numbers.
            dateAwarded (str): Date the franchise was awarded.

        Response Docs:
            docs/records.md

        Example:
            client.records.franchise_detail(team_id=7)
        """
        return self._data("franchise-detail", cayenne_exp=self._cayenne(id=franchise_id, mostRecentTeamId=team_id))

    def franchise_totals(
        self, franchise_id: Optional[int] = None, game_type_id: Optional[int] = None, sort: Optional[Sort] = None
    ) -> List[dict]:
        """Gets all-time totals for each franchise, split by game type.

        Args:
            franchise_id (int, optional): Filter to one franchise.
            game_type_id (int, optional): 2 = regular season, 3 = playoffs.
            sort (str | List[Tuple[str, str]], optional): See ``query``.

        Returns:
            List[dict]: One entry per franchise per game type.

        Key Response Fields:
            franchiseId (int): Franchise ID.
            teamName (str): Current team name.
            gameTypeId (int): 2 = regular season, 3 = playoffs.
            gamesPlayed (int): All-time games played.
            wins (int): All-time wins.
            losses (int): All-time losses.
            points (int): All-time points.
            cups (int): Stanley Cups won.

        Response Docs:
            docs/records.md

        Example:
            client.records.franchise_totals(game_type_id=2, sort="wins")
        """
        return self._data(
            "franchise-totals",
            cayenne_exp=self._cayenne(franchiseId=franchise_id, gameTypeId=game_type_id),
            sort=sort,
        )

    def franchise_team_totals(
        self,
        franchise_id: Optional[int] = None,
        team_id: Optional[int] = None,
        game_type_id: Optional[int] = None,
        sort: Optional[Sort] = None,
    ) -> List[dict]:
        """Gets all-time totals for each team identity within a franchise (e.g. Quebec Nordiques and
        Colorado Avalanche are separate rows of the same franchise).

        Args:
            franchise_id (int, optional): Filter to one franchise.
            team_id (int, optional): Filter to one team.
            game_type_id (int, optional): 2 = regular season, 3 = playoffs.
            sort (str | List[Tuple[str, str]], optional): See ``query``.

        Returns:
            List[dict]: One entry per team per game type.

        Key Response Fields:
            franchiseId (int): Franchise ID.
            teamId (int): Team ID.
            teamName (str): Team name.
            triCode (str): Three-letter abbreviation.
            activeTeam (bool): Whether this team identity is current.
            gamesPlayed (int): Games played.
            wins (int): Wins.
            points (int): Points.

        Response Docs:
            docs/records.md

        Example:
            client.records.franchise_team_totals(franchise_id=27)
        """
        return self._data(
            "franchise-team-totals",
            cayenne_exp=self._cayenne(franchiseId=franchise_id, teamId=team_id, gameTypeId=game_type_id),
            sort=sort,
        )

    def franchise_season_results(
        self,
        franchise_id: Optional[int] = None,
        season_id: Optional[int] = None,
        game_type_id: Optional[int] = None,
        sort: Optional[Sort] = None,
        limit: Optional[int] = None,
        start: Optional[int] = None,
    ) -> List[dict]:
        """Gets season-by-season results for franchises: record, finish, and playoff result.

        Args:
            franchise_id (int, optional): Filter to one franchise.
            season_id (int, optional): Filter to one season, e.g. 20232024.
            game_type_id (int, optional): 2 = regular season, 3 = playoffs.
            sort (str | List[Tuple[str, str]], optional): See ``query``.
            limit (int, optional): Max rows to return.
            start (int, optional): Row offset, for pagination.

        Returns:
            List[dict]: One entry per franchise per season per game type.

        Key Response Fields:
            franchiseId (int): Franchise ID.
            seasonId (int): Season, e.g. 20232024.
            teamName (str): Team name that season.
            wins (int): Wins.
            losses (int): Losses.
            points (int): Points.
            divisionSequence (int): Division finish.
            seriesTitle (str): Final playoff round reached, e.g. "NHL Final".
            decision (str): Result of the last series, "W" or "L".

        Response Docs:
            docs/records.md

        Example:
            client.records.franchise_season_results(franchise_id=19, game_type_id=2)
        """
        return self._data(
            "franchise-season-results",
            cayenne_exp=self._cayenne(franchiseId=franchise_id, seasonId=season_id, gameTypeId=game_type_id),
            sort=sort,
            limit=limit,
            start=start,
        )

    def franchise_playoff_appearances(self, franchise_id: Optional[int] = None) -> List[dict]:
        """Gets playoff appearance and Stanley Cup totals for each franchise.

        Args:
            franchise_id (int, optional): Filter to one franchise.

        Returns:
            List[dict]: One entry per franchise.

        Key Response Fields:
            franchiseId (int): Franchise ID.
            franchiseName (str): Franchise name.
            years (int): Seasons in the league.
            playoffSeasons (int): Seasons with a playoff appearance.
            stanleyCupAppearances (int): Stanley Cup Final appearances.
            stanleyCupWins (int): Stanley Cups won.

        Response Docs:
            docs/records.md

        Example:
            client.records.franchise_playoff_appearances(franchise_id=1)
        """
        return self._data("franchise-playoff-appearances", cayenne_exp=self._cayenne(franchiseId=franchise_id))

    def attendance(self, season_id: Optional[int] = None) -> List[dict]:
        """Gets league-wide attendance totals by season.

        Args:
            season_id (int, optional): Filter to one season, e.g. 20232024.

        Returns:
            List[dict]: One entry per season.

        Key Response Fields:
            seasonId (int): Season, e.g. 20232024.
            regularAttendance (int): Regular season attendance.
            playoffAttendance (int): Playoff attendance.
            totalAttendance (int): Combined attendance.

        Response Docs:
            docs/records.md

        Example:
            client.records.attendance(season_id=20232024)
        """
        return self._data("attendance", cayenne_exp=self._cayenne(seasonId=season_id))

    def venues(self, country_code: Optional[str] = None) -> List[dict]:
        """Gets every venue that has hosted an NHL game.

        Args:
            country_code (str, optional): Three-letter country code, e.g. "USA", "CAN".

        Returns:
            List[dict]: One entry per venue (600+).

        Key Response Fields:
            venueId (int): Venue ID.
            venueName (str): Venue name.
            city (str): City.
            stateProvinceCode (str): State/province code.
            countryCode (str): Three-letter country code.
            outdoor (bool): Whether the venue is outdoor.

        Response Docs:
            docs/records.md

        Example:
            client.records.venues(country_code="CAN")
        """
        return self._data("venue", cayenne_exp=self._cayenne(countryCode=country_code))

    def draft(
        self,
        draft_year: Optional[int] = None,
        round_number: Optional[int] = None,
        team_abbr: Optional[str] = None,
        sort: Optional[Sort] = None,
        limit: Optional[int] = None,
        start: Optional[int] = None,
    ) -> List[dict]:
        """Gets NHL draft picks, back to 1963.

        With no filters this returns every pick ever made (13,000+ rows, ~8 MB), so filter or
        pass a ``limit`` where you can.

        Args:
            draft_year (int, optional): Draft year, e.g. 2024.
            round_number (int, optional): Draft round.
            team_abbr (str, optional): Drafting team's three-letter abbreviation, e.g. "BUF".
            sort (str | List[Tuple[str, str]], optional): See ``query``.
            limit (int, optional): Max rows to return.
            start (int, optional): Row offset, for pagination.

        Returns:
            List[dict]: One entry per pick.

        Key Response Fields:
            playerName (str): Drafted player's name.
            playerId (int | None): NHL player ID, if the player has one.
            draftYear (int): Draft year.
            roundNumber (int): Round.
            overallPickNumber (int): Overall pick number.
            triCode (str): Drafting team's abbreviation.
            position (str): Position, e.g. "C", "D", "G".
            amateurClubName (str): Club drafted from.

        Response Docs:
            docs/records.md

        Example:
            client.records.draft(draft_year=2024, round_number=1)
            client.records.draft(team_abbr="BUF", draft_year=2024)
        """
        return self._data(
            "draft",
            cayenne_exp=self._cayenne(draftYear=draft_year, roundNumber=round_number, triCode=team_abbr),
            sort=sort,
            limit=limit,
            start=start,
        )

    def draft_by_team(self, team_id: int) -> List[dict]:
        """Gets every draft pick made by a team.

        Args:
            team_id (int): Team ID, e.g. 7 for BUF.

        Returns:
            List[dict]: One entry per pick. Same fields as ``draft``.

        Key Response Fields:
            playerName (str): Drafted player's name.
            draftYear (int): Draft year.
            roundNumber (int): Round.
            overallPickNumber (int): Overall pick number.
            position (str): Position.
            amateurClubName (str): Club drafted from.

        Response Docs:
            docs/records.md

        Example:
            client.records.draft_by_team(team_id=7)
        """
        return self._data(f"draft/byTeam/{team_id}")

    def draft_lottery_odds(self, draft_year: Optional[int] = None) -> List[dict]:
        """Gets draft lottery format, odds and results by year (1995 onward).

        Args:
            draft_year (int, optional): Draft year, e.g. 2024.

        Returns:
            List[dict]: One entry per lottery year. Content fields are HTML strings.

        Key Response Fields:
            draftYear (int): Draft year.
            formatContent (str): HTML description of the lottery format.
            oddsContent (str): HTML lottery odds (a table in older years, an image in recent years).
            resultNotes (str): Notes on the lottery result.

        Response Docs:
            docs/records.md

        Example:
            client.records.draft_lottery_odds(draft_year=2024)
        """
        return self._data("draft-lottery-odds", cayenne_exp=self._cayenne(draftYear=draft_year))
