from enum import Enum
from typing import Optional

import httpx
import logging


class Endpoint(Enum):
    API_WEB_V1 = "https://api-web.nhle.com/v1/"
    API_CORE = "https://api.nhle.com/"
    API_STATS = "https://api.nhle.com/stats/rest/"


class NHLApiErrorCode(Enum):
    """Enum for NHL API specific error codes if any"""

    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    SERVER_ERROR = "SERVER_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"


class NHLApiException(Exception):
    """Base exception for NHL API errors"""

    def __init__(self, message: str, status_code: int, error_code: Optional[NHLApiErrorCode] = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class ResourceNotFoundException(NHLApiException):
    """Raised when a resource is not found (404)"""

    def __init__(self, message: str, status_code: int = 404):
        super().__init__(message, status_code, NHLApiErrorCode.RESOURCE_NOT_FOUND)


class RateLimitExceededException(NHLApiException):
    """Raised when rate limit is exceeded (429)"""

    def __init__(self, message: str, status_code: int = 429):
        super().__init__(message, status_code, NHLApiErrorCode.RATE_LIMIT_EXCEEDED)


class ServerErrorException(NHLApiException):
    """Raised for server errors (5xx)"""

    def __init__(self, message: str, status_code: int):
        super().__init__(message, status_code, NHLApiErrorCode.SERVER_ERROR)


class BadRequestException(NHLApiException):
    """Raised for client errors (400)"""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code, NHLApiErrorCode.BAD_REQUEST)


class UnauthorizedException(NHLApiException):
    """Raised for authentication errors (401)"""

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code, NHLApiErrorCode.UNAUTHORIZED)


class HttpClient:
    def __init__(self, config) -> None:
        self._config = config
        if self._config.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARNING)

    def _handle_response(self, response: httpx.Response, url: str) -> None:
        """Handle different HTTP status codes and raise appropriate exceptions"""

        if response.is_success:
            return

        # Build error message
        error_message = f"Request to {url} failed"
        try:
            response_json = response.json()
            if isinstance(response_json, dict):
                error_detail = response_json.get("message")
                if error_detail:
                    error_message = f"{error_message}: {error_detail}"
        except Exception:
            # If response isn't JSON or doesn't have a message field
            pass

        if response.status_code == 404:
            raise ResourceNotFoundException(error_message)
        elif response.status_code == 429:
            raise RateLimitExceededException(error_message)
        elif response.status_code == 400:
            raise BadRequestException(error_message)
        elif response.status_code == 401:
            raise UnauthorizedException(error_message)
        elif 500 <= response.status_code < 600:
            raise ServerErrorException(error_message, response.status_code)
        else:
            raise NHLApiException(f"Unexpected error: {error_message}", response.status_code)

    def get(self, endpoint: Endpoint, resource: str, query_params: dict = None) -> httpx.Response:
        """
        Private method to make a get request to the NHL API.  This wraps the lib httpx functionality.
        :param resource:
        :return: httpx.Response
        :raises:
            ResourceNotFoundException: When the resource is not found
            RateLimitExceededException: When rate limit is exceeded
            ServerErrorException: When server returns 5xx error
            BadRequestException: When request is malformed
            UnauthorizedException: When authentication fails
            NHLApiException: For other unexpected errors

            url=f"{self._config.api_web_base_url}{self._config.api_web_api_ver}{resource}"
            )
        """
        with httpx.Client(
            verify=self._config.ssl_verify, timeout=self._config.timeout, follow_redirects=self._config.follow_redirects
        ) as client:
            r: httpx.Response = client.get(url=f"{endpoint.value}{resource}", params=query_params)

        self._handle_response(r, resource)
        return r
