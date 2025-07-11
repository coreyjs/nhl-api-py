from typing import Optional, List
from nhlpy.http_client import HttpClient, Endpoint


class GameCenter:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def boxscore(self, game_id: str) -> dict:
        """Get boxscore data for a specific NHL game. GameIds can be retrieved from the schedule endpoint.

        Args:
           game_id (str): The game_id for the game you want the boxscore for

        Example:
           API endpoint format: https://api-web.nhle.com/v1/gamecenter/2023020280/boxscore

        Returns:
           dict: Game boxscore data
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"gamecenter/{game_id}/boxscore").json()

    def play_by_play(self, game_id: str) -> dict:
        """Get play-by-play data for a specific NHL game. GameIds can be retrieved from the schedule endpoint.

        Args:
           game_id (str): The game_id for the game you want the play by play for

        Returns:
           dict: Play-by-play game data
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"gamecenter/{game_id}/play-by-play").json()

    def match_up(self, game_id: str) -> dict:
        """Get detailed match up information for a specific NHL game. GameIds can be retrieved
        from the schedule endpoint.

        Args:
           game_id (str): The game_id for the game you want the landing page for

        Returns:
           dict: Detailed game matchup data
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"gamecenter/{game_id}/landing").json()

    def daily_scores(self, date: Optional[str] = None) -> dict:
        """Get scores for NHL games on a specific date or current day.

        Args:
           date (str, optional): Date to check scores in YYYY-MM-DD format.
                                If not provided, returns current day's scores.

        Returns:
           dict: Game scores and status information
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"score/{date if date else 'now'}").json()

    def shift_chart_data(self, game_id: str, excludes: List[str] = None) -> dict:
        """Gets shift chart data for a specific game.

        Args:
           game_id (str): ID of the game to retrieve shift data for. Game IDs can be retrieved
               from the schedule endpoint.
           excludes (List[str]): List of items to exclude from the response.

        Returns:
           Dict containing the shift chart data.
        """
        if excludes is None:
            excludes = ["eventDetails"]

        exclude_p: str = ",".join(excludes)
        expr_p: str = f"gameId={game_id} and ((duration != '00:00' and typeCode = 517) or typeCode != 517 )"
        return self.client.get(
            endpoint=Endpoint.API_STATS, resource=f"en/shiftcharts?cayenneExp={expr_p}&exclude={exclude_p}"
        ).json()

    def season_series_matchup(self, game_id: str) -> dict:
        """Gets game stats and season series information for a specific game.

        Args:
           game_id (str): ID of the game to retrieve stats for. Game IDs can be retrieved
               from the schedule endpoint.

        Returns:
           Dict containing game stats and season series data.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"gamecenter/{game_id}/right-rail").json()

    def game_story(self, game_id: str) -> dict:
        """Gets game story information for a specific game.

        Args:
           game_id (str): ID of the game to retrieve story for. Game IDs can be retrieved
               from the schedule endpoint.

        Returns:
           Dict containing game story data.
        """
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"wsc/game-story/{game_id}").json()
