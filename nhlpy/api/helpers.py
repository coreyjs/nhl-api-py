import logging
import re
import time
from typing import Any, Dict, List, Optional, Tuple

from nhlpy.api.game_center import GameCenter
from nhlpy.api.query.builder import QueryBuilder
from nhlpy.api.query.filters.franchise import FranchiseQuery
from nhlpy.api.query.filters.season import SeasonQuery
from nhlpy.api.stats import Stats
from nhlpy.api.teams import Teams
from nhlpy.http_client import HttpClient

SHIFT_TYPE_CODE = 517  # shift-chart rows that are shifts (505 rows are goals)
POSITION_ORDER = {"C": 0, "L": 1, "R": 2, "D": 3, "G": 4}


def _clock_to_seconds(clock: Optional[str]) -> Optional[int]:
    """Converts a "MM:SS" game clock to seconds. Returns None if the value can't be parsed."""
    try:
        minutes, seconds = clock.split(":")
        return int(minutes) * 60 + int(seconds)
    except (AttributeError, ValueError):
        return None


def _default(name: Any) -> Optional[str]:
    """Returns the English value of a localized name ({"default": ...}), or the value itself if it's a plain string."""
    return name.get("default") if isinstance(name, dict) else name


def _team(team: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": team.get("id"),
        "abbr": team.get("abbrev"),
        "logo": team.get("logo"),
        "dark_logo": team.get("darkLogo"),
    }


