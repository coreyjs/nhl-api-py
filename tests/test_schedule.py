from unittest import mock


@mock.patch("httpx.get")
def test_get_schedule(h_m, nhl_client):
    nhl_client.schedule.get_schedule()
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/schedule?")


@mock.patch("httpx.get")
def test_get_schedule_with_season(h_m, nhl_client):
    nhl_client.schedule.get_schedule(season="20222023")
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/schedule?season=20222023")


@mock.patch("httpx.get")
def test_get_schedule_with_season_and_game_type(h_m, nhl_client):
    nhl_client.schedule.get_schedule(season="20222023", game_type="PR")
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/schedule?season=20222023&gameType=PR")


@mock.patch("httpx.get")
def test_get_schedule_with_game_type(h_m, nhl_client):
    nhl_client.schedule.get_schedule(game_type="PR")
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/schedule?gameType=PR")


@mock.patch("httpx.get")
def test_get_schedule_with_date(h_m, nhl_client):
    nhl_client.schedule.get_schedule(date="2022-10-01")
    h_m.assert_called_once_with(url="https://statsapi.web.nhl.com/api/v1/schedule?date=2022-10-01")
