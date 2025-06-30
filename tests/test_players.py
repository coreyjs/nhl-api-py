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
    teams_result = nhl_client.teams.roster_by_team(team_abbr="TOR", season="20232024")

    # Both should make the same API call
    assert mock_get.call_count == 2
    for call in mock_get.call_args_list:
        assert call[1]["url"] == "https://api-web.nhle.com/v1/roster/TOR/20232024"

    # Both should return the same result
    assert players_result == teams_result
    assert players_result == {"roster": [{"name": "Test Player", "position": "C"}]}
