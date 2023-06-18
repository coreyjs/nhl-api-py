from nhlpy.api import BaseNHLAPIClient


class Standings(BaseNHLAPIClient):
    def get_standing_types(self) -> dict:
        """
        Returns a list of standing types that can be used in get_standings_by_standing_type()
        :return: dict of standing types
        """
        return self._get(resource="standingsTypes").json()

    def get_standings(self, season: str, detailed_record: bool = False) -> dict:
        """
        Gets the standings for the season supplied via season: param.
        :param season:
        :param detailed_record: Detailed information for each team including
            home and away records, record in shootouts, last ten games, and split
            head-to-head records against divisions and conferences.
        :return: dict
        """
        modifier: str = f"season={season}"
        detailed: str = "&expand=standings.record&" if detailed_record else ""

        response: dict = self._get(resource=f"standings?{modifier}{detailed}").json()
        return response["records"]

    def get_standings_by_standing_type(
        self, season: str, standing_type: str, detailed_records: bool = False
    ) -> dict:
        """

        :param detailed_records:  bool, indicates whether or not to return detailed records for each team
        :param season: str, Season in the format of 20202021
        :param standing_type: str, full list found in get_standing_types() with the following options:
            regularSeason, wildCard,divisionLeaders, wildCardWithLeaders, preseason,
            postseason, byDivision, byConference, byLeague
        :return: dict
        """
        query: str = f"season={season}&"
        detailed: str = "expand=standings.record&" if detailed_records else ""
        response: dict = self._get(
            resource=f"standings/{standing_type}?{query}{detailed}"
        ).json()
        return response["records"]
