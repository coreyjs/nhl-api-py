from unittest import mock
import json
from unittest.mock import MagicMock


@mock.patch("httpx.Client.get")
def test_roster(h_m, nhl_client):
    nhl_client.teams.roster_by_team(team_abbr="BUF", season="20202021")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == "https://api-web.nhle.com/v1/roster/BUF/20202021"



@mock.patch("httpx.Client.get")
def test_all_teams(mock_get, nhl_client):
    # Create mock responses for the two API calls

    # Mock response for standings data
    standings_mock_response = MagicMock()
    standings_mock_response.json.return_value = {
        "standings": [
            {
                "conferenceAbbrev": "E",
                "conferenceName": "Eastern",
                "divisionAbbrev": "A",
                "divisionName": "Atlantic",
                "teamName": {"default": "Boston Bruins"},
                "teamCommonName": {"default": "Bruins"},
                "teamAbbrev": {"default": "BOS"},
                "teamLogo": "https://assets.nhle.com/logos/nhl/svg/BOS_light.svg"
            },
            {
                "conferenceAbbrev": "W",
                "conferenceName": "Western",
                "divisionAbbrev": "C",
                "divisionName": "Central",
                "teamName": {"default": "Colorado Avalanche"},
                "teamCommonName": {"default": "Avalanche"},
                "teamAbbrev": {"default": "COL"},
                "teamLogo": "https://assets.nhle.com/logos/nhl/svg/COL_light.svg"
            },
            {
                "conferenceAbbrev": "E",
                "conferenceName": "Eastern",
                "divisionAbbrev": "A",
                "divisionName": "Atlantic",
                "teamName": {"default": "Montreal Canadiens"},
                "teamCommonName": {"default": "Canadiens"},
                "teamAbbrev": {"default": "MTL"},
                "teamLogo": "https://assets.nhle.com/logos/nhl/svg/MTL_light.svg"
            },
            {
                "conferenceAbbrev": "E",
                "conferenceName": "Eastern",
                "divisionAbbrev": "M",
                "divisionName": "Metropolitan",
                "teamName": {"default": "New Team"},
                "teamCommonName": {"default": "New Team"},
                "teamAbbrev": {"default": "NEW"},
                "teamLogo": "https://assets.nhle.com/logos/nhl/svg/NEW_light.svg"
            }
        ]
    }

    # Mock response for franchise data
    franchise_mock_response = MagicMock()
    franchise_mock_response.json.return_value = {
        "data": [
            {
                "id": 6,
                "fullName": "Boston Bruins",
                "teamCommonName": "Bruins"
            },
            {
                "id": 27,
                "fullName": "Colorado Avalanche",
                "teamCommonName": "Avalanche"
            },
            {
                "id": 1,
                "fullName": "Montréal Canadiens",  # Note the accent, different from "Montreal Canadiens"
                "teamCommonName": "Canadiens"
            }
            # No entry for "New Team" - testing case where franchise ID is not found
        ]
    }

    # Configure the mock to return different responses based on the URL
    def side_effect(url, **kwargs):
        if "standings" in url:
            return standings_mock_response
        elif "franchise" in url:
            return franchise_mock_response
        return MagicMock()

    mock_get.side_effect = side_effect

    # Call the method being tested
    teams = nhl_client.teams.teams()

    # Verify the mock was called twice with the correct URLs
    assert mock_get.call_count == 2
    calls = mock_get.call_args_list
    assert "standings/now" in calls[0][1]["url"]
    assert "franchise" in calls[1][1]["url"]

    # Verify the output contains the expected data
    assert len(teams) == 4

    # Check first team - direct match
    assert teams[0]["name"] == "Boston Bruins"
    assert teams[0]["common_name"] == "Bruins"
    assert teams[0]["abbr"] == "BOS"
    assert teams[0]["conference"]["abbr"] == "E"
    assert teams[0]["conference"]["name"] == "Eastern"
    assert teams[0]["division"]["abbr"] == "A"
    assert teams[0]["division"]["name"] == "Atlantic"
    assert teams[0]["franchise_id"] == 6

    # Check second team - direct match
    assert teams[1]["name"] == "Colorado Avalanche"
    assert teams[1]["common_name"] == "Avalanche"
    assert teams[1]["abbr"] == "COL"
    assert teams[1]["conference"]["abbr"] == "W"
    assert teams[1]["conference"]["name"] == "Western"
    assert teams[1]["division"]["abbr"] == "C"
    assert teams[1]["division"]["name"] == "Central"
    assert teams[1]["franchise_id"] == 27

    # Check third team - special case for Canadiens (partial match)
    assert teams[2]["name"] == "Montreal Canadiens"
    assert teams[2]["common_name"] == "Canadiens"
    assert teams[2]["abbr"] == "MTL"
    assert teams[2]["conference"]["abbr"] == "E"
    assert teams[2]["conference"]["name"] == "Eastern"
    assert teams[2]["division"]["abbr"] == "A"
    assert teams[2]["division"]["name"] == "Atlantic"
    assert teams[2]["franchise_id"] == 1  # Should find the franchise ID despite different spelling

    # Check fourth team - no franchise ID match
    assert teams[3]["name"] == "New Team"
    assert teams[3]["common_name"] == "New Team"
    assert teams[3]["abbr"] == "NEW"
    assert teams[3]["conference"]["abbr"] == "E"
    assert teams[3]["conference"]["name"] == "Eastern"
    assert teams[3]["division"]["abbr"] == "M"
    assert teams[3]["division"]["name"] == "Metropolitan"
    assert "franchise_id" not in teams[3]  # Should not have a franchise_id
