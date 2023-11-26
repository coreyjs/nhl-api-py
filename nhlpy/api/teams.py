import json
import importlib.resources

from typing import List

from nhlpy.http_client import HttpClient


class Teams:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client
        self.base_url = "https://api.nhle.com"
        self.api_ver = "/stats/rest/"

    def team_stats_summary(self, lang="en") -> List[dict]:
        """
        I really dont know what this endpoint does.  It returns a list of dicts with team stats.
        :param lang: Language param.  'en' for English, 'fr' for French
        :return:
        """
        return self.client.get_by_url(full_resource=f"{self.base_url}{self.api_ver}{lang}/team/summary").json()["data"]

    def teams_info(self) -> dict:
        """
        Returns a list of dicts with all the teams info.  This is loaded via a harccoded json file.
        :return: dict
        """

        # with importlib.resources.files("nhlpy.data", "teams_20232024.json") as f:
        #     return json.load(f)['teams']

        data_resource = importlib.resources.files("nhlpy") / "data"
        teams_info = json.loads((data_resource / "teams_20232024.json").read_text())["teams"]
        return teams_info

    def roster(self, team_abbr: str, season: str) -> dict:
        """
        Returns the roster for the given team and season.
        :param team_abbr: Team abbreviation.  BUF, TOR, etc
        :param season: Season in format YYYYYYYY.  20202021, 20212022, etc
        :return:
        """
        return self.client.get(resource=f"roster/{team_abbr}/{season}").json()
