from nhlpy.api.query.filters.game_type import GameTypeQuery


def test_game_type_preseason():
    game_type = GameTypeQuery(game_type="1")
    assert game_type.to_query() == "gameTypeId=1"


def test_game_type_regular():
    game_type = GameTypeQuery(game_type="2")
    assert game_type.to_query() == "gameTypeId=2"
