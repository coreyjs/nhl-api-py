from typing import Optional, List
from nhlpy.http_client import HttpClient


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
        return self.client.get(resource=f"gamecenter/{game_id}/boxscore").json()

    def play_by_play(self, game_id: str) -> dict:
        """Get play-by-play data for a specific NHL game. GameIds can be retrieved from the schedule endpoint.

        Args:
           game_id (str): The game_id for the game you want the play by play for

        Returns:
           dict: Play-by-play game data
        """
        return self.client.get(resource=f"gamecenter/{game_id}/play-by-play").json()

    def landing(self, game_id: str) -> dict:
        """Get detailed match up information for a specific NHL game. GameIds can be retrieved
        from the schedule endpoint.

        Args:
           game_id (str): The game_id for the game you want the landing page for

        Returns:
           dict: Detailed game matchup data
        """
        return self.client.get(resource=f"gamecenter/{game_id}/landing").json()

    def score_now(self, date: Optional[str] = None) -> dict:
        """Get current scores for NHL games. GameDay updates at noon est I think.

        Args:
           date (str, optional): Date to check scores in YYYY-MM-DD format

        Returns:
           dict: Game scores and status information
        """
        return self.client.get(resource=f"score/{date if date else 'now'}").json()

    def shift_chart_data(self, game_id: str, excludes: List[str] = None) -> dict:
        """Gets shift chart data for a specific game.

        Args:
           game_id (str): ID of the game to retrieve shift data for. Game IDs can be retrieved
               from the schedule endpoint.
           excludes (List[str]): List of items to exclude from the response.

        Returns:
           Dict containing the shift chart data.
        """
        if not excludes:
            excludes = ["eventDetails"]

        base_url: str = "https://api.nhle.com/stats/rest/en/shiftcharts"
        exclude_p: str = ",".join(excludes)
        expr_p: str = f"gameId={game_id} and ((duration != '00:00' and typeCode = 517) or typeCode != 517 )"
        return self.client.get_by_url(full_resource=f"{base_url}?cayenneExp={expr_p}&exclude={exclude_p}").json()

    def right_rail(self, game_id: str) -> dict:
        """Gets game stats and season series information for a specific game.

        Args:
           game_id (str): ID of the game to retrieve stats for. Game IDs can be retrieved
               from the schedule endpoint.

        Returns:
           Dict containing game stats and season series data.
        """
        return self.client.get(resource=f"gamecenter/{game_id}/right-rail").json()

    def game_story(self, game_id: str) -> dict:
        """Gets game story information for a specific game.

        Args:
           game_id (str): ID of the game to retrieve story for. Game IDs can be retrieved
               from the schedule endpoint.

        Returns:
           Dict containing game story data.
        """
        return self.client.get(resource=f"wsc/game-story/{game_id}").json()
