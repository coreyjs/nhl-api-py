from unittest import mock


@mock.patch("httpx.get")
def test_stats_season(h_m, nhl_client):
    nhl_client.stats.club_stats_season(team_abbr="BUF")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-stats-season/BUF"


@mock.patch("httpx.get")
def test_player_career_stats(h_m, nhl_client):
    nhl_client.stats.player_career_stats(player_id=8481528)
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/player/8481528/landing"


@mock.patch("httpx.get")
def test_team_summary_single_year(h_m, nhl_client):
    nhl_client.stats.team_summary(start_season="20232024", end_season="20232024")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/team/summary"
    assert h_m.call_args[1]["params"] == {
        "isAggregate": False,
        "isGame": False,
        "limit": 50,
        "start": 0,
        "factCayenneExp": "gamesPlayed>1",
        "sort": "%5B%7B%22property%22%3A%20%22points%22%2C%20%22direction%22%3A%20%22DESC%22%7D%2C%20%7B%22property%22"
        "%3A%20%22wins%22%2C%20%22direction%22%3A%20%22DESC%22%7D%2C%20%7B%22property%22%3A%20%22teamId%22%2C%"
        "20%22direction%22%3A%20%22ASC%22%7D%5D",
        "cayenneExp": "gameTypeId=2 and seasonId<=20232024 and seasonId>=20232024",
    }


@mock.patch("httpx.get")
def team_test_summary_year_range(h_m, nhl_client):
    nhl_client.stats.team_summary(start_season="20202021", end_season="20232024")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/team/summary"
    assert h_m.call_args[1]["params"] == {
        "isAggregate": False,
        "isGame": False,
        "limit": 50,
        "start": 0,
        "factCayenneExp": "gamesPlayed>1",
        "sort": "%5B%7B%22property%22%3A%20%22points%22%2C%20%22direction%22%3A%20%22DESC%22%7D%2C%20%7B%22"
        "property%22%3A%20%22wins%22%2C%20%22direction%22%3A%20%22DESC%22%7D%2C%20%7B%22property%22"
        "%3A%20%22teamId%22%2C%20%22direction%22%3A%20%22ASC%22%7D%5D",
        "cayenneExp": "gameTypeId=2 and seasonId<=20232024 and seasonId>=20202021",
    }


@mock.patch("httpx.get")
def team_test_summary_year_range_playoffs(h_m, nhl_client):
    nhl_client.stats.team_summary(start_season="20182019", end_season="20222023", game_type_id=3)
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/team/summary"
    assert h_m.call_args[1]["params"] == {
        "isAggregate": False,
        "isGame": False,
        "limit": 50,
        "start": 0,
        "factCayenneExp": "gamesPlayed>1",
        "sort": "%5B%7B%22property%22%3A%20%22points%22%2C%20%22direction%22%3A%20%22DESC%22%7D%2C%20%7"
        "B%22property%22%3A%20%22wins%22%2C%20%22direction%22%3A%20%22DESC%22%7D%2C%20%7B%22pro"
        "perty%22%3A%20%22teamId%22%2C%20%22direction%22%3A%20%22ASC%22%7D%5D",
        "cayenneExp": "gameTypeId=3 and seasonId<=20222023 and seasonId>=20182019",
    }
