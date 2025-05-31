from datetime import datetime
from typing import Optional, List

from nhlpy.http_client import HttpClient


class Schedule:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def get_schedule(self, date: str = None) -> dict:
        """Gets NHL schedule for a specific date.

        Args:
           date (str): Date in YYYY-MM-DD format.

        Returns:
           dict: Game schedule data for the specified date.
        """
        try:
            # Parse and reformat the date to ensure YYYY-MM-DD
            date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        schedule_data: dict = self.client.get(resource=f"schedule/{date}").json()
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

    def get_weekly_schedule(self, date: Optional[str] = None) -> dict:
        """Gets NHL schedule for a week starting from the specified date.

        Args:
           date (str, optional): Date in YYYY-MM-DD format. Defaults to today's date.
               Note: NHL's "today" typically shifts around 12:00 EST.

        Returns:
           dict: Weekly game schedule data.
        """
        res = date if date else "now"

        return self.client.get(resource=f"schedule/{res}").json()

    def get_schedule_by_team_by_month(self, team_abbr: str, month: Optional[str] = None) -> List[dict]:
        """Gets monthly schedule for specified team or the given month.  If no month is supplied it will default to now.

        Args:
            team_abbr (str): Three-letter team abbreviation (e.g., BUF, TOR)
            month (str, optional): Month in YYYY-MM format (e.g., 2021-10). Defaults to current month.

        Returns:
            List[dict]: List of games in the monthly schedule.
        """
        resource = f"club-schedule/{team_abbr}/month/{month if month else 'now'}"
        response = self.client.get(resource=resource).json()
        return response.get("games", [])

    def get_schedule_by_team_by_week(self, team_abbr: str, date: Optional[str] = None) -> List[dict]:
        """Gets weekly schedule for specified team.  If no date is supplied it will default to current week.

        Args:
            team_abbr (str): Three-letter team abbreviation (e.g., BUF, TOR)
            date (str, optional): Date in YYYY-MM-DD format. Gets schedule for week containing this date.
                Defaults to current week.

        Returns:
            List[dict]: List of games in the weekly schedule.
        """
        resource = f"club-schedule/{team_abbr}/week/{date if date else 'now'}"
        response = self.client.get(resource=resource).json()
        return response.get("games", [])

    def get_season_schedule(self, team_abbr: str, season: str) -> dict:
        """Gets full season schedule for specified team.

        Args:
            team_abbr (str): Three-letter team abbreviation (e.g., BUF, TOR)
            season (str): Season in YYYYYYYY format (e.g., 20232024)

        Returns:
            dict: Complete season schedule data including metadata.
        """
        request = self.client.get(resource=f"club-schedule-season/{team_abbr}/{season}")

        return request.json()

    def schedule_calendar(self, date: str) -> dict:
        """Gets schedule in calendar format for specified date. Im not really sure
        how this is diff from the other endppoints.

           Args:
               date (str): Date in YYYY-MM-DD format (e.g., 2023-11-23)

           Returns:
               dict: Calendar-formatted schedule data.

           Example:
               API endpoint: https://api-web.nhle.com/v1/schedule-calendar/2023-11-08
        """
        return self.client.get(resource=f"schedule-calendar/{date}").json()
