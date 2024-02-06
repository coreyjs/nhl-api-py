from nhlpy.http_client import HttpClient


class Stats:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def club_stats_season(self, team_abbr: str) -> dict:
        """
        This seems to return gameTypes for every season the team was in existence.  Maybe its useful?
        :param team_abbr: The 3 letter abbreviation of the team.  BUF, TOR, etc
        :return: dict
        """
        return self.client.get(resource=f"club-stats-season/{team_abbr}").json()

    def player_career_stats(self, player_id: int) -> dict:
        """
        This returns the career stats for a player as well as player information.

        example: https://api-web.nhle.com/v1/player/8481528/landing

        :param player_id: The player_id for the player you want the stats for.
        :return: dict
        """
        return self.client.get(resource=f"player/{player_id}/landing").json()
