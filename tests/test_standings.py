from unittest import mock


@mock.patch("httpx.Client.get")
def test_get_standings(h_m, nhl_client):
    nhl_client.standings.league_standings()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/standings/now"


@mock.patch("httpx.Client.get")
def test_get_standings_manifest(h_m, nhl_client):
    nhl_client.standings.season_standing_manifest()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/standings-season"
