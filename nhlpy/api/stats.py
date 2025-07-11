import json
from typing import List

from nhlpy.api.query.builder import QueryContext
from nhlpy.api.query.filters import _goalie_stats_sorts
from nhlpy.api.query.sorting.sorting_options import SortingOptions
from nhlpy.http_client import HttpClient, Endpoint


class Stats:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def gametypes_per_season_directory_by_team(self, team_abbr: str) -> dict:
        """Gets all game types played by a team throughout their history.

        A dictionary containing game types for each season the team has existed in the league.

        Args:
            team_abbr (str): The 3 letter abbreviation of the team (e.g., BUF, TOR)

        Returns:
            dict: A mapping of seasons to game types played by the team

        Example:
            https://api-web.nhle.com/v1/club-stats-season/TOR

            [
                {'season': 20242025, 'gameTypes': [2]},
                {'season': 20232024, 'gameTypes': [2, 3]},
                {'season': 20222023, 'gameTypes': [2, 3]},
                {'season': 20212022, 'gameTypes': [2, 3]},
             ...
             ]

        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"club-stats-season/{team_abbr}").json()

    def player_career_stats(self, player_id: str) -> dict:
        """Gets a player's career statistics and biographical information.

        Retrieves comprehensive player data including career stats and personal details from the NHL API.
        API endpoint example: https://api-web.nhle.com/v1/player/8481528/landing

        Args:
            player_id (str): The unique identifier for the NHL player

        Returns:
            dict: A dictionary containing the player's career statistics and personal information

        Example:
            Full Example: https://github.com/coreyjs/nhl-api-py/wiki/Player-Career-Stats-%E2%80%90-Example-Payload

            {'playerId': 8478402,
             'isActive': True,
             'currentTeamId': 22,
             'currentTeamAbbrev': 'EDM',
             'fullTeamName': {'default': 'Edmonton Oilers', 'fr': "Oilers d'Edmonton"},
             'teamCommonName': {'default': 'Oilers'},
             'teamPlaceNameWithPreposition': {'default': 'Edmonton', 'fr': "d'Edmonton"},
             'firstName': {'default': 'Connor'},
             'lastName': {'default': 'McDavid'},
             'badges': [{'logoUrl': {'default': 'https://assets.nhle.com/badges/4n_face-off.svg',
                'fr': 'https://assets.nhle.com/badges/4n_face-off_fr.svg'},
               'title': {'default': '4 Nations Face-Off',
                'fr': 'Confrontation Des 4 Nations'}}],
             'teamLogo': 'https://assets.nhle.com/logos/nhl/svg/EDM_light.svg',
             'sweaterNumber': 97,
             'position': 'C',
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"player/{player_id}/landing").json()

    def player_game_log(self, player_id: str, season_id: str, game_type: int) -> List[dict]:
        """Gets a player's game log for a specific season and game type.

        Retrieves detailed game-by-game statistics for a player during a specified season and game type.

        Args:
            game_type (int): The type of games to retrieve:
                1: Preseason
                2: Regular season
                3: Playoffs
            season_id (str): The season identifier in YYYYYYYY format (e.g., "20222023", "20232024")
            player_id (str): The unique identifier for the NHL player

        Returns:
            dict: A dictionary containing the player's game-by-game statistics for the specified parameters

        Example:
            Full example here https://github.com/coreyjs/nhl-api-py/wiki/Stats.Player-Game-Log-%E2%80%90-Example-Response
            [
            {'gameId': 2024020641,
              'teamAbbrev': 'EDM',
              'homeRoadFlag': 'R',
              'gameDate': '2025-01-07',
              'goals': 1,
              'assists': 0,
              'commonName': {'default': 'Oilers'},
              'opponentCommonName': {'default': 'Bruins'},
              'points': 1,
              'plusMinus': 0,
              'powerPlayGoals': 1,
              'powerPlayPoints': 1,
              'gameWinningGoals': 0,
              'otGoals': 0,
              'shots': 5,
              'shifts': 18,
              'shorthandedGoals': 0,
              'shorthandedPoints': 0,
              'opponentAbbrev': 'BOS',
              'pim': 0,
              'toi': '18:04'},
              ...
              ]
        """
        data = self.client.get(
            endpoint=Endpoint.API_WEB_V1, resource=f"player/{player_id}/game-log/{season_id}/{game_type}"
        ).json()
        return data.get("gameLog", [])

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
        """Retrieves team summary statistics across one or more seasons.

        Gets aggregated team statistics for a specified range of seasons with optional filtering and sorting.

        Args:
            start_season (str): Beginning of season range in YYYYYYYY format (e.g., "20202021").
                For single season queries, set equal to end_season.
            end_season (str): End of season range in YYYYYYYY format (e.g., "20212022")
            game_type_id (int, optional): Type of games to include:
                2: Regular season (default)
                3: Playoffs
                1: Preseason
            is_game (bool, optional): Defaults False. (dev notes: not sure what this is, its part of the api call)
            is_aggregate (bool, optional): Defaults False. Whether to aggregate the statistics
            sort_expr (List[dict], optional): List of sorting criteria. Defaults to:
                [
                    {"property": "points", "direction": "DESC"},
                    {"property": "wins", "direction": "DESC"},
                    {"property": "teamId", "direction": "ASC"}
                ]
            start (int, optional): Starting index for pagination. Defaults to 0
            limit (int, optional): Maximum number of results to return. Defaults to 50
            fact_cayenne_exp (str, optional): Apache Cayenne filter expression.
                Defaults to 'gamesPlayed>=1'
            default_cayenne_exp (str, optional): Additional Apache Cayenne filter.
                Example: "gameTypeId=2 and seasonId<=20232024 and seasonId>=20232024"
                If provided, overrides the automatically generated expression.

        Returns:
            List[dict]: List of dictionaries containing team summary statistics

        Examples:
            Full Response Example: https://github.com/coreyjs/nhl-api-py/wiki/Stats.Team-Summary-%E2%80%90-Example-Response
            c.stats.team_summary(start_season="20202021", end_season="20212022", game_type_id=2)
            c.stats.team_summary(start_season="20202021", end_season="20212022")

            [{'faceoffWinPct': 0.48235,
              'gamesPlayed': 82,
              'goalsAgainst': 242,
              'goalsAgainstPerGame': 2.95121,
              'goalsFor': 337,
              'goalsForPerGame': 4.10975,
              'losses': 18,
              'otLosses': 6,
              'penaltyKillNetPct': 0.841698,
              'penaltyKillPct': 0.795367,
              'pointPct': 0.7439,
              'points': 122,
              'powerPlayNetPct': 0.21374,
              'powerPlayPct': 0.244274,
              'regulationAndOtWins': 55,
              'seasonId': 20212022,
              'shotsAgainstPerGame': 30.67073,
              'shotsForPerGame': 37.34146,
              'teamFullName': 'Florida Panthers',
              'teamId': 13,
              'ties': None,
              'wins': 58,
              'winsInRegulation': 42,
              'winsInShootout': 3},
              ... ]
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
        q_params["sort"] = json.dumps(sort_expr)

        if not default_cayenne_exp:
            default_cayenne_exp = f"gameTypeId={game_type_id} and seasonId<={end_season} and seasonId>={start_season}"
        q_params["cayenneExp"] = default_cayenne_exp

        return self.client.get(endpoint=Endpoint.API_STATS, resource="en/team/summary", query_params=q_params).json()[
            "data"
        ]

    def skater_stats_summary(
        self,
        start_season: str,
        end_season: str,
        franchise_id: str = None,
        game_type_id: int = 2,
        aggregate: bool = False,
        sort_expr: List[dict] = None,
        start: int = 0,
        limit: int = 25,
        fact_cayenne_exp: str = "gamesPlayed>=1",
        default_cayenne_exp: str = None,
    ) -> List[dict]:
        """Gets simplified skater statistics summary for specified seasons and franchises.

        Retrieves aggregated or season-by-season skating statistics with optional filtering and sorting.


        Args:
            start_season (str): Beginning of season range in YYYYYYYY format (e.g., "20202021")
            end_season (str): End of season range in YYYYYYYY format
            franchise_id (str, optional): Franchise identifier specific to /stats APIs.
                Note: Different from team_id used in other endpoints
            game_type_id (int, optional): Type of games to include:
                2: Regular season (Default)
                3: Playoffs
                1: Preseason
            aggregate (bool, optional): When True, combines multiple seasons' data per player.
                When False, returns separate entries per season. Defaults to False.
            sort_expr (List[dict], optional): List of sorting criteria. Defaults to:
                [
                    {"property": "points", "direction": "DESC"},
                    {"property": "gamesPlayed", "direction": "ASC"},
                    {"property": "playerId", "direction": "ASC"}
                ]
            start (int, optional): Starting index for pagination
            limit (int, optional): Maximum number of results to return. Defaults to 25.
            fact_cayenne_exp (str, optional): Base filter criteria. Defaults to 'gamesPlayed>=1'
                Can be modified for custom filtering
            default_cayenne_exp (str, optional): Additional filter expression

        Returns:
            List[dict]: List of dictionaries containing skater statistics

        Examples:
            Full Response Example: https://github.com/coreyjs/nhl-api-py/wiki/Stats.Skater-Stats-Summary-Simple
            c.stats.skater_stats_summary_simple(start_season="20232024", end_season="20232024")
            c.stats.skater_stats_summary_simple(franchise_id=10, start_season="20232024", end_season="20232024")

            [{'assists': 71,
              'evGoals': 38,
              'evPoints': 75,
              'faceoffWinPct': 0.1,
              'gameWinningGoals': 5,
              'gamesPlayed': 82,
              'goals': 49,
              'lastName': 'Panarin',
              'otGoals': 1,
              'penaltyMinutes': 24,
              'playerId': 8478550,
              'plusMinus': 18,
              'points': 120,
              'pointsPerGame': 1.46341,
              'positionCode': 'L',
              'ppGoals': 11,
              'ppPoints': 44,
              'seasonId': 20232024,
              'shGoals': 0,
              'shPoints': 1,
              'shootingPct': 0.16171,
              'shootsCatches': 'R',
              'shots': 303,
              'skaterFullName': 'Artemi Panarin',
              'teamAbbrevs': 'NYR',
              'timeOnIcePerGame': 1207.1341},
              ... ]
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
        q_params["sort"] = json.dumps(sort_expr)

        if not default_cayenne_exp:
            default_cayenne_exp = f"gameTypeId={game_type_id} and seasonId<={end_season} and seasonId>={start_season}"
            if franchise_id:
                default_cayenne_exp = f"franchiseId={franchise_id} and {default_cayenne_exp}"
        q_params["cayenneExp"] = default_cayenne_exp

        return self.client.get(endpoint=Endpoint.API_STATS, resource="en/skater/summary", query_params=q_params).json()[
            "data"
        ]

    def skater_stats_with_query_context(
        self,
        query_context: QueryContext,
        report_type: str,
        sort_expr: List[dict] = None,
        aggregate: bool = False,
        start: int = 0,
        limit: int = 25,
    ) -> dict:
        """Retrieves skater statistics using a query context and specified report type.

        Gets detailed skater statistics with customizable filtering, sorting, and aggregation options.

        Args:
            query_context (QueryContext): Context object containing query parameters
            report_type (str): Type of statistical report to retrieve:
                'summary', 'bios', 'faceoffpercentages', 'faceoffwins',
                'goalsForAgainst', 'realtime', 'penalties', 'penaltykill',
                'penaltyShots', 'powerplay', 'puckPossessions',
                'summaryshooting', 'percentages', 'scoringRates',
                'scoringpergame', 'shootout', 'shottype', 'timeonice'
            sort_expr (List[dict], optional): List of sorting criteria. Defaults to None.
                Example format:
                [
                    {"property": "points", "direction": "DESC"},
                    {"property": "gamesPlayed", "direction": "ASC"},
                    {"property": "playerId", "direction": "ASC"}
                ]
            aggregate (bool, optional): When True, combines multiple seasons' data per player.
                When False, returns separate entries per season. Defaults to False.
            start (int, optional): Starting index for pagination. Defaults to 0.
            limit (int, optional): Maximum number of results to return. Defaults to 25.

        Returns:
            dict: Dictionary containing skater statistics based on the specified report type

        Example:
            Full example here: https://github.com/coreyjs/nhl-api-py/wiki/Stats.Skater-Stats-with-Query-Context

            filters = [
                GameTypeQuery(game_type="2"),
                DraftQuery(year="2020", draft_round="2"),
                SeasonQuery(season_start="20202021", season_end="20232024"),
                PositionQuery(position=PositionTypes.ALL_FORWARDS)
            ]

            query_builder = QueryBuilder()
            query_context: QueryContext = query_builder.build(filters=filters)

            data = client.stats.skater_stats_with_query_context(
                report_type='summary',
                query_context=query_context,
                aggregate=True
            )

            Response:
            {'data': [{'assists': 42,
           'evGoals': 35,
           'evPoints': 70,
           'faceoffWinPct': 0.33333,
           'gameWinningGoals': 6,
           'gamesPlayed': 161,
           'goals': 40,
           'lastName': 'Peterka',
           'otGoals': 0,
           'penaltyMinutes': 54,
           'playerId': 8482175,
           'plusMinus': -5,
           'points': 82,
           'pointsPerGame': 0.50931,
           'positionCode': 'R',
           'ppGoals': 5,
           'ppPoints': 12,
           'shGoals': 0,
           'shPoints': 0,
           'shootingPct': 0.11299,
           'shootsCatches': 'L',
           'shots': 354,
           'skaterFullName': 'JJ Peterka',
           'timeOnIcePerGame': 904.5714},
           ...]
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
        return self.client.get(
            endpoint=Endpoint.API_STATS, resource=f"en/skater/{report_type}", query_params=q_params
        ).json()

    def goalie_stats_summary(
        self,
        start_season: str,
        end_season: str = None,
        stats_type: str = "summary",
        game_type_id: int = 2,
        franchise_id: str = None,
        aggregate: bool = False,
        sort_expr: List[dict] = None,
        start: int = 0,
        limit: int = 25,
        fact_cayenne_exp: str = None,
        default_cayenne_exp: str = None,
    ) -> List[dict]:
        """Retrieves goalie statistics with various filtering and aggregation options.

        A simple endpoint that returns different types of goalie statistics based on the specified stats_type parameter.

        Args:
            start_season (str): Beginning of season range in YYYYYYYY format (e.g., "20202021")
            end_season (str, optional): End of season range in YYYYYYYY format.
                Defaults to start_season if not provided.
            stats_type (str): Type of statistics to retrieve:
                'summary', 'advanced', 'bios', 'daysrest', 'penaltyShots',
                'savesByStrength', 'shootout', 'startedVsRelieved'
            game_type_id (int, optional): Type of games to include:
                2: Regular season
                3: Playoffs
                1: Preseason (tentative)
            franchise_id (str, optional): Franchise identifier to filter results
            aggregate (bool, optional): When True, combines multiple seasons' data per goalie.
                When False, returns separate entries per season. Defaults to False.
            sort_expr (List[dict], optional): List of sorting criteria. Uses EDGE stats site defaults.
                Can be customized using any properties from the response payload.
            start (int, optional): Starting index for pagination
            limit (int, optional): Defaults to 25. Maximum number of results to return
            fact_cayenne_exp (str, optional): Base filter criteria
            default_cayenne_exp (str, optional): Additional filter expression

        Returns:
            dict: Dictionary containing goalie statistics based on the specified parameters

        Example:
            client.stats.goalie_stats_summary_simple(start_season="20242025", stats_type="summary")

            [{'assists': 0,
              'gamesPlayed': 33,
              'gamesStarted': 33,
              'goalieFullName': 'Connor Hellebuyck',
              'goals': 0,
              'goalsAgainst': 69,
              'goalsAgainstAverage': 2.08485,
              'lastName': 'Hellebuyck',
              'losses': 6,
              'otLosses': 2,
              'penaltyMinutes': 0,
              'playerId': 8476945,
              'points': 0,
              'savePct': 0.92612,
              'saves': 865,
              'seasonId': 20242025,
              'shootsCatches': 'L',
              'shotsAgainst': 934,
              'shutouts': 5,
              'teamAbbrevs': 'WPG',
              'ties': None,
              'timeOnIce': 119145,
              'wins': 25},
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
            sort_expr = _goalie_stats_sorts(report=stats_type)

        q_params["sort"] = json.dumps(sort_expr)

        if not default_cayenne_exp:
            default_cayenne_exp = f"gameTypeId={game_type_id} and seasonId<={end_season} and seasonId>={start_season}"

        if franchise_id:
            default_cayenne_exp = f"franchiseId={franchise_id} and {default_cayenne_exp}"

        q_params["cayenneExp"] = default_cayenne_exp

        response = self.client.get(
            endpoint=Endpoint.API_STATS, resource=f"en/goalie/{stats_type}", query_params=q_params
        ).json()
        return response.get("data", [])
