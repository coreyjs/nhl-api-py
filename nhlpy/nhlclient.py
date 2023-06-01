from nhlpy.api import core, teams, standings

class NHLClient:
    def __init__(self) -> None:
        self.core = core.Core()
        self.teams = teams.Teams()
        self.standings = standings.Standings()
