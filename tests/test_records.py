import json
from unittest import mock

BASE = "https://records.nhl.com/site/api/"


@mock.patch("httpx.Client.get")
def test_query_no_params(h_m, nhl_client):
    nhl_client.records.query("goalie-shutout-streak")
    h_m.assert_called_once()
    assert h_m.call_args[1]["url"] == f"{BASE}goalie-shutout-streak"
    assert h_m.call_args[1]["params"] == {}


@mock.patch("httpx.Client.get")
def test_query_all_params(h_m, nhl_client):
    nhl_client.records.query(
        "skater-career-scoring-regular-season", cayenne_exp="franchiseId=7", sort="points", limit=10, start=20
    )
    assert h_m.call_args[1]["url"] == f"{BASE}skater-career-scoring-regular-season"
    params = h_m.call_args[1]["params"]
    assert params["cayenneExp"] == "franchiseId=7"
    assert json.loads(params["sort"]) == [{"property": "points", "direction": "DESC"}]
    assert params["limit"] == 10
    assert params["start"] == 20


@mock.patch("httpx.Client.get")
def test_query_sort_list(h_m, nhl_client):
    nhl_client.records.query("draft", sort=[("draftYear", "DESC"), ("overallPickNumber", "ASC")])
    assert json.loads(h_m.call_args[1]["params"]["sort"]) == [
        {"property": "draftYear", "direction": "DESC"},
        {"property": "overallPickNumber", "direction": "ASC"},
    ]


@mock.patch("httpx.Client.get")
def test_query_returns_raw_response(h_m, nhl_client):
    h_m.return_value.json.return_value = {"data": [{"id": 1}], "total": 1}
    assert nhl_client.records.query("franchise") == {"data": [{"id": 1}], "total": 1}


@mock.patch("httpx.Client.get")
def test_curated_methods_unwrap_data(h_m, nhl_client):
    h_m.return_value.json.return_value = {"data": [{"id": 1}], "total": 1}
    assert nhl_client.records.franchises() == [{"id": 1}]


@mock.patch("httpx.Client.get")
def test_franchises(h_m, nhl_client):
    nhl_client.records.franchises()
    assert h_m.call_args[1]["url"] == f"{BASE}franchise"
    assert h_m.call_args[1]["params"] == {}


@mock.patch("httpx.Client.get")
def test_franchise_detail(h_m, nhl_client):
    nhl_client.records.franchise_detail(team_id=7)
    assert h_m.call_args[1]["url"] == f"{BASE}franchise-detail"
    assert h_m.call_args[1]["params"] == {"cayenneExp": "mostRecentTeamId=7"}


@mock.patch("httpx.Client.get")
def test_franchise_totals(h_m, nhl_client):
    nhl_client.records.franchise_totals(franchise_id=19, game_type_id=2)
    assert h_m.call_args[1]["url"] == f"{BASE}franchise-totals"
    assert h_m.call_args[1]["params"] == {"cayenneExp": "franchiseId=19 and gameTypeId=2"}


@mock.patch("httpx.Client.get")
def test_franchise_team_totals(h_m, nhl_client):
    nhl_client.records.franchise_team_totals(franchise_id=27)
    assert h_m.call_args[1]["url"] == f"{BASE}franchise-team-totals"
    assert h_m.call_args[1]["params"] == {"cayenneExp": "franchiseId=27"}


@mock.patch("httpx.Client.get")
def test_franchise_season_results(h_m, nhl_client):
    nhl_client.records.franchise_season_results(franchise_id=19, season_id=20232024, game_type_id=2, limit=5)
    assert h_m.call_args[1]["url"] == f"{BASE}franchise-season-results"
    assert h_m.call_args[1]["params"] == {
        "cayenneExp": "franchiseId=19 and seasonId=20232024 and gameTypeId=2",
        "limit": 5,
    }


@mock.patch("httpx.Client.get")
def test_franchise_playoff_appearances(h_m, nhl_client):
    nhl_client.records.franchise_playoff_appearances()
    assert h_m.call_args[1]["url"] == f"{BASE}franchise-playoff-appearances"
    assert h_m.call_args[1]["params"] == {}


@mock.patch("httpx.Client.get")
def test_attendance(h_m, nhl_client):
    nhl_client.records.attendance(season_id=20232024)
    assert h_m.call_args[1]["url"] == f"{BASE}attendance"
    assert h_m.call_args[1]["params"] == {"cayenneExp": "seasonId=20232024"}


@mock.patch("httpx.Client.get")
def test_venues_quotes_strings(h_m, nhl_client):
    nhl_client.records.venues(country_code="CAN")
    assert h_m.call_args[1]["url"] == f"{BASE}venue"
    assert h_m.call_args[1]["params"] == {"cayenneExp": 'countryCode="CAN"'}


@mock.patch("httpx.Client.get")
def test_draft(h_m, nhl_client):
    nhl_client.records.draft(draft_year=2024, round_number=1, team_abbr="BUF")
    assert h_m.call_args[1]["url"] == f"{BASE}draft"
    assert h_m.call_args[1]["params"] == {"cayenneExp": 'draftYear=2024 and roundNumber=1 and triCode="BUF"'}


@mock.patch("httpx.Client.get")
def test_draft_by_team(h_m, nhl_client):
    nhl_client.records.draft_by_team(team_id=7)
    assert h_m.call_args[1]["url"] == f"{BASE}draft/byTeam/7"


@mock.patch("httpx.Client.get")
def test_draft_lottery_odds(h_m, nhl_client):
    nhl_client.records.draft_lottery_odds(draft_year=2024)
    assert h_m.call_args[1]["url"] == f"{BASE}draft-lottery-odds"
    assert h_m.call_args[1]["params"] == {"cayenneExp": "draftYear=2024"}
