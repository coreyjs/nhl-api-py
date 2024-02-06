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
