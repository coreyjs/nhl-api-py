from typing import Union

from nhlpy.api.query.builder import QueryBase


class ShootCatchesQuery(QueryBase):
    def __init__(self, shoot_catch: str):
        """
        Shoot / catch filter.  L or R, for both I believe its nothing.
        :param shoot_catch: L, R
        """
        self.shoot_catch = shoot_catch
        self.shoot_catch_q = "shootsCatches"

    def to_query(self) -> str:
        return f"{self.shoot_catch_q}='{self.shoot_catch}'"

    def validate(self) -> Union[bool, None]:
        return True
