import httpx
import logging


class HttpClient:
    def __init__(self, config) -> None:
        self._config = config
        if self._config.verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.WARNING)

    def get(self, resource: str) -> httpx.request:
        """
        Private method to make a get request to the NHL API.  This wraps the lib httpx functionality.
        :param resource:
        :return:
        """
        with httpx.Client(
            verify=self._config.ssl_verify, timeout=self._config.timeout, follow_redirects=self._config.follow_redirects
        ) as client:
            r: httpx.request = client.get(url=f"{self._config.api_web_base_url}{self._config.api_web_api_ver}{resource}")

        if self._config.verbose:
            logging.info(f"API URL: {r.url}")

        return r

    def get_by_url(self, full_resource: str, query_params: dict = None) -> httpx.request:
        """
        Private method to make a get request to any HTTP resource.  This wraps the lib httpx functionality.
        :param query_params:
        :param full_resource:  The full resource to get.
        :return:
        """
        with httpx.Client(
            verify=self._config.ssl_verify, timeout=self._config.timeout, follow_redirects=self._config.follow_redirects
        ) as client:
            r: httpx.request = client.get(url=full_resource, params=query_params)

        if self._config.verbose:
            logging.info(f"API URL: {r.url}")

        return r
