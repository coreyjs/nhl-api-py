from unittest import mock


@mock.patch("httpx.Client.get")
def test_carousel(h_m, nhl_client):
    nhl_client.playoffs.carousel(season="20232024")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/playoff-series/carousel/20232024"


@mock.patch("httpx.Client.get")
def test_schedule(h_m, nhl_client):
    nhl_client.playoffs.schedule(season="20232024", series="a")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/schedule/playoff-series/20232024/a"


@mock.patch("httpx.Client.get")
def test_bracket(h_m, nhl_client):
    nhl_client.playoffs.bracket(year="2024")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/playoff-bracket/2024"
