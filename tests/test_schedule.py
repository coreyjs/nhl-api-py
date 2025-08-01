from unittest import mock

import pytest


@mock.patch("httpx.Client.get")
def test_get_schedule_with_date(h_m, nhl_client):
    nhl_client.schedule.daily_schedule(date="2021-01-01")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/schedule/2021-01-01"


@mock.patch("httpx.Client.get")
def test_get_schedule_with_fixable_date(h_m, nhl_client):
    nhl_client.schedule.daily_schedule("2024-10-9")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/schedule/2024-10-09"


@mock.patch("httpx.Client.get")
def test_get_schedule_will_error_with_bad_date(h_m, nhl_client):
    with pytest.raises(ValueError):
        nhl_client.schedule.daily_schedule("2024-10-09-")


@mock.patch("httpx.Client.get")
def test_get_weekly_schedule_with_date(h_m, nhl_client):
    nhl_client.schedule.weekly_schedule(date="2021-01-01")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/schedule/2021-01-01"


@mock.patch("httpx.Client.get")
def test_get_weekly_schedule_with_no_date(h_m, nhl_client):
    nhl_client.schedule.weekly_schedule()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/schedule/now"


@mock.patch("httpx.Client.get")
def test_get_schedule_by_team_by_month_with_month(h_m, nhl_client):
    nhl_client.schedule.team_monthly_schedule(team_abbr="BUF", month="2023-11")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule/BUF/month/2023-11"


@mock.patch("httpx.Client.get")
def test_get_schedule_by_team_by_month_with_no_month(h_m, nhl_client):
    nhl_client.schedule.team_monthly_schedule(team_abbr="BUF")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule/BUF/month/now"


@mock.patch("httpx.Client.get")
def test_get_schedule_by_team_by_week(h_m, nhl_client):
    nhl_client.schedule.team_weekly_schedule(team_abbr="BUF")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule/BUF/week/now"


@mock.patch("httpx.Client.get")
def test_get_schedule_by_team_by_week_with_date(h_m, nhl_client):
    nhl_client.schedule.team_weekly_schedule(team_abbr="BUF", date="2024-02-10")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule/BUF/week/2024-02-10"


@mock.patch("httpx.Client.get")
def test_get_season_schedule(h_m, nhl_client):
    nhl_client.schedule.team_season_schedule(team_abbr="BUF", season="20202021")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-schedule-season/BUF/20202021"


@mock.patch("httpx.Client.get")
def test_carousel(h_m, nhl_client):
    nhl_client.schedule.playoff_carousel(season="20232024")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/playoff-series/carousel/20232024"


@mock.patch("httpx.Client.get")
def test_schedule(h_m, nhl_client):
    nhl_client.schedule.playoff_series_schedule(season="20232024", series="a")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/schedule/playoff-series/20232024/a"


@mock.patch("httpx.Client.get")
def test_bracket(h_m, nhl_client):
    nhl_client.schedule.playoff_bracket(year="2024")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/playoff-bracket/2024"
