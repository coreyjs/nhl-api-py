from nhlpy.api.query.filters.nationality import NationalityQuery


def test_nation_usa():
    nation = NationalityQuery(nation_code="USA")
    assert nation.to_query() == "nationalityCode='USA'"
