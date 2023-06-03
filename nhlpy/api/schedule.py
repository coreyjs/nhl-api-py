from typing import Optional
from nhlpy.api import BaseNHLAPIClient


class Schedule(BaseNHLAPIClient):
    def get_schedule(self, season: Optional[str] = None) -> dict:
        """
        Returns a list of all games for the current season if no season is supplied.  Otherwise returns the
        schedule for the season defined in the season: param.
        :param season: Season in format of 20202021
        :return:
        """
        query = f"?season={season}" if season else ""
        return self._get(resource=f"schedule{query}").json()
