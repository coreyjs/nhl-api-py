from nhlpy.nhl_client import NHLClient
from nhlpy.api import core, teams, standings, schedule, players, games


def test_nhl_client_responds_to_core():
    c = NHLClient()
    assert c.core is not None
    assert isinstance(c.core, core.Core)


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


def test_nhl_client_responds_to_players():
    c = NHLClient()
    assert c.players is not None
    assert isinstance(c.players, players.Players)


def test_nhl_client_responds_to_games():
    c = NHLClient()
    assert c.games is not None
    assert isinstance(c.games, games.Games)
