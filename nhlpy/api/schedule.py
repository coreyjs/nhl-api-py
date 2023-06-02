from typing import Optional
from nhlpy.api import BaseNHLAPIClient


class Schedule(BaseNHLAPIClient):
    def get_schedule(self, season: Optional[str] = None) -> dict:
        """

        :param season: Season in format of 20202021
        :return:
        """
        query = f"?season={season}" if season else ""
        return self._get(resource=f'schedule{query}').json()