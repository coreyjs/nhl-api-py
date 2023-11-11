from unittest import mock


@mock.patch("httpx.get")
def test_stats_summary(h_m, nhl_client):
    nhl_client.teams.team_stats_summary()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/team/summary"
