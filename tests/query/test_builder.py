from nhlpy.api.query.builder import QueryBuilder, QueryContext
from nhlpy.api.query.filters.decision import DecisionQuery
from nhlpy.api.query.filters.draft import DraftQuery
from nhlpy.api.query.filters.game_type import GameTypeQuery
from nhlpy.api.query.filters.position import PositionQuery, PositionTypes
from nhlpy.api.query.filters.season import SeasonQuery


def test_query_builder_empty_filters():
    qb = QueryBuilder()
    context: QueryContext = qb.build(filters=[])

    assert context.query_str == ""


def test_query_builder_invalid_filter():
    qb = QueryBuilder()
    context: QueryContext = qb.build(filters=["invalid"])

    assert context.query_str == ""


def test_qb_draft_year():
    qb = QueryBuilder()
    filters = [DraftQuery(year="2020", draft_round="2")]
    context: QueryContext = qb.build(filters=filters)

    assert context.query_str == "draftYear=2020 and draftRound=2"
    assert len(context.filters) == 1


def test_qb_multi_filter():
    qb = QueryBuilder()
    filters = [
        GameTypeQuery(game_type="2"),
        DraftQuery(year="2020", draft_round="2"),
        SeasonQuery(season_start="20202021", season_end="20232024"),
    ]
    context: QueryContext = qb.build(filters=filters)

    assert (
        context.query_str
        == "gameTypeId=2 and draftYear=2020 and draftRound=2 and seasonId >= 20202021 and seasonId <= 20232024"
    )


def test_position_draft_query():
    qb = QueryBuilder()
    filters = [
        GameTypeQuery(game_type="2"),
        DraftQuery(year="2020", draft_round="1"),
        PositionQuery(position=PositionTypes.CENTER),
    ]
    context: QueryContext = qb.build(filters=filters)

    assert context.query_str == "gameTypeId=2 and draftYear=2020 and draftRound=1 and positionCode='C'"
    assert len(context.filters) == 3


def test_all_forwards_playoffs_season_query():
    qb = QueryBuilder()
    filters = [
        GameTypeQuery(game_type="3"),
        SeasonQuery(season_start="20222023", season_end="20222023"),
        PositionQuery(position=PositionTypes.ALL_FORWARDS),
    ]
    context: QueryContext = qb.build(filters=filters)

    assert (
        context.query_str
        == "gameTypeId=3 and seasonId >= 20222023 and seasonId <= 20222023 and (positionCode='L' or positionCode='R' "
        "or positionCode='C')"
    )
    assert len(context.filters) == 3


def test_query_with_invalid_filter_mixed_in():
    qb = QueryBuilder(debug=True)
    filters = [
        GameTypeQuery(game_type="3"),
        SeasonQuery(season_start="20222023", season_end="20222023"),
        PositionQuery(position=PositionTypes.ALL_FORWARDS),
        DecisionQuery(decision="Win"),
    ]
    context: QueryContext = qb.build(filters=filters)

    assert context.is_valid() is False

    assert (
        context.query_str
        == "gameTypeId=3 and seasonId >= 20222023 and seasonId <= 20222023 and (positionCode='L' or positionCode='R' "
        "or positionCode='C')"
    )
