from typing import List

from nhlpy.http_client import HttpClient


class Misc:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def glossary(self) -> List[dict]:
        """Get the glossary for the NHL API.

        Returns:
           dict: NHL API glossary data
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/glossary?sort=fullName").json()[
            "data"
        ]

    def config(self) -> dict:
        """Get available filter options.

        Returns:
           dict: Dictionary of filter options
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/config").json()

    def countries(self) -> List[dict]:
        """Get list of countries from NHL API.

        Returns:
           dict: Dictionary of country data
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/country").json()["data"]

    def season_specific_rules_and_info(self) -> List[dict]:
        """Get NHL season rules and information.

        Returns:
           dict: Dictionary containing season-specific rules and information
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/season").json()["data"]

    def draft_year_and_rounds(self) -> List[dict]:
        """Get NHL draft year and round information.

        Returns:
           dict: Draft data containing 'id', 'draftYear', and 'rounds count'
        """
        return self.client.get_by_url(full_resource="https://api.nhle.com/stats/rest/en/draft").json()["data"]
