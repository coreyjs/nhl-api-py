from unittest import mock


@mock.patch("httpx.get")
def test_get_schedule_with_date(h_m, nhl_client):
    nhl_client.schedule.get_schedule(date="2021-01-01")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/schedule/2021-01-01"


@mock.patch("httpx.get")
def test_get_schedule_with_no_date(h_m, nhl_client):
    nhl_client.schedule.get_schedule()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/schedule/now"


@mock.patch("httpx.get")
def test_get_schedule_by_team_by_month_with_month(h_m, nhl_client):
    nhl_client.schedule.get_schedule_by_team_by_month(team_abbr="BUF", month="2023-11")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule/BUF/month/2023-11"


@mock.patch("httpx.get")
def test_get_schedule_by_team_by_month_with_no_month(h_m, nhl_client):
    nhl_client.schedule.get_schedule_by_team_by_month(team_abbr="BUF")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule/BUF/month/now"


@mock.patch("httpx.get")
def test_get_schedule_by_team_by_week(h_m, nhl_client):
    nhl_client.schedule.get_schedule_by_team_by_week(team_abbr="BUF")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule/BUF/week/now"


@mock.patch("httpx.get")
def test_get_schedule_by_team_by_week_with_date(h_m, nhl_client):
    nhl_client.schedule.get_schedule_by_team_by_week(team_abbr="BUF", date="2024-02-10")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule/BUF/week/2024-02-10"


@mock.patch("httpx.get")
def test_get_season_schedule(h_m, nhl_client):
    nhl_client.schedule.get_season_schedule(team_abbr="BUF", season="20202021")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule-season/BUF/20202021"
