from typing import List

from nhlpy.http_client import HttpClient


class Misc:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def glossary(self) -> List[dict]:
        """
        Get the glossary for the NHL API.
        :return: dict
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/glossary?sort=fullName").json()[
            "data"
        ]

    def config(self) -> dict:
        """
        Seems to be various options for the filters?.
        :return: dict
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/config").json()

    def countries(self) -> List[dict]:
        """
        Get the countries for the NHL API.
        :return: dict
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/country").json()["data"]

    def season_specific_rules_and_info(self) -> List[dict]:
        """
        Get the season specific rules and info for the NHL API.
        :return: dict
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/season").json()["data"]

    def draft_year_and_rounds(self) -> List[dict]:
        """
        Get the draft year and rounds for the NHL API.  This only has "id", "draftYear" and "rounds count".
        :return: dict
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/draft").json()["data"]
