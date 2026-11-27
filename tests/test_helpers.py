# Tests for nhlpy/api/helpers.py
#
# Unlike other test modules that mock at the HTTP transport layer (httpx.Client.get),
# these tests mock at the API class level because Helpers orchestrates multiple API
# modules and HTTP-level mocking would be impractically complex.

from unittest import mock

import pytest

from nhlpy.api.helpers import Helpers, _build_game_goals, _clock_to_seconds
from nhlpy.http_client import ServerErrorException


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


# -- game_goals tests --


def _spot(player_id, team_id, first, last, number, position):
    return {
        "playerId": player_id,
        "teamId": team_id,
        "firstName": {"default": first},
        "lastName": {"default": last},
        "sweaterNumber": number,
        "positionCode": position,
        "headshot": f"https://assets.nhle.com/mugs/{player_id}.png",
    }


def _play(event_id, type_key, period, clock, details=None, period_type="REG", **extra):
    return {
        "eventId": event_id,
        "typeDescKey": type_key,
        "periodDescriptor": {"number": period, "periodType": period_type},
        "timeInPeriod": clock,
        "situationCode": "1551",
        "homeTeamDefendingSide": "left",
        "details": details or {},
        **extra,
    }


def _shift(player_id, team, period, start, end, type_code=517, **extra):
    return {
        "playerId": player_id,
        "teamAbbrev": team,
        "period": period,
        "startTime": start,
        "endTime": end,
        "typeCode": type_code,
        **extra,
    }


@pytest.fixture
def mock_goals_pbp():
    """BUF (home, id 7) vs TOR (away, id 10): a home goal in P1, an away empty-net goal in P3, a shootout attempt."""
    return {
        "id": 2024020001,
        "gameState": "OFF",
        "homeTeam": {"id": 7, "abbrev": "BUF", "logo": "buf.svg", "darkLogo": "buf_dark.svg"},
        "awayTeam": {"id": 10, "abbrev": "TOR", "logo": "tor.svg", "darkLogo": "tor_dark.svg"},
        "rosterSpots": [
            _spot(1, 7, "Tage", "Thompson", 72, "C"),
            _spot(2, 7, "Rasmus", "Dahlin", 26, "D"),
            _spot(3, 7, "Ukko-Pekka", "Luukkonen", 1, "G"),
            _spot(4, 10, "Auston", "Matthews", 34, "C"),
            _spot(5, 10, "Joseph", "Woll", 60, "G"),
        ],
        "plays": [
            _play(50, "faceoff", 1, "09:15"),
            _play(
                101,
                "goal",
                1,
                "10:00",
                {
                    "xCoord": 80,
                    "yCoord": -5,
                    "zoneCode": "O",
                    "shotType": "wrist",
                    "eventOwnerTeamId": 7,
                    "scoringPlayerId": 1,
                    "assist1PlayerId": 2,
                    "goalieInNetId": 5,
                    "awayScore": 0,
                    "homeScore": 1,
                    "highlightClipSharingUrl": "https://nhl.com/video/101",
                },
                pptReplayUrl="https://wsr.nhle.com/sprites/20242025/2024020001/ev101.json",
            ),
            # Unassisted, no coordinates, scorer missing from rosterSpots, home net empty.
            _play(
                202,
                "goal",
                3,
                "19:30",
                {"eventOwnerTeamId": 10, "scoringPlayerId": 99, "awayScore": 1, "homeScore": 1},
                situationCode="1560",
            ),
            _play(303, "goal", 5, "00:00", {"eventOwnerTeamId": 10, "scoringPlayerId": 4}, period_type="SO"),
        ],
    }


@pytest.fixture
def mock_goals_shifts():
    """Shift rows around goal 101 (period 1, 10:00)."""
    return [
        _shift(1, "BUF", 1, "09:15", "10:00"),  # ends at the goal second: on the ice
        _shift(2, "BUF", 1, "09:30", "10:20"),
        _shift(2, "BUF", 1, "09:30", "10:20"),  # duplicate row: listed once
        _shift(3, "BUF", 1, "00:00", "20:00"),
        _shift(5, "TOR", 1, "00:00", "20:00"),
        _shift(98, "TOR", 1, "09:40", "10:30", firstName="Not", lastName="Rostered"),
        _shift(4, "TOR", 1, "10:00", "10:45"),  # starts at the goal second: next faceoff, not on the ice
        _shift(4, "TOR", 2, "09:30", "10:20"),  # other period
        _shift(4, "TOR", 1, None, "10:30"),  # malformed time: skipped
        _shift(4, "TOR", 1, "09:00", "11:00", type_code=505),  # goal row, not a shift
    ]


def test_build_game_goals_game_fields(mock_goals_pbp):
    result = _build_game_goals(mock_goals_pbp, None)

    assert result["game_id"] == 2024020001
    assert result["game_state"] == "OFF"
    assert result["home_team"] == {"id": 7, "abbr": "BUF", "logo": "buf.svg", "dark_logo": "buf_dark.svg"}
    assert result["away_team"] == {"id": 10, "abbr": "TOR", "logo": "tor.svg", "dark_logo": "tor_dark.svg"}


def test_build_game_goals_skips_shootout_and_other_plays(mock_goals_pbp):
    result = _build_game_goals(mock_goals_pbp, None)

    assert [g["event_id"] for g in result["goals"]] == [101, 202]


