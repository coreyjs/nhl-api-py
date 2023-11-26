from unittest import mock


@mock.patch("httpx.get")
def test_stats_summary(h_m, nhl_client):
    nhl_client.teams.team_stats_summary()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/team/summary"


@mock.patch("httpx.get")
def test_roster(h_m, nhl_client):
    nhl_client.teams.roster(team_abbr="BUF", season="20202021")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/roster/BUF/20202021"


def test_teams_info(nhl_client):
    teams = nhl_client.teams.teams_info()
    assert len(teams) == 32
