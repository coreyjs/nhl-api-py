from nhlpy.nhl_client import NHLClient
from nhlpy.api import teams, standings, schedule


def test_nhl_client_responds_to_teams():
    c = NHLClient()
    assert c.teams is not None
    assert isinstance(c.teams, teams.Teams)


def test_nhl_client_responds_to_standings():
    c = NHLClient()
    assert c.standings is not None
    assert isinstance(c.standings, standings.Standings)


def test_nhl_client_responds_to_schedule():
    c = NHLClient()
    assert c.schedule is not None
    assert isinstance(c.schedule, schedule.Schedule)
