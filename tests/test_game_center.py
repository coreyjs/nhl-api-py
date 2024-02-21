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
def test_landing_page(h_m, nhl_client):
    nhl_client.game_center.landing(game_id="2020020001")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/gamecenter/2020020001/landing"


@mock.patch("httpx.Client.get")
def test_score_now(h_m, nhl_client):
    nhl_client.game_center.score_now()
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/score/now"
