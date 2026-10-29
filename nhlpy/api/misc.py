from typing import Any, Dict, List

from nhlpy.http_client import HttpClient, Endpoint


class Misc:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def glossary(self) -> List[dict]:
        """Gets the full NHL glossary of statistical terms and abbreviations.

        Returns a list of approximately 321 glossary entries that define every
        abbreviation and term used across the NHL stats API.

        Returns:
            List[dict]: List of glossary entries. Each dict contains:

                - ``id`` (int): Unique glossary entry identifier.
                - ``abbreviation`` (str): Short-form abbreviation (e.g., "GP", "SOG").
                - ``definition`` (str): Human-readable definition of the term.
                - ``fullName`` (str): Full name of the term.

        See Also:
            https://api.nhle.com/stats/rest/en/glossary
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/glossary?sort=fullName").json()
        return response.get("data", [])

    def config(self) -> dict:
        """Gets the stats API configuration, including available report types and filters.

        Returns a dictionary describing the report types available for players,
        goalies, and teams, along with their supported filter options.

        Returns:
            dict: Configuration data with the following top-level keys:

                - ``playerReportData`` (dict): Report type names as keys,
                  each mapping to supported filters and sort options.
                - ``goalieReportData`` (dict): Same structure for goalie reports.
                - ``teamReportData`` (dict): Same structure for team reports.

        See Also:
            https://api.nhle.com/stats/rest/en/config
        """
        return self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/config").json()

    def countries(self) -> List[dict]:
        """Gets the list of countries recognized by the NHL.

        Returns approximately 49 countries that have had players in the NHL,
        including both full names and ISO-style codes.

        Returns:
            List[dict]: List of country entries. Each dict contains:

                - ``id`` (str): Three-letter country code (e.g., "CAN", "USA").
                - ``countryName`` (str): Full country name (e.g., "Canada").
                - ``nationalityName`` (str): Nationality label (e.g., "Canadian").
                - ``countryCode`` (str): Two-letter country code (e.g., "CA", "US").

        See Also:
            https://api.nhle.com/stats/rest/en/country
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/country").json()
        return response.get("data", [])

    def season_specific_rules_and_info(self) -> List[dict]:
        """Gets rules and metadata for every NHL season on record.

        Returns a list of approximately 108 seasons, each describing the
        number of games, conference/division usage, and other rule variations
        for that particular season.

        Returns:
            List[dict]: List of season entries. Each dict contains:

                - ``id`` (int): Season identifier (e.g., 20232024).
                - ``formattedSeasonId`` (str): Human-readable season label
                  (e.g., "2023-24").
                - ``numberOfGames`` (int): Number of regular-season games.
                - ``conferencesInUse`` (int): Whether conferences were active.

        See Also:
            https://api.nhle.com/stats/rest/en/season
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/season").json()
        return response.get("data", [])

    def draft_year_and_rounds(self) -> List[dict]:
        """Gets the number of rounds for each NHL draft year.

        Returns a list of approximately 63 entries covering every draft year
        on record, useful for validating draft round filters in queries.

        Returns:
            List[dict]: List of draft year entries. Each dict contains:

                - ``id`` (int): Unique identifier for the draft year record.
                - ``draftYear`` (int): The calendar year of the draft (e.g., 2023).
                - ``rounds`` (int): Number of rounds held in that draft.

        See Also:
            https://api.nhle.com/stats/rest/en/draft
        """
        response = self.client.get(endpoint=Endpoint.API_CORE, resource="stats/rest/en/draft").json()
        return response.get("data", [])

    def how_to_watch(self, game_id: str) -> Dict[str, Any]:
        """Gets where a game can be watched, by country and market.

        This is the data behind the "How to Watch" modal on nhl.com game pages.

        Args:
            game_id (str): Game ID (e.g., "2024020641").

        Returns:
            Dict[str, Any]: Viewing guide for the game.

        Key Response Fields:
            title.default (str): Matchup title (e.g., "Oilers @ Islanders")
            countries (list): Countries with a viewing guide, each with ``id``, ``abbr`` and localized ``name``
            panels (list): One panel per market
            panels[].market (str): Market name (e.g., "All Other Countries")
            panels[].countries (list[str]): Country codes the panel applies to
            panels[].broadcasters (list, optional): Broadcasters and streaming options; regional panels use homeTeam/awayTeam

        Response Docs:
            docs/misc.md

        Example:
            client.misc.how_to_watch(game_id="2026020220")
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"how-to-watch/{game_id}").json()

    def tv_schedule(self, date: str = "now") -> Dict[str, Any]:
        """Gets the NHL Network TV schedule for a window of dates around ``date``.

        Args:
            date (str, optional): Date in YYYY-MM-DD format. Defaults to "now".

        Returns:
            Dict[str, Any]: NHL Network programming for the window ``startDate``..``endDate``.

        Key Response Fields:
            date (str): Requested date
            startDate (str): First date in the returned window
            endDate (str): Last date in the returned window
            broadcasts (list): Programs in the window
            broadcasts[].title (str): Program title
            broadcasts[].startTime / endTime (str): Start and end time (ISO 8601)
            broadcasts[].durationSeconds (int): Length in seconds
            broadcasts[].broadcastStatus (str): "LIVE" for live programs, otherwise empty

        Response Docs:
            docs/misc.md

        Example:
            client.misc.tv_schedule()
            client.misc.tv_schedule(date="2025-01-07")
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"network/tv-schedule/{date}").json()

    def player_spotlight(self) -> List[Dict[str, Any]]:
        """Gets the players currently featured in the nhl.com player spotlight.

        Returns:
            List[Dict[str, Any]]: Featured players, in display order.

        Key Response Fields:
            playerId (int): Player ID
            name.default (str): Player name
            position (str): Position code
            sweaterNumber (int): Jersey number
            teamTriCode (str): Team abbreviation
            headshot (str): Headshot image URL
            sortId (int): Display order

        Response Docs:
            docs/misc.md

        Example:
            client.misc.player_spotlight()
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource="player-spotlight").json()

    def goal_replay(self, game_id: str, event_id: str) -> Dict[str, Any]:
        """Gets the puck and player tracking (PPT) replay details for a goal.

        ``event_id`` is the play-by-play ``eventId`` of a goal. For an event that isn't a goal, the
        response only contains the game details and has no ``goal`` key.

        Args:
            game_id (str): Game ID (e.g., "2024020641").
            event_id (str): Play-by-play event ID of the goal.

        Returns:
            Dict[str, Any]: Game details plus the goal and its replay links.

        Key Response Fields:
            id (int): Game ID
            gameDate (str): Game date, YYYY-MM-DD
            awayTeam / homeTeam (dict): Teams in the game
            goal.firstName.default / goal.lastName.default (str): Goal scorer
            goal.timeInPeriod (str): Time of the goal in the period
            goal.shotType (str): Shot type (e.g., "wrist")
            goal.assists (list): Assisting players
            goal.pptReplayUrl (str): URL of the tracking replay data

        Response Docs:
            docs/misc.md

        Example:
            pbp = client.game_center.play_by_play(game_id="2024020641")
            goal = next(p for p in pbp["plays"] if p["typeDescKey"] == "goal")
            client.misc.goal_replay(game_id="2024020641", event_id=goal["eventId"])
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"ppt-replay/goal/{game_id}/{event_id}").json()
