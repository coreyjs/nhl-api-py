from nhlpy.api.query.filters.home_road import HomeRoadQuery


def test_home_game():
    home_road = HomeRoadQuery(home_road="H")
    assert home_road.to_query() == "homeRoad='H'"


def test_road_game():
    home_road = HomeRoadQuery(home_road="R")
    assert home_road.to_query() == "homeRoad='R'"
