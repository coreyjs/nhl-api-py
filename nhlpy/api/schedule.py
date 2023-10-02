from typing import Optional, List
from nhlpy.api import BaseNHLAPIClient


class Schedule(BaseNHLAPIClient):
    def get_schedule(
        self, season: Optional[str] = None, game_type: str = None, team_ids: Optional[List[int]] = None
    ) -> dict:
        """

        :param season: str - Season in format of 20202021
        :param game_type: str - Game type, R (default) for regular season, P for playoffs,
        PR for preseason, A for all-star.  This can also be a comma separated list of game types such as "R,P,PR".
        :param team_ids: List[int] - List of team ids


            example:
            c.schedule.get_schedule(season="20222023", team_ids=[7], game_type='PR')
            c.schedule.get_schedule()

        :return: dict
        """
        query_p = []

        if season:
            query_p.append(f"season={season}")

        if team_ids:
            query_p.append(f"teamId={','.join(str(t) for t in team_ids)}")

        if game_type:
            query_p.append(f"gameType={game_type}")

        return self._get(resource=f"schedule?{ '&'.join(query_p) }").json()
