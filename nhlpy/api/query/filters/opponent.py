from typing import Union

from nhlpy.api.query.filters import QueryBase


class OpponentQuery(QueryBase):
    def __init__(self, opponent_franchise_id: str):
        """
        Opponent filter.  Takes in the ID of the franchise.
        :param opponent_id: int
        """
        self.opponent_id: str = opponent_franchise_id
        self._opponent_q = "opponentFranchiseId"

    def to_query(self) -> str:
        return f"{self._opponent_q}={self.opponent_id}"

    def validate(self) -> Union[bool, None]:
        return True
