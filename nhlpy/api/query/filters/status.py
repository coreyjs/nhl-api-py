from typing import Union

from nhlpy.api.query.filters import QueryBase

# Not thrilled with this implementation, having 2 bools with the later overridding the first.
# Ill think of a better design pattern for this.


class StatusQuery(QueryBase):
    def __init__(self, is_active: bool = False, is_hall_of_fame: bool = False):
        """
        Player status. is_active=True for current active players, not suppling this
            defaults to active/inactive.  OR you can specify is_hall_of_fame=True, for
            only HOF Players
        :param is_active:
        :param is_hall_of_fame:
        """
        self.is_active: bool = is_active
        self.is_hall_of_fame: bool = is_hall_of_fame
        self._active_q = "active"
        self._hof_q = "isInHallOfFame"

    def to_query(self) -> str:
        if self.is_hall_of_fame:
            return f"{self._hof_q}=1"
        elif self.is_active:
            return f"{self._active_q}=1"
        else:
            return ""

    def validate(self) -> Union[bool, None]:
        return True
