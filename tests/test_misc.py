from unittest import mock


@mock.patch("httpx.Client.get")
def test_glossary(mock_get, nhl_client):
    mock_get.return_value.json.return_value = {"data": [{"id": 1}]}
    assert nhl_client.misc.glossary() == [{"id": 1}]
    assert mock_get.call_args[1]["url"] == "https://api.nhle.com/stats/rest/en/glossary?sort=fullName"


@mock.patch("httpx.Client.get")
def test_how_to_watch(mock_get, nhl_client):
    nhl_client.misc.how_to_watch(game_id="2026020220")
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/how-to-watch/2026020220"


@mock.patch("httpx.Client.get")
def test_tv_schedule_now(mock_get, nhl_client):
    nhl_client.misc.tv_schedule()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/network/tv-schedule/now"


@mock.patch("httpx.Client.get")
def test_tv_schedule_date(mock_get, nhl_client):
    nhl_client.misc.tv_schedule(date="2025-01-07")
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/network/tv-schedule/2025-01-07"


@mock.patch("httpx.Client.get")
def test_player_spotlight(mock_get, nhl_client):
    mock_get.return_value.json.return_value = [{"playerId": 8484801}]
    assert nhl_client.misc.player_spotlight() == [{"playerId": 8484801}]
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/player-spotlight"


@mock.patch("httpx.Client.get")
def test_goal_replay(mock_get, nhl_client):
    nhl_client.misc.goal_replay(game_id="2024020641", event_id="121")
    mock_get.assert_called_once()
    assert mock_get.call_args[1]["url"] == "https://api-web.nhle.com/v1/ppt-replay/goal/2024020641/121"
