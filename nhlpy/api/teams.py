import json
import importlib.resources
from typing import List

from nhlpy.http_client import HttpClient


class Teams:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client
        self.base_url = "https://api.nhle.com"
        self.api_ver = "/stats/rest/"

    def teams_info(self) -> dict:
        """
        Returns a list of dicts with all the teams info.  This is loaded via a harccoded json file.
        :return: dict
        """
        data_resource = importlib.resources.files("nhlpy") / "data"
        teams_info = json.loads((data_resource / "teams_20232024.json").read_text())["teams"]

        # We also need to get "franchise_id", which is different than team_id.  This is used in the stats.
        franchises = self.all_franchises()
        for f in franchises:
            for team in teams_info:
                if "Canadiens" in f["fullName"] and "Canadiens" in team["name"]:
                    team["franchise_id"] = f["id"]
                    continue

                if f["fullName"] == team["name"]:
                    team["franchise_id"] = f["id"]

        return teams_info

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
