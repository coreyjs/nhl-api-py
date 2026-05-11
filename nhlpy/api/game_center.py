from typing import Optional, List
from nhlpy.http_client import HttpClient, Endpoint


class GameCenter:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def boxscore(self, game_id: str) -> dict:
        """Get the full boxscore for a specific NHL game, including team scores, shots on goal,
        and per-player stats broken down by position. Game IDs can be retrieved from the schedule endpoint.

        Args:
            game_id (str): The unique game identifier (e.g. "2023020280").

        Key Response Fields:
            gameState (str): Current state of the game ("FUT", "LIVE", "OFF", "FINAL").
            awayTeam.abbrev (str): Away team abbreviation (e.g. "TOR").
            awayTeam.score (int): Away team total goals.
            homeTeam.abbrev (str): Home team abbreviation (e.g. "BOS").
            homeTeam.score (int): Home team total goals.
            awayTeam.sog (int): Away team shots on goal.
            homeTeam.sog (int): Home team shots on goal.
            playerByGameStats.awayTeam.forwards (list): Per-player stats for away forwards.
            gameOutcome.lastPeriodType (str): Period type the game ended in ("REG", "OT", "SO").

        Response Docs:
            See ``docs/game_center.md`` for the complete response schema.

        Example:
            client.game_center.boxscore(game_id="2023020280")

        Returns:
            dict: Full boxscore data including team totals and player-level game stats.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"gamecenter/{game_id}/boxscore").json()

    def play_by_play(self, game_id: str) -> dict:
        """Get the full play-by-play feed for a specific NHL game, containing every recorded event
        such as shots, goals, faceoffs, hits, and penalties. Game IDs can be retrieved from the
        schedule endpoint.

        Args:
            game_id (str): The unique game identifier (e.g. "2023020280").

        Key Response Fields:
            plays (list): All game events (~340 per game), ordered chronologically.
            plays[].typeDescKey (str): Event type descriptor (e.g. "shot-on-goal", "goal", "faceoff").
            plays[].timeInPeriod (str): Time elapsed in the period (e.g. "12:34").
            plays[].periodDescriptor.number (int): Period number (1, 2, 3, 4 for OT).
            plays[].details.xCoord (float): Ice x-coordinate of the event.
            plays[].details.yCoord (float): Ice y-coordinate of the event.
            rosterSpots (list): Player info for all rostered players in the game.

        Response Docs:
            See ``docs/game_center.md`` for the complete response schema.

        Example:
            client.game_center.play_by_play(game_id="2023020280")

        Returns:
            dict: Complete play-by-play data including all events and roster information.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"gamecenter/{game_id}/play-by-play").json()

    def match_up(self, game_id: str) -> dict:
        """Get the landing-page summary for a specific NHL game, including scoring by period,
        three-stars selections, and penalty details. Game IDs can be retrieved from the
        schedule endpoint.

        Args:
            game_id (str): The unique game identifier (e.g. "2023020280").

        Key Response Fields:
            summary.scoring (list): Goals broken down by period.
            summary.threeStars (list): Three stars of the game, each containing:
                star (int), playerId (int), teamAbbrev (str), name (str), position (str).
            summary.penalties (list): All penalties assessed during the game.
            summary.teamGameStats (list): Head-to-head team stats (SOG, faceoff %, PIM, etc.).
            awayTeam.abbrev (str): Away team abbreviation.
            homeTeam.abbrev (str): Home team abbreviation.

        Response Docs:
            See ``docs/game_center.md`` for the complete response schema.

        Example:
            client.game_center.match_up(game_id="2023020280")

        Returns:
            dict: Detailed game matchup data including scoring summary, three stars, and penalties.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"gamecenter/{game_id}/landing").json()

    def daily_scores(self, date: Optional[str] = None) -> dict:
        """Get scores and game states for all NHL games on a given date. Returns the current
        day's scoreboard when no date is provided, along with navigation links to adjacent dates.

        Args:
            date (str, optional): Date in YYYY-MM-DD format (e.g. "2024-01-15").
                If not provided, returns the current day's scores.

        Key Response Fields:
            currentDate (str): The date for the returned scores (YYYY-MM-DD).
            prevDate (str): Previous date with NHL games, for pagination.
            nextDate (str): Next date with NHL games, for pagination.
            games (list): All games on the requested date.
            games[].awayTeam.abbrev (str): Away team abbreviation (e.g. "NYR").
            games[].awayTeam.score (int): Away team score.
            games[].homeTeam.abbrev (str): Home team abbreviation (e.g. "PIT").
            games[].homeTeam.score (int): Home team score.
            games[].gameState (str): Game state ("FUT", "LIVE", "OFF", "FINAL").

        Response Docs:
            See ``docs/game_center.md`` for the complete response schema.

        Example:
            client.game_center.daily_scores(date="2024-01-15")

        Returns:
            dict: Scoreboard data with all games, scores, statuses, and date navigation.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"score/{date if date else 'now'}").json()

    def shift_chart_data(self, game_id: str, excludes: List[str] = None) -> dict:
        """Get individual player shift data for a specific game, including start/end times and
        durations for every shift. A typical game contains ~740 shift records across both teams.

        Args:
            game_id (str): The unique game identifier (e.g. "2023020280"). Game IDs can be
                retrieved from the schedule endpoint.
            excludes (List[str], optional): Fields to exclude from the response.
                Defaults to ["eventDetails"] if not provided.

        Key Response Fields:
            data (list): All shift records (~740 per game).
            data[].firstName (str): Player's first name.
            data[].lastName (str): Player's last name.
            data[].teamAbbrev (str): Team abbreviation for the player.
            data[].period (int): Period number the shift occurred in.
            data[].startTime (str): Shift start time within the period (e.g. "05:23").
            data[].duration (str): Length of the shift (e.g. "00:45").
            total (int): Total number of shift records returned.

        Response Docs:
            See ``docs/game_center.md`` for the complete response schema.

        Example:
            client.game_center.shift_chart_data(game_id="2023020280")

        Returns:
            dict: Shift chart data containing individual shift records for all players.
        """
        if excludes is None:
            excludes = ["eventDetails"]

        exclude_p: str = ",".join(excludes)
        expr_p: str = f"gameId={game_id} and ((duration != '00:00' and typeCode = 517) or typeCode != 517 )"
        return self.client.get(
            endpoint=Endpoint.API_STATS, resource=f"en/shiftcharts?cayenneExp={expr_p}&exclude={exclude_p}"
        ).json()

    def season_series_matchup(self, game_id: str) -> dict:
        """Get the season-series record and contextual stats for a specific game, including
        head-to-head win totals, team game stats, and linescore data from the right-rail panel.

        Args:
            game_id (str): The unique game identifier (e.g. "2023020280"). Game IDs can be
                retrieved from the schedule endpoint.

        Key Response Fields:
            seasonSeries (list): Results of all regular-season matchups between the two teams.
            seasonSeriesWins (object): Win counts keyed by team ID.
            teamGameStats (list): Comparative team stats for this game (SOG, faceoff %, etc.).
            linescore (object): Period-by-period scoring breakdown.
            gameReports (object): Links to official game reports (e.g. summary, event summary).

        Response Docs:
            See ``docs/game_center.md`` for the complete response schema.

        Example:
            client.game_center.season_series_matchup(game_id="2023020280")

        Returns:
            dict: Season series record, team game stats, linescore, and game report links.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"gamecenter/{game_id}/right-rail").json()

    def game_story(self, game_id: str) -> dict:
        """Get the narrative game story for a specific game, including scoring summaries,
        three-stars selections, and head-to-head team statistics. This is the data behind
        the NHL's post-game recap page.

        Args:
            game_id (str): The unique game identifier (e.g. "2023020280"). Game IDs can be
                retrieved from the schedule endpoint.

        Key Response Fields:
            summary.scoring (list): Goals organized by period, with scorer and assist details.
            summary.threeStars (list): Three stars of the game with player info.
            summary.teamGameStats (list): Comparative team stats (SOG, faceoff %, PIM, hits, etc.).
            awayTeam.abbrev (str): Away team abbreviation.
            homeTeam.abbrev (str): Home team abbreviation.
            gameState (str): Current state of the game ("FUT", "LIVE", "OFF", "FINAL").

        Response Docs:
            See ``docs/game_center.md`` for the complete response schema.

        Example:
            client.game_center.game_story(game_id="2023020280")

        Returns:
            dict: Game story data with scoring summary, three stars, and team stat comparisons.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"wsc/game-story/{game_id}").json()
