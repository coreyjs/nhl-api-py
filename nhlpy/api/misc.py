from typing import List

from nhlpy.http_client import HttpClient, Endpoint


class Misc:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def glossary(self) -> List[dict]:
        """Get the glossary for the NHL API.

        Returns:
           dict: NHL API glossary data
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/glossary?sort=fullName").json()
        return response.get("data", [])

    def config(self) -> dict:
        """Get available filter options.

        Returns:
           dict: Dictionary of filter options
        """
        return self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/config").json()

    def countries(self) -> List[dict]:
        """Get list of countries from NHL API.

        Returns:
           dict: Dictionary of country data
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/country").json()
        return response.get("data", [])

    def season_specific_rules_and_info(self) -> List[dict]:
        """Get NHL season rules and information.

        Returns:
           dict: Dictionary containing season-specific rules and information
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/season").json()
        return response.get("data", [])

    def draft_year_and_rounds(self) -> List[dict]:
        """Get NHL draft year and round information.

        Returns:
           dict: Draft data containing 'id', 'draftYear', and 'rounds count'
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/draft").json()
        return response.get("data", [])
