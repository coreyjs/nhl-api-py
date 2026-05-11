from typing import Dict, Any

from nhlpy.http_client import Endpoint, HttpClient


class Players:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def prospects_by_team(self, team_abbr: str) -> dict:
        """Gets prospects for a specific team, grouped by position.

        Retrieves the current prospect pool for a given NHL team, returning
        players organized into positional groups.

        Args:
            team_abbr (str): Team abbreviation (e.g., "BUF", "TOR").

        Returns:
            dict: Prospect data grouped by position with the following structure:

                - ``forwards`` (list[dict]): Forward prospects.
                - ``defensemen`` (list[dict]): Defenseman prospects.
                - ``goalies`` (list[dict]): Goalie prospects.

                Each player dict contains:

                - ``id`` (int): Player ID.
                - ``firstName`` (dict): ``{"default": "..."}`` first name.
                - ``lastName`` (dict): ``{"default": "..."}`` last name.
                - ``positionCode`` (str): Position code (e.g., "C", "L", "R", "D", "G").
                - ``birthDate`` (str): Date of birth in YYYY-MM-DD format.
                - ``birthCountry`` (str): Three-letter country code.

        See Also:
            https://api-web.nhle.com/v1/prospects/{team_abbr}
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"prospects/{team_abbr}").json()

    def players_by_team(self, team_abbr: str, season: str) -> Dict[str, Any]:
        """Gets the roster for a given team and season, grouped by position.

        Provides the same data as ``teams.team_roster()``, exposed through the
        Players API for convenience.

        Args:
            team_abbr (str): Team abbreviation (e.g., "BUF", "TOR").
            season (str): Season in YYYYYYYY format (e.g., "20232024").

        Returns:
            Dict[str, Any]: Roster data grouped by position with the following structure:

                - ``forwards`` (list[dict]): Forward players.
                - ``defensemen`` (list[dict]): Defenseman players.
                - ``goalies`` (list[dict]): Goalie players.

                Each player dict contains:

                - ``id`` (int): Player ID.
                - ``firstName`` (dict): ``{"default": "..."}`` first name.
                - ``lastName`` (dict): ``{"default": "..."}`` last name.
                - ``sweaterNumber`` (int): Jersey number.
                - ``positionCode`` (str): Position code (e.g., "C", "L", "R", "D", "G").

        See Also:
            https://api-web.nhle.com/v1/roster/{team_abbr}/{season}
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"roster/{team_abbr}/{season}").json()
