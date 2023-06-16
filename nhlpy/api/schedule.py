from typing import Optional, List
from nhlpy.api import BaseNHLAPIClient


class Schedule(BaseNHLAPIClient):
    def get_schedule(
        self, season: str, game_type: str = "R", team_ids: Optional[List[int]] = None
    ) -> dict:
        """

        :param season: str - Season in format of 20202021
        :param game_type: str - Game type, R (default) for regular season, P for playoffs, PR for preseason, A for all-star
        :param team_ids: List[int] - List of team ids


            example: c.schedule.get_schedule(season="20222023", team_ids=[7], game_type='PR')

        :return: dict
        """
        q: str = f"?season={season}"
        team_q: str = (
            f"&teamId={','.join(str(t) for t in team_ids)}" if team_ids else ""
        )
        type_q: str = f"&gameType={game_type}"

        return self._get(resource=f"schedule{q}{type_q}{team_q}").json()
