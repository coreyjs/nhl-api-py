from typing import Dict, Any, Optional

from nhlpy.http_client import Endpoint, HttpClient


class Players:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def prospects_by_team(self, team_abbr: str) -> dict:
        """Gets prospects for a specific team, grouped by position.

        Retrieves the current prospect pool for a given NHL team, returning
        players organized into positional groups.

        Args:
            team_abbr (str): Team abbreviation (e.g., "BUF", "TOR").

        Returns:
            dict: Prospect data grouped by position with the following structure:

                - ``forwards`` (list[dict]): Forward prospects.
                - ``defensemen`` (list[dict]): Defenseman prospects.
                - ``goalies`` (list[dict]): Goalie prospects.

                Each player dict contains:

                - ``id`` (int): Player ID.
                - ``firstName`` (dict): ``{"default": "..."}`` first name.
                - ``lastName`` (dict): ``{"default": "..."}`` last name.
                - ``positionCode`` (str): Position code (e.g., "C", "L", "R", "D", "G").
                - ``birthDate`` (str): Date of birth in YYYY-MM-DD format.
                - ``birthCountry`` (str): Three-letter country code.

        See Also:
            https://api-web.nhle.com/v1/prospects/{team_abbr}
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"prospects/{team_abbr}").json()

    def players_by_team(self, team_abbr: str, season: str) -> Dict[str, Any]:
        """Gets the roster for a given team and season, grouped by position.

        Provides the same data as ``teams.team_roster()``, exposed through the
        Players API for convenience.

        Args:
            team_abbr (str): Team abbreviation (e.g., "BUF", "TOR").
            season (str): Season in YYYYYYYY format (e.g., "20232024").

        Returns:
            Dict[str, Any]: Roster data grouped by position with the following structure:

                - ``forwards`` (list[dict]): Forward players.
                - ``defensemen`` (list[dict]): Defenseman players.
                - ``goalies`` (list[dict]): Goalie players.

                Each player dict contains:

                - ``id`` (int): Player ID.
                - ``firstName`` (dict): ``{"default": "..."}`` first name.
                - ``lastName`` (dict): ``{"default": "..."}`` last name.
                - ``sweaterNumber`` (int): Jersey number.
                - ``positionCode`` (str): Position code (e.g., "C", "L", "R", "D", "G").

        See Also:
            https://api-web.nhle.com/v1/roster/{team_abbr}/{season}
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"roster/{team_abbr}/{season}").json()

    def player_bio(self, player_id: str) -> Dict[str, Any]:
        """Gets a player's biographical information.

        Retrieves vitals, bio text, transaction notes, draft details, awards, badges and
        the player's current team (with its roster). Optional sections are omitted when
        they don't apply, e.g. ``currentTeam`` for retired players or ``draftDetails``
        for undrafted players.

        Args:
            player_id (str): The unique identifier for the NHL player (e.g., "8478402").

        Returns:
            Dict[str, Any]: A dictionary containing the player's biographical information.

        Key Response Fields:
            vitals.birthDate (str): Date of birth in YYYY-MM-DD format
            vitals.heightInches (int): Height in inches
            vitals.weightPounds (int): Weight in pounds
            vitals.shootsCatches (str): Handedness ("L" or "R")
            bio.firstName.default (str): Player's first name
            bio.lastName.default (str): Player's last name
            bio.notesTransactions.default (str): Markdown bullet list of signings and trades
            currentTeam.teamAbbrev (str, optional): Current team abbreviation; absent for retired players
            draftDetails (dict, optional): Draft year, team, round and overall pick; absent if undrafted
            awards (list, optional): Trophies won, each with ``details`` listing the years won

        Response Docs:
            docs/players.md

        See Also:
            https://api-web.nhle.com/v2/player/{player_id}/bio
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V2, resource=f"player/{player_id}/bio").json()

    def player_header(self, player_id: str) -> Dict[str, Any]:
        """Gets a player's header summary: identity, position, size and current team.

        This is the compact summary nhl.com shows at the top of every player page.
        Retired players have no ``team``, ``age`` or ``isCaptain`` and may include ``badges``.

        Args:
            player_id (str): The unique identifier for the NHL player (e.g., "8478402").

        Returns:
            Dict[str, Any]: A dictionary containing the player's header information.

        Key Response Fields:
            playerId (int): Unique NHL player identifier
            firstName.default (str): Player's first name
            lastName.default (str): Player's last name
            position (str): Position code (e.g., "C", "L", "R", "D", "G")
            sweaterNumber (int): Jersey number
            headshot (str): URL to the player's headshot image
            isInactiveNHL (bool): True if the player is no longer active in the NHL
            team.abbrev (str, optional): Current team abbreviation; absent for retired players

        Response Docs:
            docs/players.md

        See Also:
            https://api-web.nhle.com/v2/player/{player_id}/header
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V2, resource=f"player/{player_id}/header").json()

    def player_home(self, player_id: str) -> Dict[str, Any]:
        """Gets a player's last and next game, plus their current team's roster.

        Backs the "home" tab of a player page on nhl.com. ``lastGame`` and ``nextGame`` are
        omitted when there is no such game; retired players get only ``lastName``.

        Args:
            player_id (str): The unique identifier for the NHL player (e.g., "8478402").

        Returns:
            Dict[str, Any]: A dictionary containing the player's recent and upcoming game info.

        Key Response Fields:
            teamAbbrev (str): Current team abbreviation
            lastGame.id (int): Game ID of the player's most recent game
            lastGame.gameDate (str): Date of the most recent game in YYYY-MM-DD format
            lastGame.playerStats (dict): Player's line in that game (goals, assists, points, shotsOnGoal, timeOnIce)
            nextGame.id (int): Game ID of the player's next game
            nextGame.startTimeUTC (str): Start time of the next game in ISO 8601 UTC
            nextGame.matchupStats (dict): Player's career stats vs. the next opponent
            currentTeam.roster (dict): Current team roster grouped into forwards, defensemen and goalies

        Response Docs:
            docs/players.md

        See Also:
            https://api-web.nhle.com/v2/player/{player_id}/home
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V2, resource=f"player/{player_id}/home").json()

    def player_stats(self, player_id: str) -> Dict[str, Any]:
        """Gets a player's stat line, last 5 games, career totals and season-by-season totals.

        Backs the "stats" tab of a player page on nhl.com. Stat fields differ for skaters
        and goalies (e.g., goalies have ``savePctg``, ``goalsAgainstAvg``, ``wins``).

        Args:
            player_id (str): The unique identifier for the NHL player (e.g., "8478402").

        Returns:
            Dict[str, Any]: A dictionary containing the player's statistics.

        Key Response Fields:
            statline.isPlayerActive (bool): Whether the player is active
            statline.regularSeason.current (dict): Current-season stats, each as {value, rank, ...}; active only
            statline.regularSeason.career (dict): Career stats, each as {value, rank, ...}
            last5.games (list): The player's last 5 games; empty for retired players
            last5.totals (dict): Totals across the last 5 games
            careerTotals.regularSeason (dict): Career regular season totals (goals, assists, points, ...)
            careerTotals.playoffs (dict): Career playoff totals
            seasonTotals (list): Per-season totals, including non-NHL leagues (see ``leagueAbbrev``)

        Response Docs:
            docs/players.md

        See Also:
            https://api-web.nhle.com/v2/player/{player_id}/player-stats
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V2, resource=f"player/{player_id}/player-stats").json()

    def player_game_log(self, player_id: str, season: Optional[str] = None, game_type: int = 2) -> Dict[str, Any]:
        """Gets a player's game-by-game log from the v2 API.

        Unlike ``stats.player_game_log()`` (v1), each game here includes both teams, the final
        score, the period the game ended in and the team result (``decision``). The full response
        is returned, including ``playerStatsSeasons`` (which seasons/game types have data).

        Args:
            player_id (str): The unique identifier for the NHL player (e.g., "8478402").
            season (str, optional): Season in YYYYYYYY format (e.g., "20242025"). Defaults to the current season.
            game_type (int, optional): Type of games (defaults to 2). Ignored when ``season`` is not set:
                1: Preseason
                2: Regular season
                3: Playoffs

        Returns:
            Dict[str, Any]: A dictionary containing the game log and available seasons.

        Key Response Fields:
            seasonId (int): Season the log covers
            gameTypeId (int): Game type the log covers
            playerStatsSeasons (list): Seasons with data, each as {season, gameTypes}
            gameLog (list): One entry per game, most recent first
            gameLog[].id (int): Game ID
            gameLog[].homeTeam.abbrev / awayTeam.abbrev (str): Teams in the game
            gameLog[].homeScore / awayScore (int): Final score
            gameLog[].goals / assists / points / toi: Skater line (goalies get saves, savePctg, goalsAgainst)

        Response Docs:
            docs/players.md

        See Also:
            https://api-web.nhle.com/v2/player/{player_id}/game-log/{season}/{game_type}
            https://api-web.nhle.com/v2/player/{player_id}/game-log/now
        """
        if season is None:
            resource = f"player/{player_id}/game-log/now"
        else:
            resource = f"player/{player_id}/game-log/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V2, resource=resource).json()
