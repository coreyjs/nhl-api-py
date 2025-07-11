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
            "logo": team_data.get("teamLogo", ""),
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
        """Get a list of all NHL teams with their conference, division, and franchise information.

        Args:
            date: Date in format YYYY-MM-DD. Defaults to "now".
                Note that while the NHL API uses "now" to default to the current date,
                during preseason this may default to last year's season. To get accurate
                teams for the current season, supply a date (YYYY-MM-DD) at the start of
                the upcoming season. For example:
                - 2024-04-18 for season 2023-2024
                - 2024-10-04 for season 2024-2025

        Returns:
            List of dictionaries containing team information including conference,
            division, and franchise ID. Data is aggregated from the current standings
            API and joined with franchise information.

        Note:
            Updated in 2.10.0: Now pulls from current standings API, aggregates team
            conference/division data, and joins with franchise ID. This workaround is
            necessary due to NHL API limitations preventing this data from being retrieved
            in a single request.
        """
        standings_data = self._fetch_standings_data(date)
        teams = self._parse_teams_from_standings(standings_data)
        self._enrich_teams_with_franchise_ids(teams)
        return teams

    def team_roster(self, team_abbr: str, season: str) -> Dict[str, Any]:
        """Get the roster for the given team and season.

        Args:
            team_abbr: Team abbreviation (e.g., BUF, TOR)
            season: Season in format YYYYYYYY (e.g., 20202021, 20212022)

        Returns:
            Dictionary containing roster information for the specified team and season.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"roster/{team_abbr}/{season}").json()

    def franchises(self) -> List[Dict[str, Any]]:
        """Get a list of all past and current NHL franchises.

        Returns:
            List of all NHL franchises, including historical/defunct teams.
        """
        # franchise_url = f"{self.NHL_STATS_API_BASE}/en/franchise"
        response = self.client.get(endpoint=Endpoint.API_STATS, resource="en/franchise").json()
        return response.get("data", [])
