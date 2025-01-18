import pytest
import json
import os
from nhlpy import NHLClient
from nhlpy.api.query.builder import QueryBuilder
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.query.filters.franchise import FranchiseQuery
import time


@pytest.fixture
def nhl_client():
    """Fixture to create an NHL client instance."""
    return NHLClient(verbose=True)


def save_json(data, filename):
    """
    Save data as a JSON file in the `nhlpy/data` directory.
    """
    output_dir = os.path.join("nhlpy", "data")
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved data to {filepath}")


def test_get_all_teams(nhl_client):
    """
    Test fetching all NHL teams and save to JSON.
    """
    teams = nhl_client.teams.teams_info()
    assert isinstance(teams, list), "Teams should be a list"
    assert len(teams) > 0, "Teams list should not be empty"
    save_json(teams, "teams.json")  # Save teams data as JSON


def test_get_roster_players(nhl_client):
    """
    Test fetching roster players for each team and save to JSON.
    """
    teams = nhl_client.teams.teams_info()
    for team in teams:
        players = nhl_client.teams.roster(team_abbr=team["abbr"], season="20242025")
        filename = f"{team['abbr']}_roster.json"
        save_json(players, filename)  # Save each team's roster as JSON


def test_get_player_summary_stats(nhl_client):
    """
    Test fetching summary statistics for players and save to JSON.
    """
    teams = nhl_client.teams.teams_info()
    query_builder = QueryBuilder()
    season_query = SeasonQuery(season_start="20242025", season_end="20242025")

    for team in teams:
        time.sleep(1)  # Pause to avoid rate limiting
        franchise_query = FranchiseQuery(franchise_id=team["franchise_id"])
        context = query_builder.build(filters=[franchise_query, season_query])

        data = nhl_client.stats.skater_stats_with_query_context(
            report_type="summary",
            query_context=context,
            aggregate=True,
        )
        if "data" in data:
            filename = f"{team['abbr']}_player_stats.json"
            save_json(data, filename)  # Save player stats for each team as JSON
