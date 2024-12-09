from typing import List

from nhlpy.http_client import HttpClient


class Helpers:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def get_gameids_by_season(self, season: str, game_types: List[int] = None) -> List[str]:
        """
        Get all gameids for a given season.
        :param season: The season you want the gameids for.  Format is YYYYYYYY.  20202021, 200232024, etc
        :param game_types: List of game types you want to include.  2 is regular season, 3 is playoffs, 1 is preseason
        """
        from nhlpy.api.teams import Teams
        from nhlpy.api.schedule import Schedule

        teams = Teams(self.client).teams_info()

        gameids = []
        schedule_api = Schedule(self.client)
        for team in teams:
            schedule = schedule_api.get_season_schedule(team["abbr"], season)
            for game in schedule["games"]:
                if not game_types or game["gameType"] in game_types:
                    gameids.append(game["id"])

        return gameids
