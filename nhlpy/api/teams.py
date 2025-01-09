from typing import List

from nhlpy.http_client import HttpClient


class Teams:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client
        self.base_url = "https://api.nhle.com"
        self.api_ver = "/stats/rest/"

    def teams_info(self, date: str = "now") -> List[dict]:
        """Get a list of all NHL teams with their conference, division, and franchise information.

        Args:
            date (str, optional): Date in format YYYY-MM-DD. Defaults to "now".
                Note that while the NHL API uses "now" to default to the current date,
                during preseason this may default to last year's season. To get accurate
                teams for the current season, supply a date (YYYY-MM-DD) at the start of
                the upcoming season. For example:
                - 2024-04-18 for season 2023-2024
                - 2024-10-04 for season 2024-2025

        Returns:
            dict: List of dictionaries containing team information including conference,
                division, and franchise ID. Data is aggregated from the current standings
                API and joined with franchise information.

        Note:
            Updated in 2.10.0: Now pulls from current standings API, aggregates team
            conference/division data, and joins with franchise ID. This workaround is
            necessary due to NHL API limitations preventing this data from being retrieved
            in a single request.
        """

        teams_info = self.client.get_by_url(full_resource=f"https://api-web.nhle.com/v1/standings/{date}").json()[
            "standings"
        ]
        teams = []
        for i in teams_info:
            team = {
                "conference": {"abbr": i["conferenceAbbrev"], "name": i["conferenceName"]},
                "division": {"abbr": i["divisionAbbrev"], "name": i["divisionName"]},
                "name": i["teamName"]["default"],
                "common_name": i["teamCommonName"]["default"],
                "abbr": i["teamAbbrev"]["default"],
                "logo": i["teamLogo"],
            }
            teams.append(team)

        # We also need to get "franchise_id", which is different than team_id.  This is used in the stats.
        franchises = self.all_franchises()
        for f in franchises:
            for team in teams:
                if "Canadiens" in f["fullName"] and "Canadiens" in team["name"]:
                    team["franchise_id"] = f["id"]
                    continue

                if f["fullName"] == team["name"]:
                    team["franchise_id"] = f["id"]

        return teams

    def roster(self, team_abbr: str, season: str) -> dict:
        """Returns the roster for the given team and season.

        Args:
            team_abbr (str): Team abbreviation (e.g., BUF, TOR)
            season (str): Season in format YYYYYYYY (e.g., 20202021, 20212022)

        Returns:
            Not specified in original docstring
        """
        return self.client.get(resource=f"roster/{team_abbr}/{season}").json()

    def all_franchises(self) -> List[dict]:
        """Returns a list of all past and current NHL franchises.

        Returns:
           List of all NHL franchises, including historical/defunct teams.
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/franchise").json()["data"]
