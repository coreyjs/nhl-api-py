import httpx

from nhlpy.http_client import HttpClient


class AsyncHttpClient(HttpClient):
    def __init__(self, config) -> None:
        super().__init__(config)
        # self.async_client: httpx.AsyncClient = httpx.AsyncClient()

    async def get(self, resource: str) -> httpx.Response:
        """
        Method to make a get request to the NHL API.  This wraps the lib httpx functionality.
        :param resource:
        :return:
        """
        url: str = f"{self._config.api_web_base_url}{self._config.api_web_api_ver}{resource}"

        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, follow_redirects=True)
            data = resp.json()
            return data

    async def get_by_url(self, full_resource: str, query_params: dict = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=full_resource, params=query_params, follow_redirects=True)
            data = resp.json()
            return data
