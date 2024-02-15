from nhlpy.api.query.filters.season import SeasonQuery


def test_season_query_range():
    season_query = SeasonQuery(season_start="20202021", season_end="20232024")
    assert season_query.to_query() == "seasonId >= 20202021 and seasonId <= 20232024"


def test_season_query_same_year():
    season_query = SeasonQuery(season_start="20202021", season_end="20202021")
    assert season_query.to_query() == "seasonId >= 20202021 and seasonId <= 20202021"


def test_season_query_wrong_range():
    season_query = SeasonQuery(season_start="20232024", season_end="20202020")
    assert season_query.to_query() == "seasonId >= 20232024 and seasonId <= 20202020"
