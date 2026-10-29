from unittest import mock

import pytest


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


# ========================
# TOP 10 LEADERBOARDS / TEAM COMPARISON
# ========================

EDGE_BASE = "https://api-web.nhle.com/v1/edge/"


@pytest.mark.parametrize(
    "method, kwargs, path",
    [
        ("skater_skating_speed_top_10", {}, "skater-speed-top-10/all/max/now"),
        (
            "skater_skating_speed_top_10",
            {"position_group": "defense", "sort": "over-22", "season": "20242025", "game_type": 3},
            "skater-speed-top-10/defense/over-22/20242025/3",
        ),
        ("skater_shot_speed_top_10", {}, "skater-shot-speed-top-10/all/max/now"),
        (
            "skater_shot_speed_top_10",
            {"position_group": "forwards", "sort": "90-99", "season": "20242025"},
            "skater-shot-speed-top-10/forwards/90-99/20242025/2",
        ),
        ("skater_skating_distance_top_10", {}, "skater-distance-top-10/all/all/total/now"),
        (
            "skater_skating_distance_top_10",
            {"position_group": "defense", "strength": "pk", "sort": "per-60", "season": "20242025"},
            "skater-distance-top-10/defense/pk/per-60/20242025/2",
        ),
        ("skater_zone_time_top_10", {}, "skater-zone-time-top-10/all/all/offensive/now"),
        (
            "skater_zone_time_top_10",
            {"position_group": "forwards", "strength": "es", "sort": "defensive", "season": "20242025"},
            "skater-zone-time-top-10/forwards/es/defensive/20242025/2",
        ),
        ("skater_shot_location_top_10", {}, "skater-shot-location-top-10/all/sog/all/now"),
        (
            "skater_shot_location_top_10",
            {"position_group": "defense", "category": "shooting-pctg", "area": "high", "season": "20242025"},
            "skater-shot-location-top-10/defense/shooting-pctg/high/20242025/2",
        ),
        ("goalie_5v5_top_10", {}, "goalie-5v5-top-10/save-pctg/now"),
        (
            "goalie_5v5_top_10",
            {"sort": "shots-per-60", "season": "20242025", "game_type": 3},
            "goalie-5v5-top-10/shots-per-60/20242025/3",
        ),
        ("goalie_save_percentage_top_10", {}, "goalie-edge-save-pctg-top-10/pctg/now"),
        (
            "goalie_save_percentage_top_10",
            {"sort": "games", "season": "20242025"},
            "goalie-edge-save-pctg-top-10/games/20242025/2",
        ),
        ("goalie_shot_location_top_10", {}, "goalie-shot-location-top-10/save-pctg/all/now"),
        (
            "goalie_shot_location_top_10",
            {"category": "goals-against", "area": "long", "season": "20242025"},
            "goalie-shot-location-top-10/goals-against/long/20242025/2",
        ),
        ("team_comparison", {"team_id": "22"}, "team-comparison/22/now"),
        (
            "team_comparison",
            {"team_id": "22", "season": "20242025", "game_type": 3},
            "team-comparison/22/20242025/3",
        ),
        ("team_skating_speed_top_10", {}, "team-skating-speed-top-10/all/max/now"),
        (
            "team_skating_speed_top_10",
            {"position_group": "forwards", "sort": "18-20", "season": "20242025"},
            "team-skating-speed-top-10/forwards/18-20/20242025/2",
        ),
        ("team_shot_speed_top_10", {}, "team-shot-speed-top-10/all/max/now"),
        (
            "team_shot_speed_top_10",
            {"position_group": "defense", "sort": "over-100", "season": "20242025"},
            "team-shot-speed-top-10/defense/over-100/20242025/2",
        ),
        ("team_skating_distance_top_10", {}, "team-skating-distance-top-10/all/all/total/now"),
        (
            "team_skating_distance_top_10",
            {"position_group": "forwards", "strength": "pp", "sort": "max-game", "season": "20242025"},
            "team-skating-distance-top-10/forwards/pp/max-game/20242025/2",
        ),
        ("team_zone_time_top_10", {}, "team-zone-time-top-10/all/offensive/now"),
        (
            "team_zone_time_top_10",
            {"strength": "pk", "sort": "neutral", "season": "20242025"},
            "team-zone-time-top-10/pk/neutral/20242025/2",
        ),
        ("team_shot_location_top_10", {}, "team-shot-location-top-10/all/sog/all/now"),
        (
            "team_shot_location_top_10",
            {"position_group": "defense", "category": "goals", "area": "mid", "season": "20242025"},
            "team-shot-location-top-10/defense/goals/mid/20242025/2",
        ),
    ],
)
@mock.patch("httpx.Client.get")
def test_edge_top_10_and_team_comparison_urls(mock_get, nhl_client, method, kwargs, path):
    getattr(nhl_client.edge, method)(**kwargs)
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == EDGE_BASE + path


@pytest.mark.parametrize(
    "method, kwargs",
    [
        ("skater_skating_speed_top_10", {"position_group": "goalies"}),
        ("skater_skating_speed_top_10", {"sort": "over-100"}),
        ("skater_shot_speed_top_10", {"sort": "over-22"}),
        ("skater_skating_distance_top_10", {"strength": "5v5"}),
        ("skater_skating_distance_top_10", {"sort": "max"}),
        ("skater_zone_time_top_10", {"sort": "attacking"}),
        ("skater_shot_location_top_10", {"category": "saves"}),
        ("skater_shot_location_top_10", {"area": "slot"}),
        ("goalie_5v5_top_10", {"sort": "pctg"}),
        ("goalie_save_percentage_top_10", {"sort": "save-pctg"}),
        ("goalie_shot_location_top_10", {"category": "sog"}),
        ("goalie_shot_location_top_10", {"area": "highDanger"}),
        ("team_skating_speed_top_10", {"position_group": "F"}),
        ("team_shot_speed_top_10", {"sort": "100"}),
        ("team_skating_distance_top_10", {"strength": "ev"}),
        ("team_zone_time_top_10", {"strength": "all", "sort": "total"}),
        ("team_shot_location_top_10", {"category": "shots"}),
    ],
)
@mock.patch("httpx.Client.get")
def test_edge_top_10_invalid_values_raise_before_request(mock_get, nhl_client, method, kwargs):
    with pytest.raises(ValueError, match="Valid values"):
        getattr(nhl_client.edge, method)(**kwargs)
    mock_get.assert_not_called()
