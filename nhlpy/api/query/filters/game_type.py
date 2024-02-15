from typing import Union

from nhlpy.api.query.builder import QueryBase


class GameTypeQuery(QueryBase):
    def __init__(self, game_type: str):
        self.game_type = game_type
        self._game_type_q = "gameTypeId"

    def to_query(self) -> str:
        return f"{self._game_type_q}={self.game_type}"

    def validate(self) -> Union[bool, None]:
        return True
