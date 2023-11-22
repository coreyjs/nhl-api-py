from nhlpy.http_client import HttpClient


class GameCenter:
    def __init__(self, http_client: HttpClient):
        self.client = http_client

    def boxscore(self, game_id: str) -> dict:
        """
        Get the boxscore for the game_id.  GameIds can be retrieved from the schedule endpoint.
        :param game_id: The game_id for the game you want the boxscore for.

        :example
            https://api-web.nhle.com/v1/gamecenter/2023020280/boxscore
        :return: dict
        """
        return self.client.get(resource=f"gamecenter/{game_id}/boxscore").json()

    def play_by_play(self, game_id: str) -> dict:
        """
        Get the play by play for the game_id.  GameIds can be retrieved from the schedule endpoint.
        :param game_id: The game_id for the game you want the play by play for.
        :return: dict
        """
        return self.client.get(resource=f"gamecenter/{game_id}/play-by-play").json()

    def landing(self, game_id: str) -> dict:
        """
        Get verbose information about the matchup for the given game.

        GameIds can be retrieved from the schedule endpoint.
        :param game_id: The game_id for the game you want the landing page for.
        :return: dict
        """
        return self.client.get(resource=f"gamecenter/{game_id}/landing").json()

    def score_now(self) -> dict:
        """
        Get the current score of all games in progress.  I think, not totally sure.
        :return: dict
        """
        return self.client.get(resource="score/now").json()
