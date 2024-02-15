from typing import Union
from enum import Enum

from nhlpy.api.query.builder import QueryBase


class PositionTypes(str, Enum):
    ALL_FORWARDS = "F"
    CENTER = "C"
    LEFT_WING = "L"
    RIGHT_WING = "R"
    DEFENSE = "D"


class PositionQuery(QueryBase):
    def __init__(self, position: PositionTypes):
        self.position = position
        self._position_q = "positionCode"

    def to_query(self) -> str:
        # All forwards require an OR clause
        if self.position == PositionTypes.ALL_FORWARDS:
            return (
                f"({self._position_q}='{PositionTypes.LEFT_WING.value}' "
                f"or {self._position_q}='{PositionTypes.RIGHT_WING.value}' "
                f"or {self._position_q}='{PositionTypes.CENTER.value}')"
            )

        return f"{self._position_q}='{self.position.value}'"

    def validate(self) -> Union[bool, None]:
        return True
