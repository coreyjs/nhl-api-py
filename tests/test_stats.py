from unittest import mock


@mock.patch("httpx.Client.get")
def test_stats_season(h_m, nhl_client):
    nhl_client.stats.gametypes_per_season_directory_by_team(team_abbr="BUF")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/club-stats-season/BUF"


@mock.patch("httpx.Client.get")
def test_player_career_stats(h_m, nhl_client):
    nhl_client.stats.player_career_stats(player_id=8481528)
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/player/8481528/landing"


@mock.patch("httpx.Client.get")
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
        "sort": '[{"property": "points", "direction": "DESC"}, {"property": "wins", "direction": "DESC"}, '
        '{"property": "teamId", "direction": "ASC"}]',
        "cayenneExp": "gameTypeId=2 and seasonId<=20232024 and seasonId>=20232024",
    }


@mock.patch("httpx.Client.get")
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


@mock.patch("httpx.Client.get")
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


@mock.patch("httpx.Client.get")
def test_skater_stats_summary(h_m, nhl_client):
    nhl_client.stats.skater_stats_summary(start_season="20232024", end_season="20232024")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/skater/summary"
    assert h_m.call_args[1]["params"] == {
        "isAggregate": False,
        "isGame": False,
        "limit": 25,
        "start": 0,
        "factCayenneExp": "gamesPlayed>=1",
        "sort": '[{"property": "points", "direction": "DESC"}, {"property": '
        '"gamesPlayed", "direction": "ASC"}, {"property": "playerId", '
        '"direction": "ASC"}]',
        "cayenneExp": "gameTypeId=2 and seasonId<=20232024 and seasonId>=20232024",
    }


@mock.patch("httpx.Client.get")
def test_skater_stats_summary_franchise(h_m, nhl_client):
    nhl_client.stats.skater_stats_summary(start_season="20232024", end_season="20232024", franchise_id=19)
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/skater/summary"
    assert h_m.call_args[1]["params"] == {
        "isAggregate": False,
        "isGame": False,
        "limit": 25,
        "start": 0,
        "factCayenneExp": "gamesPlayed>=1",
        "sort": '[{"property": "points", "direction": "DESC"}, {"property": '
        '"gamesPlayed", "direction": "ASC"}, {"property": "playerId", '
        '"direction": "ASC"}]',
        "cayenneExp": "franchiseId=19 and gameTypeId=2 and seasonId<=20232024 and seasonId>=20232024",
    }


@mock.patch("httpx.Client.get")
def test_player_game_log(h_m, nhl_client):
    nhl_client.stats.player_game_log(player_id="8481528", season_id="20232024", game_type=2)
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/player/8481528/game-log/20232024/2"


@mock.patch("httpx.Client.get")
def test_player_game_log_playoffs(h_m, nhl_client):
    nhl_client.stats.player_game_log(player_id="8481528", season_id="20232024", game_type=3)
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/player/8481528/game-log/20232024/3"
