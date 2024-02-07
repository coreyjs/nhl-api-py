import urllib.parse
import json
from typing import List


from nhlpy.http_client import HttpClient


class Stats:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def club_stats_season(self, team_abbr: str) -> dict:
        """
        This seems to return gameTypes for every season the team was in existence.  Maybe its useful?
        :param team_abbr: The 3 letter abbreviation of the team.  BUF, TOR, etc
        :return: dict
        """
        return self.client.get(resource=f"club-stats-season/{team_abbr}").json()

    def player_career_stats(self, player_id: int) -> dict:
        """
        This returns the career stats for a player as well as player information.

        example: https://api-web.nhle.com/v1/player/8481528/landing

        :param player_id: The player_id for the player you want the stats for.
        :return: dict
        """
        return self.client.get(resource=f"player/{player_id}/landing").json()

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
