from unittest import mock


@mock.patch("httpx.Client.get")
def test_boxscore(h_m, nhl_client):
    nhl_client.game_center.boxscore(game_id="2020020001")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/gamecenter/2020020001/boxscore"


@mock.patch("httpx.Client.get")
def test_play_by_play(h_m, nhl_client):
    nhl_client.game_center.play_by_play(game_id="2020020001")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/gamecenter/2020020001/play-by-play"


@mock.patch("httpx.Client.get")
def test_match_up(h_m, nhl_client):
    nhl_client.game_center.match_up(game_id="2020020001")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/gamecenter/2020020001/landing"


@mock.patch("httpx.Client.get")
def test_daily_scores_now(h_m, nhl_client):
    nhl_client.game_center.daily_scores()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/score/now"


@mock.patch("httpx.Client.get")
def test_daily_scores_with_date(h_m, nhl_client):
    nhl_client.game_center.daily_scores(date="2023-10-15")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/score/2023-10-15"


@mock.patch("httpx.Client.get")
def test_shift_chart_data_default_excludes(h_m, nhl_client):
    nhl_client.game_center.shift_chart_data(game_id="2020020001")
    h_m.assert_called_once()
    assert (
        h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId=2020020001 and "
        "((duration != '00:00' and typeCode = 517) or typeCode != 517 )&exclude=eventDetails"
    )


@mock.patch("httpx.Client.get")
def test_shift_chart_data_custom_excludes(h_m, nhl_client):
    nhl_client.game_center.shift_chart_data(game_id="2020020001", excludes=["eventDetails", "playerStats"])
    h_m.assert_called_once()
    assert (
        h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId=2020020001 and "
        "((duration != '00:00' and typeCode = 517) or typeCode != 517 )&exclude=eventDetails,playerStats"
    )


@mock.patch("httpx.Client.get")
def test_shift_chart_data_empty_excludes(h_m, nhl_client):
    nhl_client.game_center.shift_chart_data(game_id="2020020001", excludes=[])
    h_m.assert_called_once()
    assert (
        h_m.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId=2020020001 and "
        "((duration != '00:00' and typeCode = 517) or typeCode != 517 )&exclude="
    )


@mock.patch("httpx.Client.get")
def test_season_series_matchup(h_m, nhl_client):
    nhl_client.game_center.season_series_matchup(game_id="2020020001")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/gamecenter/2020020001/right-rail"


@mock.patch("httpx.Client.get")
def test_game_story(h_m, nhl_client):
    nhl_client.game_center.game_story(game_id="2020020001")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/wsc/game-story/2020020001"
