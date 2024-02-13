from nhlpy.api.query.filters.draft import DraftQuery


def test_draft_year_with_round():
    draft = DraftQuery(year="2020", draft_round="2")
    assert draft.to_query() == "draftYear=2020 and draftRound=2"


def test_draft_year_without_round():
    draft = DraftQuery(year="2020")
    assert draft.to_query() == "draftYear=2020"
