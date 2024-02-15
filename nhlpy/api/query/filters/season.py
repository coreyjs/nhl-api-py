from typing import Union

from nhlpy.api.query.filters import QueryBase


class SeasonQuery(QueryBase):
    def __init__(self, season_start: str, season_end: str):
        self.season_start = season_start
        self.season_end = season_end
        self._season_start_q = "seasonId"
        self._season_start_q_exp = ">="
        self._season_end_q = "seasonId"
        self._season_end_q_exp = "<="

    def to_query(self) -> str:
        query = f"{self._season_start_q} {self._season_start_q_exp} {self.season_start}"
        query += " and "
        query += f"{self._season_end_q} {self._season_end_q_exp} {self.season_end}"
        return query

    def validate(self) -> Union[bool, None]:
        return True
