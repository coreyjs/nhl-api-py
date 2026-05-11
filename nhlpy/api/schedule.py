from datetime import datetime
from typing import Optional, List

from nhlpy.http_client import HttpClient, Endpoint


class Schedule:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def daily_schedule(self, date: Optional[str] = None) -> dict:
        """Gets NHL schedule for a specific date.

        This method transforms the raw API response by extracting only the
        matching day from the ``gameWeek`` list and flattening it into a
        single-date payload.

        Args:
           date (str): Date in YYYY-MM-DD format. Defaults to today's date.

        Returns:
           dict: Transformed schedule data for the specified date.

        Key Response Fields:
            nextStartDate (str): Next date with scheduled games.
            previousStartDate (str): Previous date with scheduled games.
            date (str): The requested date.
            games (list): List of game objects for the date.
            games[].id (int): Unique game identifier.
            games[].awayTeam.abbrev (str): Away team abbreviation.
            games[].homeTeam.abbrev (str): Home team abbreviation.
            games[].gameState (str): Game state code (e.g., ``"FUT"``,
                ``"LIVE"``, ``"OFF"``).
            numberOfGames (int): Total number of games on the date.

        Response Docs:
            https://api-web.nhle.com/v1/schedule/{date}

        Example:
            client.schedule.daily_schedule(date="2024-02-10")
        """
        try:
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")  # Default to today's date
            else:
                # Parse and reformat the date to ensure YYYY-MM-DD
                date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        schedule_data: dict = self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"schedule/{date}").json()
        response_payload = {
            "nextStartDate": schedule_data.get("nextStartDate", None),
            "previousStartDate": schedule_data.get("previousStartDate", None),
            "date": date,
            "oddsPartners": schedule_data.get("oddsPartners", None),
        }

        game_week = schedule_data.get("gameWeek", [])
        matching_day = next((day for day in game_week if day.get("date") == date), None)

        if matching_day:
            games = matching_day.get("games", [])
            response_payload["games"] = games
            response_payload["numberOfGames"] = len(games)

        return response_payload

    def weekly_schedule(self, date: Optional[str] = None) -> dict:
        """Gets NHL schedule for a week starting from the specified date.

        Args:
           date (str, optional): Date in YYYY-MM-DD format. Defaults to today's
               date. Note: NHL's "today" typically shifts around 12:00 EST.

        Returns:
           dict: Weekly game schedule data.

        Key Response Fields:
            nextStartDate (str): Start date of the following week.
            previousStartDate (str): Start date of the preceding week.
            gameWeek (list): List of 7 day objects spanning the week.
            gameWeek[].date (str): Date string for the day (``YYYY-MM-DD``).
            gameWeek[].games (list): List of game objects for that day.
            numberOfGames (int): Total number of games across the week.

        Response Docs:
            https://api-web.nhle.com/v1/schedule/{date}

        Example:
            client.schedule.weekly_schedule(date="2024-02-10")
        """
        res = date if date else "now"

        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"schedule/{res}").json()

    def team_monthly_schedule(self, team_abbr: str, month: Optional[str] = None) -> List[dict]:
        """Gets monthly schedule for a specified team.

        If no month is supplied it defaults to the current month.

        Args:
            team_abbr (str): Three-letter team abbreviation (e.g., ``"BUF"``,
                ``"TOR"``).
            month (str, optional): Month in ``YYYY-MM`` format (e.g.,
                ``"2021-10"``). Defaults to current month.

        Returns:
            List[dict]: List of game dicts for the monthly schedule.

        Key Response Fields (per game dict):
            id (int): Unique game identifier.
            gameDate (str): Date of the game.
            awayTeam.abbrev (str): Away team abbreviation.
            homeTeam.abbrev (str): Home team abbreviation.
            gameState (str): Game state code (e.g., ``"FUT"``, ``"OFF"``).
            winningGoalie (dict or None): Winning goalie info, if applicable.

        Response Docs:
            https://api-web.nhle.com/v1/club-schedule/{team}/month/{month}

        Example:
            client.schedule.team_monthly_schedule(team_abbr="TOR", month="2024-01")
        """
        resource = f"club-schedule/{team_abbr}/month/{month if month else 'now'}"
        response = self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()
        return response.get("games", [])

    def team_weekly_schedule(self, team_abbr: str, date: Optional[str] = None) -> List[dict]:
        """Gets weekly schedule for a specified team.

        If no date is supplied it defaults to the current week.

        Args:
            team_abbr (str): Three-letter team abbreviation (e.g., ``"BUF"``,
                ``"TOR"``).
            date (str, optional): Date in ``YYYY-MM-DD`` format. Returns
                the schedule for the week containing this date. Defaults to
                current week.

        Returns:
            List[dict]: List of game dicts for the weekly schedule.

        Key Response Fields (per game dict):
            id (int): Unique game identifier.
            gameDate (str): Date of the game.
            awayTeam.abbrev (str): Away team abbreviation.
            homeTeam.abbrev (str): Home team abbreviation.
            gameState (str): Game state code (e.g., ``"FUT"``, ``"OFF"``).
            winningGoalie (dict or None): Winning goalie info, if applicable.

        Response Docs:
            https://api-web.nhle.com/v1/club-schedule/{team}/week/{date}

        Example:
            client.schedule.team_weekly_schedule(team_abbr="BUF", date="2024-02-10")
        """
        resource = f"club-schedule/{team_abbr}/week/{date if date else 'now'}"
        response = self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()
        return response.get("games", [])

    def team_season_schedule(self, team_abbr: str, season: str) -> dict:
        """Gets the full season schedule for a specified team.

        Args:
            team_abbr (str): Three-letter team abbreviation (e.g., ``"BUF"``,
                ``"TOR"``).
            season (str): Season in ``YYYYYYYY`` format (e.g., ``"20232024"``).

        Returns:
            dict: Complete season schedule data including metadata.

        Key Response Fields:
            previousSeason (int): Previous season identifier.
            currentSeason (int): Current season identifier.
            nextSeason (int): Next season identifier.
            clubTimezone (str): Team's local timezone (e.g.,
                ``"America/New_York"``).
            games (list): List of game dicts for the entire season.

        Response Docs:
            https://api-web.nhle.com/v1/club-schedule-season/{team}/{season}

        Example:
            client.schedule.team_season_schedule(team_abbr="TOR", season="20232024")
        """
        request = self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"club-schedule-season/{team_abbr}/{season}")

        return request.json()

    def calendar_schedule(self, date: str) -> dict:
        """Gets the schedule in calendar format for a specified date.

        Returns a high-level calendar view of the schedule, including a list
        of all 32 teams and their metadata.

        Args:
            date (str): Date in ``YYYY-MM-DD`` format (e.g., ``"2023-11-23"``).

        Returns:
            dict: Calendar-formatted schedule data.

        Key Response Fields:
            startDate (str): Start date of the calendar window.
            endDate (str): End date of the calendar window.
            teams (list): List of all 32 NHL teams.
            teams[].abbrev (str): Team abbreviation.
            teams[].commonName.default (str): Common team name.

        Response Docs:
            https://api-web.nhle.com/v1/schedule-calendar/{date}

        Example:
            client.schedule.calendar_schedule(date="2023-11-08")
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"schedule-calendar/{date}").json()

    def playoff_carousel(self, season: str) -> dict:
        """Gets all playoff series information up to the current round.

        Args:
            season (str): Season in ``YYYYYYYY`` format (e.g., ``"20232024"``).

        Returns:
            dict: Playoff series data for the specified season.

        Key Response Fields:
            seasonId (int): Season identifier.
            currentRound (int): The current active playoff round number.
            rounds (list): List of round objects.
            rounds[].series (list): List of series within each round.

        Response Docs:
            https://api-web.nhle.com/v1/playoff-series/carousel/{season}

        Example:
            client.schedule.playoff_carousel(season="20232024")
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"playoff-series/carousel/{season}").json()

    def playoff_series_schedule(self, season: str, series: str) -> dict:
        """Returns the schedule and results for a specified playoff series matchup.

        Args:
            season (str): Season in ``YYYYYYYY`` format (e.g., ``"20252026"``).
            series (str): Series letter identifier (``"a"``-``"h"`` for Round 1,
                ``"i"``-``"l"`` for Round 2, ``"m"``-``"n"`` for CF, ``"o"`` for SCF).

        Returns:
            dict: Series schedule data for the specified playoff matchup.

        Key Response Fields:
            round (int): Playoff round number.
            seriesLetter (str): Series letter identifier (e.g., "B").
            neededToWin (int): Wins required to advance (4).
            length (int): Total games played in the series.
            topSeedTeam.abbrev (str): Top seed team abbreviation.
            topSeedTeam.seed (int): Seed number.
            topSeedTeam.record (str): Series record (e.g., "3-4").
            bottomSeedTeam.abbrev (str): Bottom seed team abbreviation.
            bottomSeedTeam.seriesWins (int): Series wins for the bottom seed.
            games (list): List of game objects in the series.
            games[].gameNumber (int): Game number within the series (1-7).
            games[].ifNecessary (bool): Whether the game was an "if necessary" game.
            games[].seriesStatus.topSeedWins (int): Top seed wins after this game.
            games[].seriesStatus.bottomSeedWins (int): Bottom seed wins after this game.

        Response Docs:
            docs/schedule.md

        Example:
            client.schedule.playoff_series_schedule(season="20252026", series="b")
        """

        return self.client.get(
            endpoint=Endpoint.API_WEB_V1, resource=f"schedule/playoff-series/{season}/{series}"
        ).json()

    def playoff_bracket(self, year: str) -> dict:
        """Returns the full playoff bracket for a given year.

        Args:
            year (str): Year the playoffs take place (e.g., ``"2024"``).

        Returns:
            dict: Playoff bracket data.

        Key Response Fields:
            bracketLogo (str): URL of the playoff bracket logo.
            series (list): List of all 15 playoff series.
            series[].topSeedTeam.abbrev (str): Top-seed team abbreviation.
            series[].bottomSeedTeam.abbrev (str): Bottom-seed team abbreviation.
            series[].topSeedWins (int): Number of wins for the top seed.

        Response Docs:
            https://api-web.nhle.com/v1/playoff-bracket/{year}

        Example:
            client.schedule.playoff_bracket(year="2024")
        """

        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"playoff-bracket/{year}").json()
