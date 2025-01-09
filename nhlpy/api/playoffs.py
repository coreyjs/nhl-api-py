from nhlpy.http_client import HttpClient


class Playoffs:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def carousel(self, season: str) -> dict:
        """Gets list of all series games up to current playoff round.

        Args:
           season (str): Season in YYYYYYYY format (e.g., "20232024")

        Returns:
           dict: Playoff series data for the specified season.

        Example:
           API endpoint: https://api-web.nhle.com/v1/playoff-series/carousel/20232024/
        """
        return self.client.get(resource=f"playoff-series/carousel/{season}").json()

    def schedule(self, season: str, series: str) -> dict:
        """Returns the schedule for a specified playoff series.

        Args:
           season (str): Season in YYYYYYYY format (e.g., "20232024")
           series (str): Series identifier (a-h) for Round 1

        Returns:
           dict: Schedule data for the specified playoff series.

        Example:
           API endpoint: https://api-web.nhle.com/v1/schedule/playoff-series/20232024/a/
        """

        return self.client.get(resource=f"schedule/playoff-series/{season}/{series}").json()

    def bracket(self, year: str) -> dict:
        """Returns the playoff bracket.

        Args:
           year (str): Year playoffs take place (e.g., "2024")

        Returns:
           dict: Playoff bracket data.

        Example:
           API endpoint: https://api-web.nhle.com/v1/playoff-bracket/2024
        """

        return self.client.get(resource=f"playoff-bracket/{year}").json()
