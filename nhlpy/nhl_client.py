from nhlpy.api import teams, standings, schedule, game_center
from nhlpy.http_client import HttpClient
from nhlpy.config import ClientConfig


class NHLClient:
    """
    This is the main class that is used to access the NHL API.

    You can instantiate this class and then access the various endpoints of the API,
    such as:
        client = NHLClient()
        client = NHLClient(verbose=True) # for a lil extra logging
    """

    def __init__(self, verbose: bool = False) -> None:
        """
        param: verbose:  If True, will print out the URL of the API call.
        """
        self._config = ClientConfig(verbose=verbose)
        self._http_client = HttpClient(self._config)

        self.teams = teams.Teams(http_client=self._http_client)
        self.standings = standings.Standings(http_client=self._http_client)
        self.schedule = schedule.Schedule(http_client=self._http_client)
        self.game_center = game_center.GameCenter(http_client=self._http_client)
