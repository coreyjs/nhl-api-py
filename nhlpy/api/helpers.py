from typing import List

from nhlpy.http_client import HttpClient


class Helpers:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def get_gameids_by_season(self, season: str, game_types: List[int] = None) -> List[str]:
        """Gets all game IDs for a specified season.

        Args:
           season (str): Season to retrieve game IDs for in YYYYYYYY format (e.g., 20232024).
           game_types (List[int]): List of game types to include. Valid types:
               1: Preseason
               2: Regular season
               3: Playoffs

        Returns:
           List of game IDs for the specified season and game types.
        """
        from nhlpy.api.teams import Teams
        from nhlpy.api.schedule import Schedule

        teams = Teams(self.client).teams_info()

        gameids = []
        schedule_api = Schedule(self.client)
        for team in teams:
            team_abbr = team.get("abbr", "")
            if not team_abbr:
                continue

            schedule = schedule_api.get_season_schedule(team_abbr, season)
            games = schedule.get("games", [])

            for game in games:
                game_type = game.get("gameType")
                game_id = game.get("id")

                if game_id and (not game_types or game_type in game_types):
                    gameids.append(game_id)

        return gameids
