from unittest import mock


@mock.patch("httpx.get")
def test_get_configuration(h_m, nhl_client):
    nhl_client.core.get_configurations()
    h_m.assert_called_once_with(
        url="https://statsapi.web.nhl.com/api/v1/configurations"
    )


@mock.patch("httpx.get")
def test_get_game_types(h_m, nhl_client):
    nhl_client.core.get_game_types()
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/gameTypes")


@mock.patch("httpx.get")
def test_get_standings_types(h_m, nhl_client):
    nhl_client.core.get_standings_types()
    h_m.assert_called_once_with(
        url="https://statsapi.web.nhl.com/api/v1/standingsTypes"
    )
