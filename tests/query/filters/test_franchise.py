from nhlpy.api.query.filters.franchise import FranchiseQuery


def test_franchise_query():
    franchise_query = FranchiseQuery(franchise_id="1")
    assert franchise_query.to_query() == "franchiseId=1"
