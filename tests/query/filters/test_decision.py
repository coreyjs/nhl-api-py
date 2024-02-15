from pytest import raises

from nhlpy.api.query import InvalidQueryValueException
from nhlpy.api.query.filters.decision import DecisionQuery


def test_win_outcome():
    decision = DecisionQuery(decision="W")
    assert decision.to_query() == "decision='W'"


def test_loss_outcome():
    decision = DecisionQuery(decision="L")
    assert decision.to_query() == "decision='L'"


def test_overtime_loss_outcome():
    decision = DecisionQuery(decision="O")
    assert decision.to_query() == "decision='O'"


def test_invalid_data():
    decision = DecisionQuery(decision="A")
    with raises(InvalidQueryValueException):
        assert decision.validate() is False
