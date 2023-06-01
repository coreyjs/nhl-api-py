from httpx import request

from nhlpy.api import BaseNHLAPIClient


class Core(BaseNHLAPIClient):
    def get_configurations(self) -> dict:
        r: request = self._get(resource='configurations')
        return r.json()
    
    def get_game_types(self) -> dict:
        r: request = self._get(resource='gameTypes')
        return r.json()
    
    def get_standings_types(self) -> dict:
        r: request = self._get(resource='standingsTypes')
        return r.json()
