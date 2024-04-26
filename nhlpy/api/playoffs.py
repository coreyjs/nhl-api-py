from nhlpy.http_client import HttpClient


class Playoffs:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def carousel(self, season: str) -> dict:
        """
        Get the list of all series games up to the current round.

        :param season: the current season ex. "20232024"

        example:
                https://api-web.nhle.com/v1/playoff-series/carousel/20232024/

        :return: dict
        """
        return self.client.get(resource=f"playoff-series/carousel/{season}").json()

    def schedule(self, season: str, series: str) -> dict:
        """
        Returns the schedule for a specified series.

        :param season: the season you wish to see the schedule of
        :param series: the series (a-h) for Round 1

        example:
                https://api-web.nhle.com/v1/schedule/playoff-series/20232024/a/

        :return: dict
        """

        return self.client.get(resource=f"schedule/playoff-series/{season}/{series}").json()

    def bracket(self, year: str) -> dict:
        """
        Returns the playoff bracket

        :param year: the year the playoffs are taking place ex. "2024"

        example:
                https://api-web.nhle.com/v1/playoff-bracket/2024

        :return: dict
        """

        return self.client.get(resource=f"playoff-bracket/{year}").json()
