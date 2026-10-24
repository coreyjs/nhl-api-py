import logging
import time
from typing import List, Any

from nhlpy.api.query.builder import QueryBuilder
from nhlpy.api.query.filters.franchise import FranchiseQuery
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.stats import Stats
from nhlpy.api.teams import Teams
from nhlpy.http_client import HttpClient


class Helpers:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def _clean_name(self, ntype, name):
        """
        Clean the name of the player or team
        """
        return name[ntype]["default"]

    def game_ids_by_season(self, season: str, game_types: List[int] = None, api_sleep_rate: float = 1) -> List[str]:
        """Gets all game IDs for a specified season by querying every team's schedule.

        Iterates over all 32 NHL teams and collects game IDs from each team's
        season schedule.  Expect roughly 2,600 IDs for a full regular season
        and approximately 32 API calls (one per team).

        Args:
            season (str): Season in YYYYYYYY format (e.g., "20232024").
            game_types (List[int], optional): Game types to include. Valid values:

                - ``1`` -- Preseason
                - ``2`` -- Regular season
                - ``3`` -- Playoffs

                Defaults to ``None`` (all game types).
            api_sleep_rate (float): Seconds to sleep between API calls to
                avoid rate limiting. Defaults to ``1``.

        Returns:
            List[str]: Game IDs matching the requested season and game types.

        Note:
            This method makes one API call per team (~32 calls) and respects
            ``api_sleep_rate`` between each call. Total runtime depends on the
            sleep rate chosen.

            Teams come from ``teams.teams()``, which returns the current
            teams. For historical seasons this iterates today's teams, so
            relocated or defunct teams are missed. For a season-accurate team
            list, use ``stats.team_summary()`` for the season's team IDs and
            ``teams.all_time_teams()`` for their abbreviations.
        """
        from nhlpy.api.teams import Teams
        from nhlpy.api.schedule import Schedule

        teams = Teams(self.client).teams()

        game_ids = []
        schedule_api = Schedule(self.client)
        for team in teams:
            team_abbr = team.get("abbr", "")
            if not team_abbr:
                continue

            time.sleep(api_sleep_rate)
            schedule = schedule_api.team_season_schedule(team_abbr, season)
            games = schedule.get("games", [])

            for game in games:
                game_type = game.get("gameType")
                game_id = game.get("id")

                if game_id and (not game_types or game_type in game_types):
                    game_ids.append(game_id)

        return game_ids

    def all_players(self, season: str, api_sleep_rate: float = 0.5) -> List[dict[str, Any]]:
        """Gets every rostered player across all 32 NHL teams for a given season.

        Iterates over every team roster and returns a flat list of player
        dicts with cleaned name fields and an added ``team`` key.  Makes
        approximately 32 API calls (one per team).

        Args:
            season (str): Season in YYYYYYYY format (e.g., "20232024").
            api_sleep_rate (float): Seconds to sleep between API calls to
                avoid rate limiting. Defaults to ``0.5``.

        Returns:
            List[dict[str, Any]]: List of player dicts. Key fields include:

                - ``id`` (int): Player ID.
                - ``firstName`` (str): Cleaned first name (``default`` value).
                - ``lastName`` (str): Cleaned last name (``default`` value).
                - ``sweaterNumber`` (int): Jersey number.
                - ``positionCode`` (str): Position code (e.g., "C", "D", "G").
                - ``team`` (str): Team abbreviation added by this method.

        Note:
            This method makes one API call per team (~32 calls) and respects
            ``api_sleep_rate`` between each call.

            Teams come from ``teams.teams()``, which returns the current
            teams. For historical seasons this iterates today's teams, so
            relocated or defunct teams are missed. For a season-accurate team
            list, use ``stats.team_summary()`` for the season's team IDs and
            ``teams.all_time_teams()`` for their abbreviations.
        """
        from nhlpy.api.teams import Teams

        teams_client = Teams(self.client)
        teams = teams_client.teams()

        print("Fetching all player base stats. This may take a while...")
        out_data = []
        for team in teams:
            time.sleep(api_sleep_rate)
            players = teams_client.team_roster(team_abbr=team["abbr"], season=season)

            # Tweak and clean some player data
            for p in players["forwards"] + players["defensemen"] + players["goalies"]:
                p["team"] = team["abbr"]
                p["firstName"] = self._clean_name("firstName", p)
                p["lastName"] = self._clean_name("lastName", p)

                out_data.append(p)

        return out_data

    def all_players_summary_statistics(self, season: str, api_sleep_rate: float = 1):
        """Gets summary statistics for every skater in a given season.

        Combines roster data from ``all_players()`` with per-team summary
        stats fetched through the query builder, then merges the two datasets
        on player ID.  Makes multiple paginated API calls (one roster call
        per team plus one stats call per team franchise).

        Args:
            season (str): Season in YYYYYYYY format (e.g., "20232024").
            api_sleep_rate (float): Seconds to sleep between API calls to
                avoid rate limiting. Defaults to ``1``.

        Returns:
            list[dict]: Merged player and summary-stats dicts.  Each entry
            contains the roster fields from ``all_players()`` plus stats
            fields such as ``goals``, ``assists``, ``points``,
            ``gamesPlayed``, and other summary report columns.

        Warning:
            This method is slow and makes a large number of API calls.
            Increase ``api_sleep_rate`` if you encounter rate limiting.

        Note:
            Teams and their franchise IDs come from ``teams.teams()``, which
            returns the current teams, so historical seasons only cover
            franchises that are active today. See ``game_ids_by_season()``.
        """
        logging.warning(
            "This method will take a while to run.  In the event of rate limiting, you may need to increase the api_sleep_rate."
        )
        players = self.all_players(season, api_sleep_rate=api_sleep_rate)
        teams = Teams(self.client).teams()
        stats_client = Stats(self.client)

        season_query = SeasonQuery(season_start=season, season_end=season)
        query_builder = QueryBuilder()

        out_data = []
        for team in teams:
            time.sleep(api_sleep_rate)
            fran_query = FranchiseQuery(franchise_id=team["franchise_id"])
            context = query_builder.build(filters=[fran_query, season_query])

            data = stats_client.skater_stats_with_query_context(
                report_type="summary", query_context=context, aggregate=True
            )
            out_data.extend(data.get("data", []))

        # Create a dictionary for fast player lookup by id
        player_dict = {player["id"]: player for player in players}

        # Merge player data with stats data
        merged_data = []
        for stat_entry in out_data:
            player_id = stat_entry.get("playerId")
            if player_id and player_id in player_dict:
                # Merge player data with stats data
                merged_entry = {**player_dict[player_id], **stat_entry}
                merged_data.append(merged_entry)
            else:
                # Include stats entry even if no matching player found
                merged_data.append(stat_entry)

        return merged_data
