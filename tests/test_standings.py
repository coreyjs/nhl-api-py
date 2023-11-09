from unittest import mock


@mock.patch("httpx.get")
def test_get_standings(h_m, nhl_client):
    nhl_client.standings.get_standings(season="20222023")
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/standings?season=20222023")


@mock.patch("httpx.get")
def test_get_standings_with_details(h_m, nhl_client):
    nhl_client.standings.get_standings(season="20222023", detailed_record=True)
    h_m.assert_called_once_with(
        url="https://statsapi.web.nhl.com/api/v1/standings?season=20222023&expand=standings.record&"
    )


@mock.patch("httpx.get")
def get_standing_types(h_m, nhl_client):
    nhl_client.standings.get_standing_types()
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/standingsTypes")


@mock.patch("httpx.get")
def test_get_standings_by_type(h_m, nhl_client):
    nhl_client.standings.get_standings_by_standing_type(season="20222023", standing_type="wildCard")
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/standings/wildCard?season=20222023&")


@mock.patch("httpx.get")
def test_get_standings_by_type_with_details(h_m, nhl_client):
    nhl_client.standings.get_standings_by_standing_type(
        season="20222023", standing_type="wildCard", detailed_records=True
    )
    h_m.assert_called_once_with(
        url="https://statsapi.web.nhl.com/api/v1/standings/wildCard?season=20222023&expand=standings.record&"
    )
