from nhlpy.api import teams, standings, schedule, game_center, stats, misc, helpers, players
from nhlpy.http_client import HttpClient
from nhlpy.config import ClientConfig


class NHLClient:
    """
    This is the main class that is used to access the NHL API.

    You can instantiate this class and then access the various endpoints of the API,
    such as:
        client = NHLClient()
        client = NHLClient(debug=True) # for a lil extra logging
    """

    def __init__(
        self, debug: bool = False, timeout: int = 10, ssl_verify: bool = True, follow_redirects: bool = True
    ) -> None:
        """
        :param follow_redirects: bool.  Some of these endpoints use redirects (ew).  This is the case when using
        endpoints that use "/now" in them, which will redirect to todays data.
        :param debug: bool, Defaults to False.  Set to True for extra logging.
        :param timeout: int, Defaults to 10 seconds.
        :param ssl_verify: bool, Defaults to True.  Set to false if you want to ignore SSL verification.
        """
        # This config type setup isnt doing what I thought it would.  This will be reworked later on.
        self._config = ClientConfig(
            debug=debug, timeout=timeout, ssl_verify=ssl_verify, follow_redirects=follow_redirects
        )
        self._http_client = HttpClient(self._config)

        self.teams = teams.Teams(http_client=self._http_client)
        self.standings = standings.Standings(http_client=self._http_client)
        self.schedule = schedule.Schedule(http_client=self._http_client)
        self.game_center = game_center.GameCenter(http_client=self._http_client)
        self.stats = stats.Stats(http_client=self._http_client)
        self.misc = misc.Misc(http_client=self._http_client)
        self.helpers = helpers.Helpers(http_client=self._http_client)
        self.players = players.Players(http_client=self._http_client)