def _build_game_goals(pbp: Dict[str, Any], shifts: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Reshapes a play-by-play feed, plus optional shift-chart rows, into the ``game_goals()`` result."""
    home, away = pbp.get("homeTeam") or {}, pbp.get("awayTeam") or {}
    abbr_by_team_id = {home.get("id"): home.get("abbrev"), away.get("id"): away.get("abbrev")}
    roster = {spot.get("playerId"): spot for spot in pbp.get("rosterSpots") or []}

    def player(player_id: Optional[int], shift: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        if player_id is None:
            return None
        spot = roster.get(player_id)
        if spot is None:
            # Not in the play-by-play roster: keep the ID, and use the shift row's name and team if there is one.
            shift = shift or {}
            spot = {"firstName": shift.get("firstName"), "lastName": shift.get("lastName")}
            team_abbr = shift.get("teamAbbrev")
        else:
            team_abbr = abbr_by_team_id.get(spot.get("teamId"))
        return {
            "player_id": player_id,
            "first_name": _default(spot.get("firstName")),
            "last_name": _default(spot.get("lastName")),
            "sweater_number": spot.get("sweaterNumber"),
            "position": spot.get("positionCode"),
            "team_abbr": team_abbr,
            "headshot": spot.get("headshot"),
        }

    shifts_by_period: Dict[int, List[Tuple[int, int, Dict[str, Any]]]] = {}
    for row in shifts or []:
        start, end = _clock_to_seconds(row.get("startTime")), _clock_to_seconds(row.get("endTime"))
        if row.get("typeCode") == SHIFT_TYPE_CODE and row.get("playerId") is not None and None not in (start, end):
            shifts_by_period.setdefault(row.get("period"), []).append((start, end, row))

    def on_ice(period: Optional[int], goal_time: Optional[int]) -> Optional[List[Dict[str, Any]]]:
        period_shifts = shifts_by_period.get(period)
        if not period_shifts or goal_time is None:
            return None  # no shift data: unknown, not "nobody on the ice"
        # A shift that ends at the goal second was on the ice for it; one that starts then is the faceoff after it.
        players = {}
        for start, end, row in period_shifts:
            if start < goal_time <= end and row["playerId"] not in players:
                players[row["playerId"]] = player(row["playerId"], row)
        return sorted(
            players.values(),
            key=lambda p: (
                p["team_abbr"] or "",
                POSITION_ORDER.get(p["position"], len(POSITION_ORDER)),
                p["sweater_number"] or 0,
            ),
        )

    goals = []
    for play in pbp.get("plays") or []:
        period = play.get("periodDescriptor") or {}
        if play.get("typeDescKey") != "goal" or period.get("periodType") == "SO":
            continue
        details = play.get("details") or {}
        team_id = details.get("eventOwnerTeamId")
        assist_ids = (details.get("assist1PlayerId"), details.get("assist2PlayerId"))
        goals.append(
            {
                "event_id": play.get("eventId"),
                "period": period.get("number"),
                "period_type": period.get("periodType"),
                "time_in_period": play.get("timeInPeriod"),
                "situation_code": play.get("situationCode"),
                "team_abbr": abbr_by_team_id.get(team_id),
                "is_home": None if team_id is None else team_id == home.get("id"),
                "home_team_defending_side": play.get("homeTeamDefendingSide"),
                "x": details.get("xCoord"),
                "y": details.get("yCoord"),
                "zone": details.get("zoneCode"),
                "shot_type": details.get("shotType"),
                "scorer": player(details.get("scoringPlayerId")),
                "assists": [player(pid) for pid in assist_ids if pid is not None],
                "goalie": player(details.get("goalieInNetId")),
                "away_score": details.get("awayScore"),
                "home_score": details.get("homeScore"),
                "highlight_clip_url": details.get("highlightClipSharingUrl"),
                "ppt_replay_url": play.get("pptReplayUrl"),
                "on_ice": on_ice(period.get("number"), _clock_to_seconds(play.get("timeInPeriod"))),
            }
        )

    return {
        "game_id": pbp.get("id"),
        "game_state": pbp.get("gameState"),
        "home_team": _team(home),
        "away_team": _team(away),
        "goals": goals,
    }


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

    def game_goals(self, game_id: str, include_on_ice: bool = True) -> Dict[str, Any]:
        """Gets every goal in a game with both teams, named players, rink coordinates and who was on the ice.

        Joins the play-by-play feed with the shift chart (2 API calls, about 400 KB) into one
        result that's ready to plot. Shootout attempts are left out; they're still in
        ``game_center.play_by_play()`` as plays with ``periodType`` "SO".

        Args:
            game_id (str): 10-digit game ID (e.g., "2024020500").
            include_on_ice (bool): Also fetch the shift chart to fill ``on_ice``. Defaults to
                ``True``. Pass ``False`` to make one API call instead of two.

        Returns:
            Dict[str, Any]: ``game_id``, ``game_state``, ``home_team`` and ``away_team`` (each
            ``{id, abbr, logo, dark_logo}``), and ``goals`` in game order. ``scorer``,
            ``assists``, ``goalie`` and ``on_ice`` share one player shape: ``{player_id,
            first_name, last_name, sweater_number, position, team_abbr, headshot}``.

        Key Response Fields:
            goals[].event_id (int): Play-by-play eventId. Pass it to ``misc.goal_replay()`` for the
                NHL's official ``strength`` and ``goalModifier``.
            goals[].situation_code (str): Four digits: away goalie (1 in net, 0 pulled), away
                skaters, home skaters, home goalie. "1451" is a home power play, "0651" the away
                team with its goalie pulled, "1331" 3-on-3 overtime.
            goals[].x, goals[].y (int): Shot location in feet, (0, 0) at center ice; x runs -100 to
                100 and y -42.5 to 42.5. Teams switch ends each period (see Note).
            goals[].goalie (dict): Goalie scored on. ``None`` for an empty-net goal.
            goals[].away_score, goals[].home_score (int): Score after the goal.
            goals[].highlight_clip_url (str): Public video of the goal.
            goals[].on_ice (list): Skaters and goalies on the ice for the goal, sorted by team, then
                position. ``None`` when ``include_on_ice=False`` or the shift chart has no data for
                that period yet (common while a game is live).
            goals[].ppt_replay_url (str): The NHL's puck and player tracking file for the goal,
                2023-24 onward (``None`` before). The NHL only serves these files to nhl.com, so
                nhlpy doesn't download them.

        Response Docs:
            See ``docs/helpers.md`` for every field and when it's ``None``.

        Note:
            To draw every goal attacking the same end, flip the coordinates when the scoring team
            attacks left::

                attacks_right = (goal["home_team_defending_side"] == "left") == goal["is_home"]
                x, y = (goal["x"], goal["y"]) if attacks_right else (-goal["x"], -goal["y"])

            ``on_ice`` comes from shift times. A player whose shift ends at the goal second is
            included; one whose shift starts then is not, because they came on for the next faceoff.
            For a penalty-shot goal (``situation_code`` "1010" or "0101") it lists the lines from
            the shift chart, not just the shooter and goalie.

        Raises:
            ValueError: If ``game_id`` isn't a 10-digit game ID.

        Example:
            game = client.helpers.game_goals(game_id="2024020500")
            for goal in game["goals"]:
                scorer = goal["scorer"]
                print(goal["time_in_period"], goal["team_abbr"], scorer["first_name"], scorer["last_name"])
        """
        if not re.fullmatch(r"\d{10}", str(game_id)):
            raise ValueError(f"Invalid game_id '{game_id}'. Expected a 10-digit game ID, e.g. '2024020500'.")

        game_center = GameCenter(self.client)
        pbp = game_center.play_by_play(game_id)
        shifts = game_center.shift_chart_data(game_id).get("data", []) if include_on_ice else None
        return _build_game_goals(pbp, shifts)
