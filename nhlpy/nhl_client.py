from nhlpy.api import core, teams, standings, schedule, players


class NHLClient:
    """
    This is the main class that is used to access the NHL API.
    """

    def __init__(self) -> None:
        self.core = core.Core()
        self.teams = teams.Teams()
        self.standings = standings.Standings()
        self.schedule = schedule.Schedule()
        self.players = players.Players()
