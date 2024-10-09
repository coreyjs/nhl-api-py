import urllib.parse
import json
from typing import List

from nhlpy.api.query.builder import QueryContext
from nhlpy.api.query.sorting.sorting_options import SortingOptions
from nhlpy.http_client import HttpClient


class Stats:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def _goalie_stats_sorts(self, report: str) -> List[dict]:
        """
        This is default criteria for sorting on goalie stats.  I hate this method.  Ill fix it soon.
        :param report:
        :return:
        """
        if report == "summary":
            return [
                {"property": "wins", "direction": "DESC"},
                {"property": "gamesPlayed", "direction": "ASC"},
                {"property": "playerId", "direction": "ASC"},
            ]
        elif report == "advanced":
            return [
                {"property": "qualityStart", "direction": "DESC"},
                {"property": "goalsAgainstAverage", "direction": "ASC"},
                {"property": "playerId", "direction": "ASC"},
            ]
        elif report == "bios":
            return [
                {"property": "lastName", "direction": "ASC_CI"},
                {"property": "goalieFullName", "direction": "ASC_CI"},
                {"property": "playerId", "direction": "ASC"},
            ]
        elif report == "daysrest":
            return [
                {"property": "wins", "direction": "DESC"},
                {"property": "savePct", "direction": "DESC"},
                {"property": "playerId", "direction": "ASC"},
            ]
        elif report == "penaltyShots":
            return [
                {"property": "penaltyShotsSaves", "direction": "DESC"},
                {"property": "penaltyShotSavePct", "direction": "DESC"},
                {"property": "playerId", "direction": "ASC"},
            ]
        elif report == "savesByStrength":
            return [
                {"property": "wins", "direction": "DESC"},
                {"property": "savePct", "direction": "DESC"},
                {"property": "playerId", "direction": "ASC"},
            ]
        elif report == "shootout":
            return [
                {"property": "shootoutWins", "direction": "DESC"},
                {"property": "shootoutSavePct", "direction": "DESC"},
                {"property": "playerId", "direction": "ASC"},
            ]
        elif report == "startedVsRelieved":
            return [
                {"property": "gamesStarted", "direction": "DESC"},
                {"property": "gamesStartedSavePct", "direction": "DESC"},
                {"property": "playerId", "direction": "ASC"},
            ]
        else:
            return [{}]

    def club_stats_season(self, team_abbr: str) -> dict:
        """
        This seems to return gameTypes for every season the team was in existence.  Maybe its useful?
        :param team_abbr: The 3 letter abbreviation of the team.  BUF, TOR, etc
        :return: dict
        """
        return self.client.get(resource=f"club-stats-season/{team_abbr}").json()

    def player_career_stats(self, player_id: str) -> dict:
        """
        This returns the career stats for a player as well as player information.

        example: https://api-web.nhle.com/v1/player/8481528/landing

        :param player_id: The player_id for the player you want the stats for.
        :return: dict
        """
        return self.client.get(resource=f"player/{player_id}/landing").json()

    def player_game_log(self, player_id: str, season_id: str, game_type: int) -> List[dict]:
        """
        Returns the game log, for the given player, for the given season and game type.
        :param game_type: 1 is for preseason, 2 is for regular season, 3 is for playoffs.
        :param season_id: Season format of "20222023", "20232024", etc.
        :param player_id:
        :return:
        """
        return self.client.get(resource=f"player/{player_id}/game-log/{season_id}/{game_type}").json()["gameLog"]

    def team_summary(
        self,
        start_season: str,
        end_season: str,
        game_type_id: int = 2,
        is_game: bool = False,
        is_aggregate: bool = False,
        sort_expr: List[dict] = None,
        start: int = 0,
        limit: int = 50,
        fact_cayenne_exp: str = "gamesPlayed>1",
        default_cayenne_exp: str = None,
    ) -> List[dict]:
        """
        Example: c.stats.team_summary(start_season="20202021", end_season="20212022", game_type_id=2)
                 c.stats.team_summary(start_season="20202021", end_season="20212022")
        :param start_season: Season id, in format 20202021, 20212022, etc, that will be the start of the range.  This
            allows for searching over multiple season.  If you just want one season, set start_season and end_season.
        :param end_season: Season id for the end range.
        :param game_type_id: 2 is for regular season, 3 is for playoffs.  I think 1 is for preseason.
        :param is_game: (dev notes: not sure what this is, its part of the api call)
        :param is_aggregate:
        :param sort_expr: A list of key/value pairs of properties and their sort direction.  For Example this defaults
            to [
            {"property":"points","direction":"DESC"},
            {"property":"wins","direction":"DESC"},
            {"property":"teamId","direction":"ASC"}
            ]
        :param start:
        :param limit:
        :param fact_cayenne_exp:  An expression used by apache cayenne.  This defaults to 'gamesPlayed>=1'.
            You can experiment at will, this was taken from the nhl.com website.
        :param default_cayenne_exp: Similar to above, I believe this provides a filter for the data returned.
            This will look something like: "gameTypeId=2 and seasonId<=20232024 and seasonId>=20232024".

            If this value is supplied, it will override a generated one, giving the user ability to experiment.
        :return:
        """
        q_params = {
            "isAggregate": is_aggregate,
            "isGame": is_game,
            "start": start,
            "limit": limit,
            "factCayenneExp": fact_cayenne_exp,
        }

        if not sort_expr:
            sort_expr = [
                {"property": "points", "direction": "DESC"},
                {"property": "wins", "direction": "DESC"},
                {"property": "teamId", "direction": "ASC"},
            ]
        q_params["sort"] = urllib.parse.quote(json.dumps(sort_expr))

        if not default_cayenne_exp:
            default_cayenne_exp = f"gameTypeId={game_type_id} and seasonId<={end_season} and seasonId>={start_season}"
        q_params["cayenneExp"] = default_cayenne_exp

        return self.client.get_by_url("https://api.nhle.com/stats/rest/en/team/summary", query_params=q_params).json()[
            "data"
        ]

    def skater_stats_summary_simple(
        self,
        start_season: str,
        end_season: str,
        franchise_id: str = None,
        game_type_id: int = 2,
        aggregate: bool = False,
        sort_expr: List[dict] = None,
        start: int = 0,
        limit: int = 70,
        fact_cayenne_exp: str = "gamesPlayed>=1",
        default_cayenne_exp: str = None,
    ) -> List[dict]:
        """
        Example: c.stats.skater_stats_summary_simple(start_season="20232024", end_season="20232024")
                 c.stats.skater_stats_summary_simple(franchise_id=10, start_season="20232024", end_season="20232024")
        :param start_season: Season id, in format 20202021, 20212022, etc, that will be the start of the range.
        :param end_season: Season id for the end range.
        :param franchise_id: String, The ID of the franchise.  Not to be confused with team_id found on other endpoints.
            This seems to be specific to the /stats apis.
        :param game_type_id: 2 is for regular season, 3 is for playoffs.  I think 1 is for preseason.
        :param aggregate: If doing multiple years, you can choose to aggreate the date per player, or have separate
            entries for each one.
        :param sort_expr: Default sorting expresions.  Provided as an array of key/value pairs.  For example:
            [
                {"property": "points", "direction": "DESC"},
                {"property": "gamesPlayed", "direction": "ASC"},
                {"property": "playerId", "direction": "ASC"}
            ]
        :param start: Possibly start of the retrieved data, based on limit.
        :param limit: How many to return.
        :param fact_cayenne_exp: An anchor expression almost, default criteria.  Only players with more than 1 game
            played.  I default this to gamesPlayed>=1, which is what the nhl.com site uses.  But you can play with it.
        :param default_cayenne_exp:
        :return:
        """
        q_params = {
            "isAggregate": aggregate,
            "isGame": False,
            "start": start,
            "limit": limit,
            "factCayenneExp": fact_cayenne_exp,
        }

        if not sort_expr:
            sort_expr = [
                {"property": "points", "direction": "DESC"},
                {"property": "gamesPlayed", "direction": "ASC"},
                {"property": "playerId", "direction": "ASC"},
            ]
        q_params["sort"] = urllib.parse.quote(json.dumps(sort_expr))

        if not default_cayenne_exp:
            default_cayenne_exp = f"gameTypeId={game_type_id} and seasonId<={end_season} and seasonId>={start_season}"
            if franchise_id:
                default_cayenne_exp = f"franchiseId={franchise_id} and {default_cayenne_exp}"
        q_params["cayenneExp"] = default_cayenne_exp

        return self.client.get_by_url("https://api.nhle.com/stats/rest/en/skater/summary", query_params=q_params).json()[
            "data"
        ]

    def skater_stats_with_query_context(
        self,
        query_context: QueryContext,
        report_type: str,
        sort_expr: List[dict] = None,
        aggregate: bool = False,
        start: int = 0,
        limit: int = 70,
    ) -> dict:
        """

        example:
            sort_expr = [
                {"property": "points", "direction": "DESC"},
                {"property": "gamesPlayed", "direction": "ASC"},
                {"property": "playerId", "direction": "ASC"}
                ]
            cayenne_exp = "gameTypeId=2 and seasonId<=20232024 and seasonId>=20232024"
            client.stats.skater_stats_summary_by_expression(cayenne_exp=expr, sort_expr=sort_expr)

        :param report_type: summary, bios,  faceoffpercentages, faceoffwins, goalsForAgainst, realtime, penalties,
            penaltykill, penaltyShots, powerplay, puckPossessions, summaryshooting, percentages, scoringRates,
            scoringpergame, shootout, shottype, timeonice
        :param query_context:
        :param aggregate: bool - If doing multiple years, you can choose to aggregate the date per player,
            or have separate entries for each one.
        :param sort_expr: A list of key/value pairs for sort criteria.  As used in skater_stats_summary(), this is
            in the format:
            [
                {"property": "points", "direction": "DESC"},
                {"property": "gamesPlayed", "direction": "ASC"},
                {"property": "playerId", "direction": "ASC"}
            ]
        :param start:
        :param limit:
        :return:
        """
        q_params = {
            "isAggregate": aggregate,
            "isGame": False,
            "start": start,
            "limit": limit,
            "factCayenneExp": query_context.fact_query,
        }

        if not sort_expr:
            sort_expr = SortingOptions.get_default_sorting_for_report(report_type)

        q_params["sort"] = json.dumps(sort_expr)
        q_params["cayenneExp"] = query_context.query_str
        return self.client.get_by_url(
            f"https://api.nhle.com/stats/rest/en/skater/{report_type}", query_params=q_params
        ).json()

    def goalie_stats_summary_simple(
        self,
        start_season: str,
        end_season: str = None,
        stats_type: str = "summary",
        game_type_id: int = 2,
        franchise_id: str = None,
        aggregate: bool = False,
        sort_expr: List[dict] = None,
        start: int = 0,
        limit: int = 70,
        fact_cayenne_exp: str = None,
        default_cayenne_exp: str = None,
    ) -> List[dict]:
        """
        Simple endpoint to retrieve goalie stats.  Types of status are derived via the stats_type parameter.
        :param start_season: Season id, in string format 20202021, 20212022, etc, that will be the start of the range.
        :param end_season: Optional, Season id for the end range.  If not provided, it will default to start_season.
        :param stats_type: summary, advanced, bios, daysrest, penaltyShots, savesByStrength, shootout, startedVsRelieved
        :param game_type_id: 2 is for regular season, 3 is for playoffs.  I think 1 is for preseason.
        :param franchise_id: Optional, the franchise id to filter by.
        :param aggregate: bool - If doing multiple years, you can choose to aggreate the date per player,
        :param sort_expr: A list of key/value pairs for sort criteria.  This is defaulting to what is used on the EDGE
            stats site, but I think it works with any properties returned in the payload.
        :param start:
        :param limit:
        :param fact_cayenne_exp:
        :param default_cayenne_exp:
        :return:
        """
        q_params = {
            "isAggregate": aggregate,
            "isGame": False,
            "start": start,
            "limit": limit,
            "factCayenneExp": fact_cayenne_exp,
        }

        if end_season is None:
            end_season = start_season

        if not sort_expr:
            sort_expr = self._goalie_stats_sorts(stats_type)
        q_params["sort"] = urllib.parse.quote(json.dumps(sort_expr))

        if not default_cayenne_exp:
            default_cayenne_exp = f"gameTypeId={game_type_id} and seasonId<={end_season} and seasonId>={start_season}"

        if franchise_id:
            default_cayenne_exp = f"franchiseId={franchise_id} and {default_cayenne_exp}"

        q_params["cayenneExp"] = default_cayenne_exp

        return self.client.get_by_url(
            f"https://api.nhle.com/stats/rest/en/goalie/{stats_type}", query_params=q_params
        ).json()["data"]
