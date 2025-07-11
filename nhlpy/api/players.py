from typing import Dict, Any

from nhlpy.http_client import Endpoint, HttpClient


class Players:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def prospects_by_team(self, team_abbr: str) -> dict:
        """Gets prospects for a specific team.

        Args:
           team_abbr (str): Team abbreviation (e.g., BUF, TOR)

        Returns:
           dict: Prospects data for the specified team.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"prospects/{team_abbr}").json()

    def players_by_team(self, team_abbr: str, season: str) -> Dict[str, Any]:
        """Get the roster/players for the given team and season.  This is the same as teams.roster_by_team(),
        but it's a separate endpoint to avoid confusion.

        This method provides the same functionality as teams.roster_by_team(),
        offering a convenient way to access team rosters through the Players API.

        Args:
            team_abbr (str): Team abbreviation (e.g., BUF, TOR)
            season (str): Season in format YYYYYYYY (e.g., 20202021, 20212022)

        Returns:
            Dict[str, Any]: Dictionary containing roster information for the specified team and season.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"roster/{team_abbr}/{season}").json()
