from typing import Union

from nhlpy.api.query.filters import QueryBase


class ExperienceQuery(QueryBase):
    def __init__(self, is_rookie: bool):
        """
        Experience filter.  R=rookie, S=sophomore, V=veteran
        :param experience: R, S, V
        """
        self.is_rookie: bool = is_rookie
        self._experience_q = "isRookie"

    def to_query(self) -> str:
        val = "1" if self.is_rookie else "0"
        return f"{self._experience_q}='{val}'"

    def validate(self) -> Union[bool, None]:
        return True
