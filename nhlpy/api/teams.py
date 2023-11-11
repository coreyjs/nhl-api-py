from typing import List

from nhlpy.api import BaseNHLAPIClient


class Teams(BaseNHLAPIClient):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.nhle.com"
        self.api_ver = "/stats/rest/"

    def team_stats_summary(self, lang="en") -> List[dict]:
        """

        :param lang: Language param.  'en' for English, 'fr' for French
        :return:
        """
        return self._get(resource=f"{lang}/team/summary").json()["data"]
