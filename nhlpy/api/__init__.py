import httpx


class BaseNHLAPIClient:
    def __init__(self) -> None:
        self.base_url = "https://api-web.nhle.com"
        self.api_ver = "/v1/"

    def _get(self, resource: str) -> httpx.request:
        print(f"{self.base_url}{self.api_ver}{resource}")
        r: httpx.request = httpx.get(url=f"{self.base_url}{self.api_ver}{resource}")
        return r
