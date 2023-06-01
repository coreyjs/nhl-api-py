import httpx

class BaseNHLAPIClient:
    def __init__(self) -> None:
        self.base_url = "https://statsapi.web.nhl.com"
        self.api_ver = "/api/v1/"

    def _get(self, resource: str) -> httpx.request:
        r: httpx.request = httpx.get(f"{self.base_url}{self.api_ver}{resource}")
        return r