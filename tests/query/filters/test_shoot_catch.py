from nhlpy.api.query.filters.shoot_catch import ShootCatchesQuery


def test_shoot_catch_l():
    shoot_catch = ShootCatchesQuery(shoot_catch="L")
    assert shoot_catch.to_query() == "shootsCatches=L"


def test_shoot_catch_r():
    shoot_catch = ShootCatchesQuery(shoot_catch="R")
    assert shoot_catch.to_query() == "shootsCatches=R"
