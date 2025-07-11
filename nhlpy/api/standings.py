from typing import List, Optional

from nhlpy.http_client import Endpoint


class Standings:
    def __init__(self, http_client):
        self.client = http_client

    def league_standings(self, date: Optional[str] = None, season: Optional[str] = None) -> dict:
        """Gets league standings for a specified season or date.

        Retrieves NHL standings either for a specific date or for the end of a season.
        If both parameters are provided, season takes precedence.

        Args:
            date (str, optional): Date in YYYY-MM-DD format. Defaults to current date.
            season (str, optional): Season identifier to get final standings.
                Takes precedence over date parameter if both are provided.

        Returns:
            dict: Dictionary containing league standings data
        """

        # We need to look up the last date of the season and use that as the date, since it doesnt seem to take
        # season as a param.
        if season:
            seasons = self.season_standing_manifest()

            season_data = next((s for s in seasons if s.get("id") == int(season)), None)
            if not season_data:
                raise ValueError(f"Invalid Season Id {season}")
            date = season_data.get("standingsEnd")

        res = date if date else "now"

        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"standings/{res}").json()

    def season_standing_manifest(self) -> List[dict]:
        """Gets metadata for all NHL seasons.
        Returns information about what seems like every season.  Start date, end date, etc.

        Args:
           None

        Returns:
           dict: Season metadata including dates, conference/division usage, and scoring rules.

        Example:
           Response format:
           [{
               "id": 20232024,
               "conferencesInUse": true,
               "divisionsInUse": true,
               "pointForOTlossInUse": true,
               "regulationWinsInUse": true,
               "rowInUse": true,
               "standingsEnd": "2023-11-10",
               "standingsStart": "2023-10-10",
               "tiesInUse": false,
               "wildcardInUse": true
           }]
        """
        response = self.client.get(endpoint=Endpoint.API_WEB_V1, resource="standings-season").json()
        return response.get("seasons", [])
