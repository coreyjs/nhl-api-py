from typing import Optional, List
from nhlpy.api import BaseNHLAPIClient


class Schedule(BaseNHLAPIClient):
    def get_schedule(self, date: Optional[str] = None) -> dict:
        """
        Get the schedule for the NHL for the given date.  If no date is supplied it will
        default to today.
        :param date:  In format YYYY-MM-DD.  If no date is supplied, it will default to "Today".  Which in case
            of the NHL could be today or yesterday depending on how early you call it.
        :return: dict
        """
        res = date if date else "now"

        return self._get(resource=f"schedule/{res}").json()

    def get_schedule_by_team_by_month(self, team_abbr: str, month: Optional[str] = None) -> List[dict]:
        """
        Get the schedule for the team (team_abbr) for the given month.  If no month is supplied it will
        :param team_abbr: The 3 letter abbreviation of the team.  BUF, TOR, etc
        :param month: In format YYYY-MM.  2021-10, 2021-11, etc.  Defaults to "now" otherwise.
        :return:
        """
        resource = f"club-schedule/{team_abbr}/month/{month if month else 'now'}"
        return self._get(resource=resource).json()["games"]

    def get_schedule_by_team_by_week(self, team_abbr: str) -> List[dict]:
        """
        This returns the schedule for the team (team_abbr) for the current week.
        :param team_abbr: The 3 letter abbreviation of the team.  BUF, TOR, etc
        :return:
        """
        resource = f"club-schedule/{team_abbr}/week/now"
        return self._get(resource=resource).json()["games"]

    def get_season_schedule(self, team_abbr: str, season: str) -> dict:
        """
        This returns the schedule for the team (team_abbr) for the current season.  This also
        contains all the metadata from the base api request.
        :param team_abbr: Team abbreviation.  BUF, TOR, etc
        :param season: Season in format YYYYYYYY.  20202021, 20212022, etc
        :return:
        """
        return self._get(resource=f"club-schedule-season/{team_abbr}/{season}").json()