def test_build_game_goals_goal_fields(mock_goals_pbp):
    goal = _build_game_goals(mock_goals_pbp, None)["goals"][0]

    assert goal["period"] == 1
    assert goal["period_type"] == "REG"
    assert goal["time_in_period"] == "10:00"
    assert goal["situation_code"] == "1551"
    assert goal["team_abbr"] == "BUF"
    assert goal["is_home"] is True
    assert goal["home_team_defending_side"] == "left"
    assert (goal["x"], goal["y"], goal["zone"], goal["shot_type"]) == (80, -5, "O", "wrist")
    assert (goal["away_score"], goal["home_score"]) == (0, 1)
    assert goal["highlight_clip_url"] == "https://nhl.com/video/101"
    assert goal["ppt_replay_url"] == "https://wsr.nhle.com/sprites/20242025/2024020001/ev101.json"
    assert goal["scorer"] == {
        "player_id": 1,
        "first_name": "Tage",
        "last_name": "Thompson",
        "sweater_number": 72,
        "position": "C",
        "team_abbr": "BUF",
        "headshot": "https://assets.nhle.com/mugs/1.png",
    }
    assert [a["last_name"] for a in goal["assists"]] == ["Dahlin"]
    assert goal["goalie"]["last_name"] == "Woll"
    assert goal["goalie"]["team_abbr"] == "TOR"


def test_build_game_goals_missing_data(mock_goals_pbp):
    goal = _build_game_goals(mock_goals_pbp, None)["goals"][1]

    assert goal["team_abbr"] == "TOR"
    assert goal["is_home"] is False
    assert goal["assists"] == []
    assert goal["goalie"] is None
    assert (goal["x"], goal["y"], goal["zone"], goal["shot_type"]) == (None, None, None, None)
    assert goal["highlight_clip_url"] is None
    assert goal["ppt_replay_url"] is None
    assert goal["scorer"] == {
        "player_id": 99,
        "first_name": None,
        "last_name": None,
        "sweater_number": None,
        "position": None,
        "team_abbr": None,
        "headshot": None,
    }


def test_build_game_goals_on_ice(mock_goals_pbp, mock_goals_shifts):
    on_ice = _build_game_goals(mock_goals_pbp, mock_goals_shifts)["goals"][0]["on_ice"]

    # Sorted by team, then position (C, L, R, D, G, unknown).
    assert [p["player_id"] for p in on_ice] == [1, 2, 3, 5, 98]
    assert on_ice[0]["last_name"] == "Thompson"
    # Not in rosterSpots: name and team come from the shift row.
    assert on_ice[-1] == {
        "player_id": 98,
        "first_name": "Not",
        "last_name": "Rostered",
        "sweater_number": None,
        "position": None,
        "team_abbr": "TOR",
        "headshot": None,
    }


def test_build_game_goals_on_ice_is_none_without_shift_data(mock_goals_pbp, mock_goals_shifts):
    with_shifts = _build_game_goals(mock_goals_pbp, mock_goals_shifts)["goals"]

    assert with_shifts[1]["on_ice"] is None  # no shift rows for period 3
    assert all(g["on_ice"] is None for g in _build_game_goals(mock_goals_pbp, None)["goals"])
    assert all(g["on_ice"] is None for g in _build_game_goals(mock_goals_pbp, [])["goals"])


@pytest.mark.parametrize(
    "clock, expected",
    [("05:47", 347), ("00:00", 0), ("20:00", 1200), (None, None), ("", None), ("5:4x", None), ("1:02:03", None)],
)
def test_clock_to_seconds(clock, expected):
    assert _clock_to_seconds(clock) == expected


@mock.patch("nhlpy.api.helpers.GameCenter")
def test_game_goals(MockGameCenter, nhl_client, mock_goals_pbp, mock_goals_shifts):
    MockGameCenter.return_value.play_by_play.return_value = mock_goals_pbp
    MockGameCenter.return_value.shift_chart_data.return_value = {"data": mock_goals_shifts}

    result = nhl_client.helpers.game_goals(game_id="2024020001")

    MockGameCenter.return_value.play_by_play.assert_called_once_with("2024020001")
    MockGameCenter.return_value.shift_chart_data.assert_called_once_with("2024020001")
    assert [p["player_id"] for p in result["goals"][0]["on_ice"]] == [1, 2, 3, 5, 98]


@mock.patch("nhlpy.api.helpers.GameCenter")
def test_game_goals_without_on_ice(MockGameCenter, nhl_client, mock_goals_pbp):
    MockGameCenter.return_value.play_by_play.return_value = mock_goals_pbp

    result = nhl_client.helpers.game_goals(game_id="2024020001", include_on_ice=False)

    MockGameCenter.return_value.shift_chart_data.assert_not_called()
    assert all(g["on_ice"] is None for g in result["goals"])


@mock.patch("nhlpy.api.helpers.GameCenter")
def test_game_goals_raises_shift_chart_errors(MockGameCenter, nhl_client, mock_goals_pbp):
    MockGameCenter.return_value.play_by_play.return_value = mock_goals_pbp
    MockGameCenter.return_value.shift_chart_data.side_effect = ServerErrorException("boom", 503)

    with pytest.raises(ServerErrorException):
        nhl_client.helpers.game_goals(game_id="2024020001")


@pytest.mark.parametrize("game_id", ["abc", "", "20240200", "20240200011", "2024020001 or 1=1"])
@mock.patch("nhlpy.api.helpers.GameCenter")
def test_game_goals_rejects_invalid_game_id(MockGameCenter, game_id, nhl_client):
    with pytest.raises(ValueError, match="10-digit"):
        nhl_client.helpers.game_goals(game_id=game_id)

    MockGameCenter.assert_not_called()
