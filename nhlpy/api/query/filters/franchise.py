from typing import Union

from nhlpy.api.query.builder import QueryBase


class FranchiseQuery(QueryBase):
    def __init__(self, franchise_id: str):
        self.franchise_id = franchise_id
        self._franchise_q = "franchiseId"

    def to_query(self) -> str:
        return f"{self._franchise_q}={self.franchise_id}"

    def validate(self) -> Union[bool, None]:
        return True
