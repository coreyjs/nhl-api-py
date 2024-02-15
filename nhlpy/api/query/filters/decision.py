import logging
from typing import Union

from nhlpy.api.query import InvalidQueryValueException
from nhlpy.api.query.filters import QueryBase


logger = logging.getLogger(__name__)


class DecisionQuery(QueryBase):
    def __init__(self, decision: str):
        """
        Decision filter.  W=win, L=loss, O=overtime loss,
        :param decision: W, L, O
        """
        self.decision = decision
        self._decision_q = "decision"

    def __str__(self):
        return f"DecisionQuery: Value={self.decision}"

    def to_query(self) -> str:
        return f"{self._decision_q}='{self.decision}'"

    def validate(self) -> Union[bool, None]:
        if self.decision not in ["W", "L", "O"]:
            raise InvalidQueryValueException("Decision value must be one of [W, L, O]")
