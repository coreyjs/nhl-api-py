from typing import Union

from nhlpy.api.query.builder import QueryBase


class NationalityQuery(QueryBase):
    """
    Country/Nationality codes can be found via client.misc.countries() endpoint.  As of 2/15/24 these are the codes"
    [
        "AUS", "AUT", "BEL", "BHS", "BLR", "BRA",
        "CAN", "CHE", "CHN", "DEU", "DNK", "EST",
        "FIN", "FRA", "GBR", "GRC", "GUY", "HRV",
        "HTI", "HUN", "IRL", "ISR", "ITA", "JAM",
        "JPN", "KAZ", "KOR", "LBN", "LTU", "LVA",
        "MEX", "NGA", "NLD", "NOR", "POL", "PRY",
        "ROU", "RUS", "SRB", "SVK", "SVN", "SWE",
        "THA", "UKR", "USA", "VEN", "YUG", "ZAF",
        "CZE"
    ]

    """

    def __init__(self, nation_code: str):
        self.nation_code = nation_code
        self._nation_q = "nationalityCode"

    def validate(self) -> Union[bool, None]:
        return True

    def to_query(self) -> str:
        return f"{self._nation_q}='{self.nation_code}'"
