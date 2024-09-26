from unittest import mock


@mock.patch("httpx.Client.get")
def test_roster(h_m, nhl_client):
    nhl_client.teams.roster(team_abbr="BUF", season="20202021")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/roster/BUF/20202021"
