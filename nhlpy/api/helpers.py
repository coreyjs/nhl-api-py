from typing import List

from nhlpy.http_client import HttpClient


class Helpers:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def get_gameids_by_season(self, season: str) -> List[str]:
        """
        Get all gameids for a given season.
        :param season: The season you want the gameids for.  Format is YYYYYYYY.  20202021, 200232024, etc
        """
        from nhlpy.api.teams import Teams
        from nhlpy.api.schedule import Schedule

        teams = Teams(self.client).teams_info()

        gameids = []
        for team in teams:
            schedule = Schedule(self.client).get_season_schedule(team["abbr"], season)
            gameids.extend([game["id"] for game in schedule["games"]])

        return gameids
