from typing import List, Dict, Optional, Any
from nhlpy.http_client import Endpoint, HttpClient

# @dataclass
# class TeamInfo:
#     """Data class for team information."""
#
#     name: str
#     common_name: str
#     abbr: str
#     logo: str
#     conference: Dict[str, str]
#     division: Dict[str, str]
#     franchise_id: Optional[int] = None


class Teams:
    """NHL Teams API client."""

    # Constants for API endpoints
    # NHL_WEB_API_BASE = "https://api-web.nhle.com"
    # NHL_STATS_API_BASE = "https://api.nhle.com/stats/rest"

    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client
        # self.base_url = "https://api.nhle.com"
        self.api_ver = "/stats/rest/"

    def _fetch_standings_data(self, date: str) -> List[Dict[str, Any]]:
        """Fetch standings data from NHL API."""
        response = self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"standings/{date}").json()
        return response.get("standings", [])

    def _parse_teams_from_standings(self, standings_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse team information from standings data."""
        teams = []

        for team_data in standings_data:
            team = self._create_team_dict(team_data)
            teams.append(team)

        return teams

    def _create_team_dict(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a standardized team dictionary from API data."""
        return {
            "conference": {"abbr": team_data.get("conferenceAbbrev", ""), "name": team_data.get("conferenceName", "")},
            "division": {"abbr": team_data.get("divisionAbbrev", ""), "name": team_data.get("divisionName", "")},
            "name": self._extract_nested_default(team_data, "teamName"),
            "common_name": self._extract_nested_default(team_data, "teamCommonName"),
            "abbr": self._extract_nested_default(team_data, "teamAbbrev"),
            "place_name": self._extract_nested_default(team_data, "placeName"),
            "logo": team_data.get("teamLogo", ""),
            "dark_logo": team_data.get("teamLogoDark", ""),
        }

    def _extract_nested_default(self, data: Dict[str, Any], key: str) -> str:
        """Extract default value from nested dictionary structure."""
        return data.get(key, {}).get("default", "")

    def _enrich_teams_with_franchise_ids(self, teams: List[Dict[str, Any]]) -> None:
        """Add franchise IDs to teams using franchise data."""
        franchises = self.franchises()
        franchise_lookup = self._create_franchise_lookup(franchises)

        for team in teams:
            team_name = team.get("name", "")
            franchise_id = self._find_franchise_id(team_name, franchise_lookup)
            if franchise_id:
                team["franchise_id"] = franchise_id

    def _create_franchise_lookup(self, franchises: List[Dict[str, Any]]) -> Dict[str, int]:
        """Create a lookup dictionary for franchise names to IDs."""
        lookup = {}
        for franchise in franchises:
            full_name = franchise.get("fullName", "")
            franchise_id = franchise.get("id")
            if full_name and franchise_id:
                lookup[full_name] = franchise_id
        return lookup

    def _find_franchise_id(self, team_name: str, franchise_lookup: Dict[str, int]) -> Optional[int]:
        """Find franchise ID for a given team name."""
        # Direct match first
        if team_name in franchise_lookup:
            return franchise_lookup[team_name]

        # Special case for Canadiens (could be made configurable)
        if "Canadiens" in team_name:
            for franchise_name, franchise_id in franchise_lookup.items():
                if "Canadiens" in franchise_name:
                    return franchise_id
        elif "Utah" in team_name:
            for franchise_name, franchise_id in franchise_lookup.items():
                if "Utah" in franchise_name:
                    return franchise_id

        return None

    def teams(self, date: str = "now") -> List[Dict[str, Any]]:
        """Get a list of all NHL teams with conference, division, and franchise info.

        This method transforms the raw API response by aggregating team data
        from the standings endpoint and enriching it with franchise IDs.

        Args:
            date (str): Date in ``YYYY-MM-DD`` format. Defaults to ``"now"``.
                Note that while the NHL API uses ``"now"`` to default to the
                current date, during preseason this may default to last year's
                season. To get accurate teams for the current season, supply a
                date at the start of the upcoming season. For example:

                - ``"2024-04-18"`` for season 2023-2024
                - ``"2024-10-04"`` for season 2024-2025

        Returns:
            List[Dict[str, Any]]: List of team dicts.

        Key Response Fields (per team dict):
            name (str): Full team name (e.g., ``"Buffalo Sabres"``).
            common_name (str): Common team name (e.g., ``"Sabres"``).
            abbr (str): Three-letter team abbreviation (e.g., ``"BUF"``).
            place_name (str): Team location (e.g., ``"Buffalo"``).
            logo (str): URL of the team logo.
            dark_logo (str): URL of the dark-mode team logo.
            franchise_id (int): Numeric franchise identifier.
            conference.name (str): Conference name (e.g., ``"Eastern"``).
            division.name (str): Division name (e.g., ``"Atlantic"``).

        Note:
            Updated in 2.10.0: Now pulls from the standings API, aggregates
            team conference/division data, and joins with franchise IDs. This
            workaround is necessary due to NHL API limitations preventing this
            data from being retrieved in a single request.

        See Also:
            ``all_time_teams()`` for every team past and present (including
            relocated and defunct teams) with team and franchise IDs.

        Response Docs:
            https://api-web.nhle.com/v1/standings/{date}

        Example:
            client.teams.teams()
            client.teams.teams(date="2024-10-04")
        """
        standings_data = self._fetch_standings_data(date)
        teams = self._parse_teams_from_standings(standings_data)
        self._enrich_teams_with_franchise_ids(teams)
        return teams

    def team_roster(self, team_abbr: str, season: str) -> Dict[str, Any]:
        """Get the roster for the given team and season.

        Args:
            team_abbr (str): Team abbreviation (e.g., ``"BUF"``, ``"TOR"``).
            season (str): Season in ``YYYYYYYY`` format (e.g., ``"20202021"``).

        Returns:
            Dict[str, Any]: Dictionary keyed by position group.

        Key Response Fields:
            forwards (list): List of forward player dicts.
            defensemen (list): List of defenseman player dicts.
            goalies (list): List of goalie player dicts.

        Key Player Fields (per player dict):
            id (int): Unique player identifier.
            firstName.default (str): Player's first name.
            lastName.default (str): Player's last name.
            sweaterNumber (int): Jersey number.
            positionCode (str): Position code (e.g., ``"C"``, ``"D"``, ``"G"``).
            birthDate (str): Date of birth (``YYYY-MM-DD``).
            birthCountry (str): Three-letter country code.

        Response Docs:
            https://api-web.nhle.com/v1/roster/{team}/{season}

        Example:
            client.teams.team_roster(team_abbr="BUF", season="20232024")
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"roster/{team_abbr}/{season}").json()

    def franchises(self) -> List[Dict[str, Any]]:
        """Get a list of all past and current NHL franchises.

        Returns:
            List[Dict[str, Any]]: List of franchise dicts, including
            historical and defunct teams.

        Key Response Fields (per franchise dict):
            id (int): Unique franchise identifier.
            fullName (str): Full franchise name (e.g.,
                ``"Buffalo Sabres"``).
            teamCommonName (str): Common name (e.g., ``"Sabres"``).
            teamPlaceName (str): Place name (e.g., ``"Buffalo"``).

        Response Docs:
            https://api.nhle.com/stats/rest/en/franchise

        Example:
            client.teams.franchises()
        """
        # franchise_url = f"{self.NHL_STATS_API_BASE}/en/franchise"
        response = self.client.get(endpoint=Endpoint.API_STATS, resource="en/franchise").json()
        return response.get("data", [])

    def all_time_teams(self) -> List[Dict[str, Any]]:
        """Get every NHL team past and present, including relocated and defunct teams, with its franchise ID.

        A franchise can have several teams over time (e.g., the Quebec Nordiques
        and Colorado Avalanche are both franchise 27). Team IDs are the ``teamId``
        values used by game feeds and the stats API. Unlike ``teams()``, the
        response uses the NHL's raw field names and has no conference or
        division data.

        Returns:
            List[Dict[str, Any]]: List of team dicts (about 60), returned as the
            NHL publishes them. Placeholder entries such as ``"To be determined"``
            (id 70) and ``"NHL"`` (id 99) have no franchise.

        Key Response Fields (per team dict):
            id (int): Unique team identifier (e.g., ``32`` for the Quebec Nordiques).
            franchiseId (int | None): Franchise identifier, or ``None`` for
                placeholder entries.
            fullName (str): Full team name (e.g., ``"Quebec Nordiques"``).
            triCode (str): Three-letter abbreviation (e.g., ``"QUE"``).
            rawTricode (str): Raw three-letter abbreviation.
            leagueId (int): League identifier.

        See Also:
            ``teams()`` for the current 32 teams with conference and division.

        Response Docs:
            docs/teams.md

        Example:
            client.teams.all_time_teams()
        """
        response = self.client.get(endpoint=Endpoint.API_STATS, resource="en/team").json()
        return response.get("data", [])
