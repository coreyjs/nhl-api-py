from unittest import mock

import pytest

from nhlpy.api.draft import Draft


def test_client_has_draft_module(nhl_client):
    assert isinstance(nhl_client.draft, Draft)


@mock.patch("httpx.Client.get")
def test_rankings_now(mock_get, nhl_client):
    nhl_client.draft.rankings()
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/draft/rankings/now"


@mock.patch("httpx.Client.get")
def test_rankings_year_defaults_to_category_1(mock_get, nhl_client):
    nhl_client.draft.rankings(year="2025")
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/draft/rankings/2025/1"


@mock.patch("httpx.Client.get")
def test_rankings_year_and_category(mock_get, nhl_client):
    nhl_client.draft.rankings(year="2025", category=4)
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/draft/rankings/2025/4"


@pytest.mark.parametrize("category", [0, 5, "1"])
@mock.patch("httpx.Client.get")
def test_rankings_invalid_category(mock_get, nhl_client, category):
    with pytest.raises(ValueError, match="Valid values"):
        nhl_client.draft.rankings(year="2025", category=category)
    mock_get.assert_not_called()


@mock.patch("httpx.Client.get")
def test_picks_now(mock_get, nhl_client):
    nhl_client.draft.picks()
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/draft/picks/now"


@mock.patch("httpx.Client.get")
def test_picks_year_defaults_to_all_rounds(mock_get, nhl_client):
    nhl_client.draft.picks(year="2024")
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/draft/picks/2024/all"


@pytest.mark.parametrize("draft_round", [1, "7"])
@mock.patch("httpx.Client.get")
def test_picks_year_and_round(mock_get, nhl_client, draft_round):
    nhl_client.draft.picks(year="2024", draft_round=draft_round)
    assert mock_get.call_args[1]["url"] == f"https://api-web.nhle.com/v1/draft/picks/2024/{draft_round}"


@pytest.mark.parametrize("draft_round", [0, 8, "first"])
@mock.patch("httpx.Client.get")
def test_picks_invalid_round(mock_get, nhl_client, draft_round):
    with pytest.raises(ValueError, match="Valid values"):
        nhl_client.draft.picks(year="2024", draft_round=draft_round)
    mock_get.assert_not_called()


@mock.patch("httpx.Client.get")
def test_tracker_now(mock_get, nhl_client):
    nhl_client.draft.tracker()
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/draft-tracker/picks/now"


@mock.patch("httpx.Client.get")
def test_tracker_year(mock_get, nhl_client):
    nhl_client.draft.tracker(year="2025")
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/draft-tracker/picks/2025"
