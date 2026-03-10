# Tests for nhlpy/api/helpers.py
#
# Unlike other test modules that mock at the HTTP transport layer (httpx.Client.get),
# these tests mock at the API class level because Helpers orchestrates multiple API
# modules and HTTP-level mocking would be impractically complex.

from unittest import mock

import pytest

from nhlpy.api.helpers import Helpers


@pytest.fixture
def mock_teams_data():
    return [
        {"abbr": "TOR", "franchise_id": 5},
        {"abbr": "MTL", "franchise_id": 1},
    ]


@pytest.fixture
def mock_schedule_data():
    """Schedule data keyed by team abbreviation. Game 2024020001 appears in both teams."""
    return {
        "TOR": {
            "games": [
                {"id": 2024010001, "gameType": 1},
                {"id": 2024020001, "gameType": 2},
                {"id": 2024030001, "gameType": 3},
            ]
        },
        "MTL": {
            "games": [
                {"id": 2024020001, "gameType": 2},
                {"id": 2024020002, "gameType": 2},
            ]
        },
    }


@pytest.fixture
def mock_roster_data():
    return {
        "TOR": {
            "forwards": [
                {
                    "id": 1,
                    "firstName": {"default": "Auston"},
                    "lastName": {"default": "Matthews"},
                }
            ],
            "defensemen": [],
            "goalies": [],
        },
        "MTL": {
            "forwards": [],
            "defensemen": [
                {
                    "id": 2,
                    "firstName": {"default": "Mike"},
                    "lastName": {"default": "Matheson"},
                }
            ],
            "goalies": [],
        },
    }


# -- game_ids_by_season tests --


@mock.patch("nhlpy.api.helpers.time")
@mock.patch("nhlpy.api.schedule.Schedule")
@mock.patch("nhlpy.api.teams.Teams")
def test_game_ids_by_season(MockTeams, MockSchedule, mock_time, nhl_client, mock_teams_data, mock_schedule_data):
    MockTeams.return_value.teams.return_value = mock_teams_data
    MockSchedule.return_value.team_season_schedule.side_effect = lambda abbr, season: mock_schedule_data[abbr]

    result = nhl_client.helpers.game_ids_by_season("20242025", api_sleep_rate=0.1)

    assert result == [2024010001, 2024020001, 2024030001, 2024020001, 2024020002]
    mock_time.sleep.assert_called_with(0.1)
    assert mock_time.sleep.call_count == 2


@mock.patch("nhlpy.api.helpers.time")
@mock.patch("nhlpy.api.schedule.Schedule")
@mock.patch("nhlpy.api.teams.Teams")
def test_game_ids_by_season_with_game_types_filter(
    MockTeams, MockSchedule, mock_time, nhl_client, mock_teams_data, mock_schedule_data
):
    MockTeams.return_value.teams.return_value = mock_teams_data
    MockSchedule.return_value.team_season_schedule.side_effect = lambda abbr, season: mock_schedule_data[abbr]

    result = nhl_client.helpers.game_ids_by_season("20242025", game_types=[2])

    assert result == [2024020001, 2024020001, 2024020002]


@mock.patch("nhlpy.api.helpers.time")
@mock.patch("nhlpy.api.schedule.Schedule")
@mock.patch("nhlpy.api.teams.Teams")
def test_game_ids_by_season_skips_empty_abbr(MockTeams, MockSchedule, mock_time, nhl_client):
    MockTeams.return_value.teams.return_value = [
        {"abbr": "TOR", "franchise_id": 5},
        {"abbr": "", "franchise_id": 99},
    ]
    MockSchedule.return_value.team_season_schedule.return_value = {"games": [{"id": 2024020001, "gameType": 2}]}

    result = nhl_client.helpers.game_ids_by_season("20242025")

    assert result == [2024020001]
    MockSchedule.return_value.team_season_schedule.assert_called_once_with("TOR", "20242025")


@mock.patch("nhlpy.api.helpers.time")
@mock.patch("nhlpy.api.schedule.Schedule")
@mock.patch("nhlpy.api.teams.Teams")
def test_game_ids_by_season_empty_teams(MockTeams, MockSchedule, mock_time, nhl_client):
    MockTeams.return_value.teams.return_value = []

    result = nhl_client.helpers.game_ids_by_season("20242025")

    assert result == []
    MockSchedule.return_value.team_season_schedule.assert_not_called()


# -- all_players tests --


@mock.patch("nhlpy.api.helpers.time")
@mock.patch("nhlpy.api.teams.Teams")
def test_all_players(MockTeams, mock_time, nhl_client, mock_teams_data, mock_roster_data):
    teams_instance = MockTeams.return_value
    teams_instance.teams.return_value = mock_teams_data
    teams_instance.team_roster.side_effect = lambda team_abbr, season: mock_roster_data[team_abbr]

    result = nhl_client.helpers.all_players("20242025")

    assert len(result) == 2

    assert result[0]["id"] == 1
    assert result[0]["firstName"] == "Auston"
    assert result[0]["lastName"] == "Matthews"
    assert result[0]["team"] == "TOR"

    assert result[1]["id"] == 2
    assert result[1]["firstName"] == "Mike"
    assert result[1]["lastName"] == "Matheson"
    assert result[1]["team"] == "MTL"


# -- all_players_summary_statistics tests --


@mock.patch("nhlpy.api.helpers.time")
@mock.patch("nhlpy.api.helpers.Stats")
@mock.patch("nhlpy.api.helpers.Teams")
@mock.patch.object(Helpers, "all_players")
def test_all_players_summary_statistics(mock_all_players, MockTeams, MockStats, mock_time, nhl_client, mock_teams_data):
    mock_all_players.return_value = [
        {"id": 1, "firstName": "Auston", "lastName": "Matthews", "team": "TOR", "position": "C"},
        {"id": 2, "firstName": "Mike", "lastName": "Matheson", "team": "MTL", "position": "D"},
    ]
    MockTeams.return_value.teams.return_value = mock_teams_data

    def stats_side_effect(report_type, query_context, aggregate):
        return {
            "data": [
                {"playerId": 1, "goals": 50, "position": "F"},
                {"playerId": 999, "goals": 10},
            ]
        }

    MockStats.return_value.skater_stats_with_query_context.side_effect = stats_side_effect

    result = nhl_client.helpers.all_players_summary_statistics("20242025")

    # Find entries by playerId
    matched = [e for e in result if e.get("playerId") == 1]
    assert len(matched) >= 1
    entry = matched[0]
    # Stat fields overwrite player fields on collision (position: "F" from stats overwrites "C" from player)
    assert entry["position"] == "F"
    assert entry["goals"] == 50
    assert entry["firstName"] == "Auston"

    # Unmatched stat entries (playerId 999) are still included
    unmatched = [e for e in result if e.get("playerId") == 999]
    assert len(unmatched) >= 1
    assert unmatched[0]["goals"] == 10


@mock.patch("nhlpy.api.helpers.time")
@mock.patch("nhlpy.api.helpers.Stats")
@mock.patch("nhlpy.api.helpers.Teams")
@mock.patch.object(Helpers, "all_players")
def test_all_players_summary_statistics_empty_teams(mock_all_players, MockTeams, MockStats, mock_time, nhl_client):
    mock_all_players.return_value = []
    MockTeams.return_value.teams.return_value = []

    result = nhl_client.helpers.all_players_summary_statistics("20242025")

    assert result == []
    MockStats.return_value.skater_stats_with_query_context.assert_not_called()
