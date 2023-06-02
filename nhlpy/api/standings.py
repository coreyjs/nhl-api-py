from nhlpy.api import BaseNHLAPIClient


class Standings(BaseNHLAPIClient):
    def get_standings(self, season: str = None, detailed_record: bool = False) -> dict:
        """
        year: str - Format of 20212022
        detailed_record: bool - Detailed information for each team including
            home and away records, record in shootouts, last ten games, and split
            head-to-head records against divisions and conferences
        """
        modifier = f"season={season}&" if season else ""
        detailed = "expand=standings.record&" if detailed_record else ""
        return self._get(resource=f'standings?{modifier}{detailed}').json()

    def get_standing_types(self) -> dict:
        """
        Returns a list of standing types that can be used in get_standings_by_standing_type()
        :return:
        """
        return self._get(resource='standingsTypes').json()

    def get_standings_by_standing_type(self, standing_type: str) -> dict:
        """

        :param standing_type: string, full list found in get_standing_types() with the following options:
            regularSeason, wildCard,divisionLeaders, wildCardWithLeaders, preseason,
            postseason, byDivision, byConference, byLeague
        :return:
        """
        return self._get(resource=f'standings/{standing_type}').json()
