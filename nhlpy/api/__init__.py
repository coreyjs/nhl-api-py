# import httpx
#
#
# class BaseHttpClient:
#     def __init__(self, config) -> None:
#         self.config = config
#
#     def _get(self, resource: str) -> httpx.request:
#         """
#         Private method to make a get request to the NHL API.  This wraps the lib httpx functionality.
#         :param resource:
#         :return:
#         """
#         if self.config.verbose:
#             print(f"API URL: {self.config.api_web_api_ver}{self.config.api_web_api_ver}{resource}")
#         r: httpx.request = httpx.get(
#             url=f"{self.config.api_web_base_url}{self.config.api_web_api_ver}{resource}", follow_redirects=True
#         )
#         return r
#
#     def _get_plain(self, full_resource: str) -> httpx.request:
#         """
#         Private method to make a get request to any HTTP resource.  This wraps the lib httpx functionality.
#         :param full_resource:  The full resource to get.
#         :return:
#         """
#         if self.config.verbose:
#             print(f"API URL: {full_resource}")
#         r: httpx.request = httpx.get(url=full_resource, follow_redirects=True)
#         return r.text
