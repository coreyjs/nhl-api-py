from datetime import datetime
from typing import Optional, List

from nhlpy.http_client import HttpClient


class Schedule:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def get_schedule(self, date: str = None) -> dict:
        """
        Get the schedule for the NHL for the given date.  Contains only games for the given date.
        :param date:  In format YYYY-MM-DD.
        :return: dict
        """
        try:
            # Parse and reformat the date to ensure YYYY-MM-DD
            date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

        schedule_data: dict = self.client.get(resource=f"schedule/{date}").json()
        response_payload = {
            "nextStartDate": schedule_data["nextStartDate"],
            "previousStartDate": schedule_data["previousStartDate"],
            "date": date,
            "oddsPartners": schedule_data["oddsPartners"],
        }

        matching_day = next((day for day in schedule_data["gameWeek"] if day["date"] == date), None)

        if matching_day:
            response_payload["games"] = matching_day["games"]
            response_payload["numberOfGames"] = len(matching_day["games"])

        return response_payload

    def get_weekly_schedule(self, date: Optional[str] = None) -> dict:
        """
        Get the schedule for the NHL for the week of `date`.  If no date is supplied it will
        default to today. What the "NHL" deems as "today" seems to switch over around 12 est.  Its preferred you
        supply a date

        :param date:  In format YYYY-MM-DD.  If no date is supplied, it will default to "Today".  Which in case
            of the NHL could be today or yesterday depending on how early you call it.
        :return: dict
        """
        res = date if date else "now"

        return self.client.get(resource=f"schedule/{res}").json()

    def get_schedule_by_team_by_month(self, team_abbr: str, month: Optional[str] = None) -> List[dict]:
        """
        Get the schedule for the team (team_abbr) for the given month.  If no month is supplied it will
        :param team_abbr: The 3 letter abbreviation of the team.  BUF, TOR, etc
        :param month: In format YYYY-MM.  2021-10, 2021-11, etc.  Defaults to "now" otherwise.
        :return:
        """
        resource = f"club-schedule/{team_abbr}/month/{month if month else 'now'}"
        return self.client.get(resource=resource).json()["games"]

    def get_schedule_by_team_by_week(self, team_abbr: str, date: Optional[str] = None) -> List[dict]:
        """
        This returns the schedule for the team (team_abbr) for the week set or the current week if no week is specified.

        :param date: Optional date, in which to search the week of.  In format YYYY-MM-DD.  Example "2024-02-10".
        :param team_abbr: The 3 letter abbreviation of the team.  BUF, TOR, etc
        :return:
        """
        resource = f"club-schedule/{team_abbr}/week/{date if date else 'now'}"
        return self.client.get(resource=resource).json()["games"]

    def get_season_schedule(self, team_abbr: str, season: str) -> dict:
        """
        This returns the schedule for the team (team_abbr) for the current season.  This also
        contains all the metadata from the base api request.
        :param team_abbr: Team abbreviation.  BUF, TOR, etc
        :param season: Season in format YYYYYYYY.  20202021, 20212022, etc
        :return:
        """
        return self.client.get(resource=f"club-schedule-season/{team_abbr}/{season}").json()

    def schedule_calendar(self, date: str) -> dict:
        """
        This returns the schedule for the given date in a calendar format.  Im not really sure
        how this is diff from the other endppoints.
        https://api-web.nhle.com/v1/schedule-calendar/2023-11-08
        :param date: In format 2023-11-23
        :return:
        """
        return self.client.get(resource=f"schedule-calendar/{date}").json()
