from nhlpy.api import teams, standings, schedule, game_center


class NHLClient:
    """
    This is the main class that is used to access the NHL API.

    You can instantiate this class and then access the various endpoints of the API,
    such as:
        client = NHLClient()
    """

    def __init__(self) -> None:
        self.teams = teams.Teams()
        self.standings = standings.Standings()
        self.schedule = schedule.Schedule()
        self.game_center = game_center.GameCenter()
        # self.helpers = helpers.Helpers()
