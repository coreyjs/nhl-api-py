from nhlpy.api import BaseNHLAPIClient


class Teams(BaseNHLAPIClient):
    def all(self) -> dict:
        """
        Returns a list of all teams.
        :return: dict
        """
        return self._get(resource="/teams").json()

    def get_by_id(
        self,
        id: int,
        roster: bool = False,
    ) -> dict:
        """
        Returns a team by id.
        :param id: int, NHL team id
        :param roster: bool, Should include the roster for the team
        :return: dict
        """
        query = ""
        if roster:
            query += "?expand=team.roster"
        return self._get(resource=f"teams/{id}{query}").json()

    def get_team_next_game(self, id: int) -> dict:
        """
        Returns the next game for the team with the id supplied.
        :param id: int, NHL team id
        :return: dict
        """
        return self._get(resource=f"teams/{id}?expand=team.schedule.next").json()

    def get_team_previous_game(self, id: int) -> dict:
        """
        Returns the previous game for the team with the id supplied.
        :param id: int, NHL team id
        :return: dict
        """
        return self._get(resource=f"teams/{id}?expand=team.schedule.previous").json()

    def get_team_with_stats(self, id: int) -> dict:
        """
        Returns the team with stats for the team with the id supplied.
        :param id: int, NHL team id
        :return: dict
        """
        return self._get(resource=f"teams/{id}?expand=team.stats").json()

    def get_team_roster(self, id: int) -> dict:
        """
        Returns the roster for the team with the id supplied.
        :param id: int, NHL team id
        :return: dict
        """
        return self._get(resource=f"teams/{id}/roster").json()

    def get_team_stats(self, id: int) -> dict:
        """
        Returns the stats for the team with the id supplied.
        :param id:
        :return: dict
        """
        return self._get(resource=f"teams/{id}/stats").json()
