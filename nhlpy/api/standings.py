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
        return self._get(resource='standingsTypes').json()
