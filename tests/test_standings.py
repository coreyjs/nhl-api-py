from unittest import mock


@mock.patch("httpx.get")
def test_get_standings(h_m, nhl_client):
    nhl_client.standings.get_standings()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/standings/now"
