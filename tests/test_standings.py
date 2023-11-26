from unittest import mock


@mock.patch("httpx.get")
def test_get_standings(h_m, nhl_client):
    nhl_client.standings.get_standings()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/standings/now"


@mock.patch("httpx.get")
def test_get_standings_with_cache_load(h_m, nhl_client):
    nhl_client.standings.get_standings(season="20202021", cache=True)
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/standings/2021-05-19"
