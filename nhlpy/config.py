class ClientConfig:
    def __init__(
        self, debug: bool = False, timeout: int = 10, ssl_verify: bool = True, follow_redirects: bool = True
    ) -> None:
        self.debug = debug
        self.timeout = timeout
        self.ssl_verify = ssl_verify
        self.follow_redirects = follow_redirects

        self.api_web_base_url = "https://api-web.nhle.com"
        self.api_base_url = "https://api.nhle.com"
        self.api_web_api_ver = "/v1/"
