from unittest import mock
from unittest.mock import MagicMock


@mock.patch("httpx.Client.get")
def test_prospects_by_team(mock_get, nhl_client):
    """Test the prospects_by_team method."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"prospects": [{"name": "Test Prospect"}]}
    mock_get.return_value = mock_response

    result = nhl_client.players.prospects_by_team(team_abbr="BUF")

    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/prospects/BUF"
    assert result == {"prospects": [{"name": "Test Prospect"}]}


@mock.patch("httpx.Client.get")
def test_players_by_team(mock_get, nhl_client):
    """Test the players_by_team method - should behave identically to teams.roster_by_team."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"roster": [{"name": "Test Player"}]}
    mock_get.return_value = mock_response

    result = nhl_client.players.players_by_team(team_abbr="BUF", season="20202021")

    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/roster/BUF/20202021"
    assert result == {"roster": [{"name": "Test Player"}]}


@mock.patch("httpx.Client.get")
def test_players_by_team_same_as_teams_roster(mock_get, nhl_client):
    """Test that players_by_team returns the same data as teams.roster_by_team."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"roster": [{"name": "Test Player", "position": "C"}]}
    mock_get.return_value = mock_response

    # Call both methods with the same parameters
    players_result = nhl_client.players.players_by_team(team_abbr="TOR", season="20232024")
    teams_result = nhl_client.teams.team_roster(team_abbr="TOR", season="20232024")

    # Both should make the same API call
    assert mock_get.call_count == 2
    for call in mock_get.call_args_list:
        assert call[1]["url"] == "https://api-web.nhle.com/v1/roster/TOR/20232024"

    # Both should return the same result
    assert players_result == teams_result
    assert players_result == {"roster": [{"name": "Test Player", "position": "C"}]}


@mock.patch("httpx.Client.get")
def test_player_bio(mock_get, nhl_client):
    """Test the player_bio method uses the v2 player bio endpoint."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"vitals": {"birthDate": "1998-12-08"}, "bio": {"lastName": {"default": "Dunne"}}}
    mock_get.return_value = mock_response

    result = nhl_client.players.player_bio(player_id="8482623")

    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v2/player/8482623/bio"
    assert result == {"vitals": {"birthDate": "1998-12-08"}, "bio": {"lastName": {"default": "Dunne"}}}


@mock.patch("httpx.Client.get")
def test_player_header(mock_get, nhl_client):
    """Test the player_header method uses the v2 player header endpoint."""
    mock_get.return_value.json.return_value = {"playerId": 8478402}

    result = nhl_client.players.player_header(player_id="8478402")

    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v2/player/8478402/header"
    assert result == {"playerId": 8478402}


@mock.patch("httpx.Client.get")
def test_player_home(mock_get, nhl_client):
    """Test the player_home method uses the v2 player home endpoint."""
    mock_get.return_value.json.return_value = {"teamAbbrev": "EDM"}

    result = nhl_client.players.player_home(player_id="8478402")

    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v2/player/8478402/home"
    assert result == {"teamAbbrev": "EDM"}


@mock.patch("httpx.Client.get")
def test_player_stats(mock_get, nhl_client):
    """Test the player_stats method uses the v2 player-stats endpoint."""
    mock_get.return_value.json.return_value = {"careerTotals": {}}

    result = nhl_client.players.player_stats(player_id="8478402")

    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v2/player/8478402/player-stats"
    assert result == {"careerTotals": {}}


@mock.patch("httpx.Client.get")
def test_player_game_log_now(mock_get, nhl_client):
    """Test the v2 player_game_log defaults to the current season."""
    mock_get.return_value.json.return_value = {"gameLog": []}

    result = nhl_client.players.player_game_log(player_id="8478402")

    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v2/player/8478402/game-log/now"
    assert result == {"gameLog": []}


@mock.patch("httpx.Client.get")
def test_player_game_log_season(mock_get, nhl_client):
    """Test the v2 player_game_log with an explicit season and game type."""
    mock_get.return_value.json.return_value = {"gameLog": []}

    nhl_client.players.player_game_log(player_id="8478402", season="20242025", game_type=3)

    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v2/player/8478402/game-log/20242025/3"
