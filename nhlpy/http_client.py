import httpx
import logging


class HttpClient:
    def __init__(self, config) -> None:
        self._config = config
        if self._config.verbose:
            logging.basicConfig(level=logging.INFO)

    def get(self, resource: str) -> httpx.request:
        """
        Private method to make a get request to the NHL API.  This wraps the lib httpx functionality.
        :param resource:
        :return:
        """
        r: httpx.request = httpx.get(
            url=f"{self._config.api_web_base_url}{self._config.api_web_api_ver}{resource}", follow_redirects=True
        )

        if self._config.verbose:
            logging.info(f"API URL: {r.url}")

        return r

    def get_by_url(self, full_resource: str) -> httpx.request:
        """
        Private method to make a get request to any HTTP resource.  This wraps the lib httpx functionality.
        :param full_resource:  The full resource to get.
        :return:
        """
        r: httpx.request = httpx.get(url=full_resource, follow_redirects=True)

        if self._config.verbose:
            logging.info(f"API URL: {r.url}")

        return r
