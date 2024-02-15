from typing import Optional, Union

from nhlpy.api.query.filters import QueryBase


class DraftQuery(QueryBase):
    def __init__(self, year: str, draft_round: Optional[str] = None):
        """

        :param year:
        :param draft_round: This seems to default to "1" on the API.  Should
        check not supplying it.
        """
        self.year = year
        self.round = draft_round
        self._year_q = "draftYear"
        self._round_q = "draftRound"

    def to_query(self) -> str:
        query = f"{self._year_q}={self.year}"
        if self.round:
            query += " and "
            query += f"{self._round_q}={self.round}"
        return query

    def validate(self) -> Union[bool, None]:
        return True
