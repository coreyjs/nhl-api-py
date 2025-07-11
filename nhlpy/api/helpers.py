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
        """Gets all game IDs for a specified season.

        Args:
           season (str): Season to retrieve game IDs for in YYYYYYYY format (e.g., 20232024).
           game_types (List[int]): List of game types to include. Valid types:
               1: Preseason
               2: Regular season
               3: Playoffs
        api_sleep_rate (float): Sleep rate in seconds between API calls to avoid hitting rate limits.

        Returns:
           List of game IDs for the specified season and game types.
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
        """Gets all player base stats.

        Args:
            api_sleep_rate (float): Sleep rate in seconds between API calls to avoid hitting rate limits.

        Returns:
            List of player base stats.
        """
        from nhlpy.api.teams import Teams

        teams_client = Teams(self.client)
        teams = teams_client.teams()

        print("Fetching all player base stats. This may take a while...")
        out_data = []
        for team in teams:
            time.sleep(api_sleep_rate)
            players = teams_client.roster_by_team(team_abbr=team["abbr"], season=season)

            # Tweak and clean some player data
            for p in players["forwards"] + players["defensemen"] + players["goalies"]:
                p["team"] = team["abbr"]
                p["firstName"] = self._clean_name("firstName", p)
                p["lastName"] = self._clean_name("lastName", p)

                out_data.append(p)

        return out_data

    def all_players_summary_statistics(self, season: str, api_sleep_rate: float = 1):
        """Gets all player summary statistics for a specified season."""
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
