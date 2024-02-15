from nhlpy.api.query.filters.status import StatusQuery


def test_active_player():
    status = StatusQuery(is_active=True)
    assert status.to_query() == "active=1"


def test_hall_of_fame_player():
    status = StatusQuery(is_hall_of_fame=True)
    assert status.to_query() == "isInHallOfFame=1"


def test_active_and_hof_should_return_hof():
    status = StatusQuery(is_active=True, is_hall_of_fame=True)
    assert status.to_query() == "isInHallOfFame=1"


def test_inactive_not_hof_returns_empty():
    status = StatusQuery(is_active=False, is_hall_of_fame=False)
    assert status.to_query() == ""
