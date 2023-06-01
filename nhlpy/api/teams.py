from nhlpy.api import BaseNHLAPIClient


class Teams(BaseNHLAPIClient):
    def all(self) -> dict:
        """Returns a list of all NHL teams."""
        return self._get(resource='/teams').json()

    def get_by_id(
            self,
            id: int,
            roster: bool = False,
    ) -> dict:
        query = ""
        if roster:
            query += "?expand=team.roster"
        return self._get(resource=f'teams/{id}{query}').json()

    def get_team_next_game(self, id: int) -> dict:
        return self._get(resource=f"teams/{id}?expand=team.schedule.next").json()

    def get_team_previous_game(self, id: int) -> dict:
        return self._get(resource=f"teams/{id}?expand=team.schedule.previous").json()

    def get_team_stats(self, id: int) -> dict:
        return self._get(resource=f"teams/{id}?expand=team.stats").json()