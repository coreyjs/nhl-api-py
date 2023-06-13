from nhlpy.api import core, teams, standings, schedule, players, games, helpers


class NHLClient:
    """
    This is the main class that is used to access the NHL API.

    You can instantiate this class and then access the various endpoints of the API,
    such as:
        client = NHLClient()
        client.teams.all()
    """

    def __init__(self) -> None:
        self.core = core.Core()
        self.teams = teams.Teams()
        self.standings = standings.Standings()
        self.schedule = schedule.Schedule()
        self.players = players.Players()
        self.games = games.Games()
        self.helpers = helpers.Helpers()
