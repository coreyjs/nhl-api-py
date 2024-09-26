from typing import List

from nhlpy.http_client import HttpClient


class Teams:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client
        self.base_url = "https://api.nhle.com"
        self.api_ver = "/stats/rest/"

    def teams_info(self, date: str = "now") -> List[dict]:
        """

        :param date: Optional string, in format YYYY-MM-DD.  Defaults to "now".  So,
        the NHL API sometimes uses the "now" string to default to the current date, but in some cases
        such as preseaosn this is defaulting to last years season.  So, to get accurate teams for
        this season, aka whatever year this is, you can supply the timestamp YYYY-MM-DD which should be the start
        of the upcoming season.  For example, 2024-04-18 is for the season 2023-2025 and 2024-10-04 is for the season
        2024-2025.

        Returns a list of dicts with all the teams info.
        Updated in 2.10.0, this pulls from current standings API, aggregates a list of teams
        and their conf/div, joins it with franchise ID, and returns it.  This isnt pretty but
        the NHL API has limitations to return this data in 1 request.
        :return: dict
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
        """
        Returns the roster for the given team and season.
        :param team_abbr: Team abbreviation.  BUF, TOR, etc
        :param season: Season in format YYYYYYYY.  20202021, 20212022, etc
        :return:
        """
        return self.client.get(resource=f"roster/{team_abbr}/{season}").json()

    def all_franchises(self) -> List[dict]:
        """
        Returns a list of all past and current NHL franchises.  This includes ones long forgotten.
        :return:
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/franchise").json()["data"]
