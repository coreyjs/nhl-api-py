from unittest import mock


@mock.patch("httpx.Client.get")
def test_skater_detail_now(mock_get, nhl_client):
    nhl_client.edge.skater_detail(player_id=8478402)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-detail/8478402/now"


@mock.patch("httpx.Client.get")
def test_skater_detail_with_season_and_game_type(mock_get, nhl_client):
    nhl_client.edge.skater_detail(player_id=8478402, season=20242025, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-detail/8478402/20242025/2"


@mock.patch("httpx.Client.get")
def test_skater_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.skater_detail(player_id=8478402, season=20232024, game_type=3)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-detail/8478402/20232024/3"


@mock.patch("httpx.Client.get")
def test_goalie_detail_now(mock_get, nhl_client):
    nhl_client.edge.goalie_detail(player_id=8476945)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-detail/8476945/now"


@mock.patch("httpx.Client.get")
def test_goalie_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.goalie_detail(player_id=8476945, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-detail/8476945/20232024/2"


@mock.patch("httpx.Client.get")
def test_skater_shot_speed_detail_now(mock_get, nhl_client):
    nhl_client.edge.skater_shot_speed_detail(player_id=1)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-shot-speed-detail/1/now"


@mock.patch("httpx.Client.get")
def test_skater_shot_speed_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.skater_shot_speed_detail(player_id=1, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-shot-speed-detail/1/20232024/2"


@mock.patch("httpx.Client.get")
def test_skater_skating_speed_detail_now(mock_get, nhl_client):
    nhl_client.edge.skater_skating_speed_detail(player_id=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-skating-speed-detail/2/now"


@mock.patch("httpx.Client.get")
def test_skater_skating_speed_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.skater_skating_speed_detail(player_id=2, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-skating-speed-detail/2/20232024/2"


@mock.patch("httpx.Client.get")
def test_skater_shot_location_detail_now(mock_get, nhl_client):
    nhl_client.edge.skater_shot_location_detail(player_id=3)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-shot-location-detail/3/now"


@mock.patch("httpx.Client.get")
def test_skater_shot_location_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.skater_shot_location_detail(player_id=3, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-shot-location-detail/3/20232024/2"


@mock.patch("httpx.Client.get")
def test_skater_skating_distance_detail_now(mock_get, nhl_client):
    nhl_client.edge.skater_skating_distance_detail(player_id=4)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-skating-distance-detail/4/now"


@mock.patch("httpx.Client.get")
def test_skater_skating_distance_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.skater_skating_distance_detail(player_id=4, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-skating-distance-detail/4/20232024/2"


@mock.patch("httpx.Client.get")
def test_skater_comparison_now(mock_get, nhl_client):
    nhl_client.edge.skater_comparison(player_id=5)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-comparison/5/now"


@mock.patch("httpx.Client.get")
def test_skater_comparison_with_season(mock_get, nhl_client):
    nhl_client.edge.skater_comparison(player_id=5, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-comparison/5/20232024/2"


@mock.patch("httpx.Client.get")
def test_skater_zone_time_now(mock_get, nhl_client):
    nhl_client.edge.skater_zone_time(player_id=6)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-zone-time/6/now"


@mock.patch("httpx.Client.get")
def test_skater_zone_time_with_season(mock_get, nhl_client):
    nhl_client.edge.skater_zone_time(player_id=6, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-zone-time/6/20232024/2"


@mock.patch("httpx.Client.get")
def test_skater_landing_now(mock_get, nhl_client):
    nhl_client.edge.skater_landing()
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-landing/now"


@mock.patch("httpx.Client.get")
def test_skater_landing_with_season(mock_get, nhl_client):
    nhl_client.edge.skater_landing(season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/skater-landing/20232024/2"


@mock.patch("httpx.Client.get")
def test_cat_skater_detail_now(mock_get, nhl_client):
    nhl_client.edge.cat_skater_detail(player_id=7)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/cat/edge/skater-detail/7/now"


@mock.patch("httpx.Client.get")
def test_cat_skater_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.cat_skater_detail(player_id=7, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/cat/edge/skater-detail/7/20232024/2"


@mock.patch("httpx.Client.get")
def test_goalie_shot_location_detail_now(mock_get, nhl_client):
    nhl_client.edge.goalie_shot_location_detail(player_id=8)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-shot-location-detail/8/now"


@mock.patch("httpx.Client.get")
def test_goalie_shot_location_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.goalie_shot_location_detail(player_id=8, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-shot-location-detail/8/20232024/2"


@mock.patch("httpx.Client.get")
def test_goalie_5v5_detail_now(mock_get, nhl_client):
    nhl_client.edge.goalie_5v5_detail(player_id=9)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-5v5-detail/9/now"


@mock.patch("httpx.Client.get")
def test_goalie_5v5_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.goalie_5v5_detail(player_id=9, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-5v5-detail/9/20232024/2"


@mock.patch("httpx.Client.get")
def test_goalie_comparison_now(mock_get, nhl_client):
    nhl_client.edge.goalie_comparison(player_id=10)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-comparison/10/now"


@mock.patch("httpx.Client.get")
def test_goalie_comparison_with_season(mock_get, nhl_client):
    nhl_client.edge.goalie_comparison(player_id=10, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-comparison/10/20232024/2"


@mock.patch("httpx.Client.get")
def test_goalie_save_percentage_detail_now(mock_get, nhl_client):
    nhl_client.edge.goalie_save_percentage_detail(player_id=11)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-save-percentage-detail/11/now"


@mock.patch("httpx.Client.get")
def test_goalie_save_percentage_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.goalie_save_percentage_detail(player_id=11, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-save-percentage-detail/11/20232024/2"


@mock.patch("httpx.Client.get")
def test_goalie_landing_now(mock_get, nhl_client):
    nhl_client.edge.goalie_landing()
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-landing/now"


@mock.patch("httpx.Client.get")
def test_goalie_landing_with_season(mock_get, nhl_client):
    nhl_client.edge.goalie_landing(season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/goalie-landing/20232024/2"


@mock.patch("httpx.Client.get")
def test_cat_goalie_detail_now(mock_get, nhl_client):
    nhl_client.edge.cat_goalie_detail(player_id=12)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/cat/edge/goalie-detail/12/now"


@mock.patch("httpx.Client.get")
def test_cat_goalie_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.cat_goalie_detail(player_id=12, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/cat/edge/goalie-detail/12/20232024/2"


@mock.patch("httpx.Client.get")
def test_team_detail_now(mock_get, nhl_client):
    nhl_client.edge.team_detail(team_id=13)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-detail/13/now"


@mock.patch("httpx.Client.get")
def test_team_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.team_detail(team_id=13, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-detail/13/20232024/2"


@mock.patch("httpx.Client.get")
def test_team_skating_distance_detail_now(mock_get, nhl_client):
    nhl_client.edge.team_skating_distance_detail(team_id=14)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-skating-distance-detail/14/now"


@mock.patch("httpx.Client.get")
def test_team_skating_distance_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.team_skating_distance_detail(team_id=14, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-skating-distance-detail/14/20232024/2"


@mock.patch("httpx.Client.get")
def test_team_zone_time_details_now(mock_get, nhl_client):
    nhl_client.edge.team_zone_time_details(team_id=15)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-zone-time-details/15/now"


@mock.patch("httpx.Client.get")
def test_team_zone_time_details_with_season(mock_get, nhl_client):
    nhl_client.edge.team_zone_time_details(team_id=15, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-zone-time-details/15/20232024/2"


@mock.patch("httpx.Client.get")
def test_team_shot_location_detail_now(mock_get, nhl_client):
    nhl_client.edge.team_shot_location_detail(team_id=16)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-shot-location-detail/16/now"


@mock.patch("httpx.Client.get")
def test_team_shot_location_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.team_shot_location_detail(team_id=16, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-shot-location-detail/16/20232024/2"


@mock.patch("httpx.Client.get")
def test_team_landing_now(mock_get, nhl_client):
    nhl_client.edge.team_landing()
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-landing/now"


@mock.patch("httpx.Client.get")
def test_team_landing_with_season(mock_get, nhl_client):
    nhl_client.edge.team_landing(season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-landing/20232024/2"


@mock.patch("httpx.Client.get")
def test_team_shot_speed_detail_now(mock_get, nhl_client):
    nhl_client.edge.team_shot_speed_detail(team_id=17)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-shot-speed-detail/17/now"


@mock.patch("httpx.Client.get")
def test_team_shot_speed_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.team_shot_speed_detail(team_id=17, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-shot-speed-detail/17/20232024/2"


@mock.patch("httpx.Client.get")
def test_team_skating_speed_detail_now(mock_get, nhl_client):
    nhl_client.edge.team_skating_speed_detail(team_id=18)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-skating-speed-detail/18/now"


@mock.patch("httpx.Client.get")
def test_team_skating_speed_detail_with_season(mock_get, nhl_client):
    nhl_client.edge.team_skating_speed_detail(team_id=18, season=20232024, game_type=2)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/edge/team-skating-speed-detail/18/20232024/2"
