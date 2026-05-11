from typing import List

from nhlpy.http_client import HttpClient, Endpoint


class Misc:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def glossary(self) -> List[dict]:
        """Gets the full NHL glossary of statistical terms and abbreviations.

        Returns a list of approximately 321 glossary entries that define every
        abbreviation and term used across the NHL stats API.

        Returns:
            List[dict]: List of glossary entries. Each dict contains:

                - ``id`` (int): Unique glossary entry identifier.
                - ``abbreviation`` (str): Short-form abbreviation (e.g., "GP", "SOG").
                - ``definition`` (str): Human-readable definition of the term.
                - ``fullName`` (str): Full name of the term.

        See Also:
            https://api.nhle.com/stats/rest/en/glossary
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/glossary?sort=fullName").json()
        return response.get("data", [])

    def config(self) -> dict:
        """Gets the stats API configuration, including available report types and filters.

        Returns a dictionary describing the report types available for players,
        goalies, and teams, along with their supported filter options.

        Returns:
            dict: Configuration data with the following top-level keys:

                - ``playerReportData`` (dict): Report type names as keys,
                  each mapping to supported filters and sort options.
                - ``goalieReportData`` (dict): Same structure for goalie reports.
                - ``teamReportData`` (dict): Same structure for team reports.

        See Also:
            https://api.nhle.com/stats/rest/en/config
        """
        return self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/config").json()

    def countries(self) -> List[dict]:
        """Gets the list of countries recognized by the NHL.

        Returns approximately 49 countries that have had players in the NHL,
        including both full names and ISO-style codes.

        Returns:
            List[dict]: List of country entries. Each dict contains:

                - ``id`` (str): Three-letter country code (e.g., "CAN", "USA").
                - ``countryName`` (str): Full country name (e.g., "Canada").
                - ``nationalityName`` (str): Nationality label (e.g., "Canadian").
                - ``countryCode`` (str): Two-letter country code (e.g., "CA", "US").

        See Also:
            https://api.nhle.com/stats/rest/en/country
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/country").json()
        return response.get("data", [])

    def season_specific_rules_and_info(self) -> List[dict]:
        """Gets rules and metadata for every NHL season on record.

        Returns a list of approximately 108 seasons, each describing the
        number of games, conference/division usage, and other rule variations
        for that particular season.

        Returns:
            List[dict]: List of season entries. Each dict contains:

                - ``id`` (int): Season identifier (e.g., 20232024).
                - ``formattedSeasonId`` (str): Human-readable season label
                  (e.g., "2023-24").
                - ``numberOfGames`` (int): Number of regular-season games.
                - ``conferencesInUse`` (int): Whether conferences were active.

        See Also:
            https://api.nhle.com/stats/rest/en/season
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/season").json()
        return response.get("data", [])

    def draft_year_and_rounds(self) -> List[dict]:
        """Gets the number of rounds for each NHL draft year.

        Returns a list of approximately 63 entries covering every draft year
        on record, useful for validating draft round filters in queries.

        Returns:
            List[dict]: List of draft year entries. Each dict contains:

                - ``id`` (int): Unique identifier for the draft year record.
                - ``draftYear`` (int): The calendar year of the draft (e.g., 2023).
                - ``rounds`` (int): Number of rounds held in that draft.

        See Also:
            https://api.nhle.com/stats/rest/en/draft
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/draft").json()
        return response.get("data", [])
