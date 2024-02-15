from nhlpy.api.query.filters.position import PositionQuery, PositionTypes


def test_centers():
    position = PositionQuery(position=PositionTypes.CENTER)
    assert position.to_query() == "positionCode='C'"


def test_left_wings():
    position = PositionQuery(position=PositionTypes.LEFT_WING)
    assert position.to_query() == "positionCode='L'"


def test_right_wings():
    position = PositionQuery(position=PositionTypes.RIGHT_WING)
    assert position.to_query() == "positionCode='R'"


def test_forwards():
    position = PositionQuery(position=PositionTypes.ALL_FORWARDS)
    assert position.to_query() == "(positionCode='L' or positionCode='R' or positionCode='C')"


def test_defense():
    position = PositionQuery(position=PositionTypes.DEFENSE)
    assert position.to_query() == "positionCode='D'"
