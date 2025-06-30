import pytest
from unittest.mock import Mock, patch
from nhlpy.nhl_client import NHLClient
from nhlpy.api import teams, standings, schedule
from nhlpy.http_client import (
    NHLApiException,
    ResourceNotFoundException,
    RateLimitExceededException,
    ServerErrorException,
    BadRequestException,
    UnauthorizedException,
    HttpClient,
    Endpoint,
)


class MockResponse:
    """Mock httpx.Response for testing"""

    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.url = "https://api.nhle.com/test"

    def json(self):
        return self._json_data

    @property
    def is_success(self):
        return 200 <= self.status_code < 300


@pytest.fixture
def mock_config():
    """Fixture for config object"""
    config = Mock()
    config.debug = False
    config.ssl_verify = True
    config.timeout = 30
    config.follow_redirects = True
    config.api_web_base_url = "https://api.nhl.com"
    config.api_web_api_ver = "/v1"
    return config


@pytest.fixture
def http_client(mock_config):
    """Fixture for HttpClient instance"""
    return HttpClient(mock_config)


def test_nhl_client_responds_to_teams():
    c = NHLClient()
    assert c.teams is not None
    assert isinstance(c.teams, teams.Teams)


def test_nhl_client_responds_to_standings():
    c = NHLClient()
    assert c.standings is not None
    assert isinstance(c.standings, standings.Standings)


def test_nhl_client_responds_to_schedule():
    c = NHLClient()
    assert c.schedule is not None
    assert isinstance(c.schedule, schedule.Schedule)


@pytest.mark.parametrize(
    "status_code,expected_exception",
    [
        (404, ResourceNotFoundException),
        (429, RateLimitExceededException),
        (400, BadRequestException),
        (401, UnauthorizedException),
        (500, ServerErrorException),
        (502, ServerErrorException),
        (599, NHLApiException),
    ],
)
def test_http_client_error_handling(http_client, status_code, expected_exception):
    """Test different HTTP error status codes raise appropriate exceptions"""
    mock_response = MockResponse(status_code=status_code, json_data={"message": "Test error message"})

    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        with pytest.raises(expected_exception) as exc_info:
            http_client.get(endpoint=Endpoint.API_CORE, resource="/test")

        assert exc_info.value.status_code == status_code
        assert "Test error message" in str(exc_info.value)


def test_http_client_success_response(http_client):
    """Test successful HTTP response"""
    mock_response = MockResponse(status_code=200, json_data={"data": "test"})

    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        response = http_client.get(endpoint=Endpoint.API_CORE, resource="/test")
        assert response.status_code == 200


def test_http_client_non_json_error_response(http_client):
    """Test error response with non-JSON body still works"""
    mock_response = MockResponse(status_code=500)
    mock_response.json = Mock(side_effect=ValueError)  # Simulate JSON decode error

    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        with pytest.raises(ServerErrorException) as exc_info:
            http_client.get(endpoint=Endpoint.API_CORE, resource="test")

        assert exc_info.value.status_code == 500
        assert "Request to" in str(exc_info.value)


def test_http_client_get_by_url_with_params(http_client):
    """Test get_by_url method with query parameters"""
    mock_response = MockResponse(status_code=200, json_data={"data": "test"})
    query_params = {"season": "20232024"}

    with patch("httpx.Client") as mock_client:
        mock_instance = mock_client.return_value.__enter__.return_value
        mock_instance.get.return_value = mock_response

        response = http_client.get(endpoint=Endpoint.API_CORE, resource="test", query_params=query_params)

        mock_instance.get.assert_called_once_with(url="https://api.nhle.com/test", params=query_params)
        assert response.status_code == 200


def test_http_client_custom_error_message(http_client):
    """Test custom error message in JSON response"""
    custom_message = "Custom API error explanation"
    mock_response = MockResponse(status_code=400, json_data={"message": custom_message})

    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        with pytest.raises(BadRequestException) as exc_info:
            http_client.get(endpoint=Endpoint.API_CORE, resource="/test")

        assert custom_message in str(exc_info.value)
