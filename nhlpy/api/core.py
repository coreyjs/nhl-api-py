from httpx import request

from nhlpy.api import BaseNHLAPIClient


class Core(BaseNHLAPIClient):
    def get_configurations(self) -> dict:
        """
        Returns a list of configuration items that can be used in other endpoints
        :return:
        """
        r: request = self._get(resource="configurations")
        return r.json()

    def get_game_types(self) -> dict:
        """
        Returns a list of game types that can be used in other endpoints
        :return:
        """
        r: request = self._get(resource="gameTypes")
        return r.json()

    def get_standings_types(self) -> dict:
        """

        :return:
        """
        r: request = self._get(resource="standingsTypes")
        return r.json()
