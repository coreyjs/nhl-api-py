from typing import Union

from nhlpy.api.query.filters import QueryBase


class HomeRoadQuery(QueryBase):
    def __init__(self, home_road: str):
        """
        H or R to indicate home or road games.
        :param home_road:
        """
        self.home_road = home_road
        self._home_road_q = "homeRoad"

    def to_query(self) -> str:
        return f"{self._home_road_q}='{self.home_road}'"

    def validate(self) -> Union[bool, None]:
        return True
