from unittest import mock


@mock.patch("httpx.get")
def test_get_teams(h_m, nhl_client):
    nhl_client.teams.all()
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/teams")


@mock.patch("httpx.get")
def test_get_team(h_m, nhl_client):
    nhl_client.teams.get_by_id(team_id=1)
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/teams/1")


@mock.patch("httpx.get")
def test_get_team_next_game(h_m, nhl_client):
    nhl_client.teams.get_team_next_game(team_id=1)
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/teams/1?expand=team.schedule.next")


@mock.patch("httpx.get")
def test_get_team_previous_game(h_m, nhl_client):
    nhl_client.teams.get_team_previous_game(team_id=1)
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/teams/1?expand=team.schedule.previous")


@mock.patch("httpx.get")
def test_get_team_with_stats(h_m, nhl_client):
    nhl_client.teams.get_team_with_stats(team_id=1)
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/teams/1?expand=team.stats")


@mock.patch("httpx.get")
def test_get_team_roster(h_m, nhl_client):
    nhl_client.teams.get_team_roster(team_id=1)
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/teams/1/roster")


@mock.patch("httpx.get")
def test_get_team_stats(h_m, nhl_client):
    nhl_client.teams.get_team_stats(team_id=1)
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/teams/1/stats")
