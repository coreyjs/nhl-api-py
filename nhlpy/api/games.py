import warnings
from typing import Union, List
from nhlpy.api import BaseNHLAPIClient


class Games(BaseNHLAPIClient):
    """
    This class is used to access the NHL API for game data.
    """

    def get_game_types(self) -> dict:
        """
        Returns a list of game types that can be used in other endpoints
        :return:
        """
        return self._get(resource="gameTypes").json()

    def get_game_play_types(self) -> dict:
        """
        Returns a list of play types that can be used in other endpoints
        :return:
        """
        return self._get(resource="playTypes").json()

    def get_game_status_codes(self) -> dict:
        """
        Returns a list of game status codes that can be used in other endpoints
             example:
                [{
                    "code": "1",
                    "abstractGameState": "Preview",
                    "detailedState": "Scheduled",
                    "baseballCode": "S",
                    "startTimeTBD": false
                }...]
        :return: dict
        """
        return self._get(resource="gameStatus").json()

    def get_game_live_feed(self, game_id: Union[str, int]) -> dict:
        """
        Returns a live feed for the game with the id supplied.  WARNING, this tends to be a large response.
        :param game_id: int, NHL game id,

            GameIDS are in the format {Season}{GameType}{GameNumber}.  For example, the first game of the 2020-2021 season
            would be 2020020001.  This is also the gamePk field that can be found in the team schedule endpoints.

            For playoffs the {GameNumber} portion will be formatted as RRMG where RR is the round (01, 02, 03, 04),
            M is the matchup and G is the game out of 7.  So 2022030412 is the 2022-2023 NHL season, 03 means playoffs
            04 means fourth round, 1 means matchup (I really cant 100% figure this out)
             and 2 is the second game out of 7

            {Season} is the first 4 digits of the season year, so for 20222023 it would be 2022.

            {GameType} are the following: 01=preseason, 02=regular season, 03=playoffs, 04=all-star.

            {GameNumber} is the game number in the season, starting at 0001.
        :return: dict
        """
        return self._get(resource=f"game/{game_id}/feed/live").json()

    def get_game_live_feed_diff_after_timestamp(
        self, game_id: Union[str, int], timestamp: str
    ) -> dict:
        """
        Returns the difference in the live feed game data, from since the given timestamp: param.
        :param game_id:
        :param timestamp:
        :return:
        """
        warnings.warn(
            "This endpoint is still experimental and may not work as expected"
        )
        return self._get(resource=f"game/{game_id}/feed/live/diffPath").json()

    def get_game_boxscore(self, game_id: Union[str, int]) -> List[dict]:
        """
        Less detail than get_game_live_feed() but still a large response, contains lots of information about
        the game.

        See documentation for get_game_live_feed() for more verbose explanation of game_id.
        :param game_id:
        :return:
        """
        return self._get(resource=f"game/{game_id}/boxscore").json()

    def get_game_linescore(self, game_id: Union[str, int]) -> dict:
        """
        Returns the linescore for the game with the id supplied.

        See documentation for get_game_live_feed() for more verbose explanation of game_id.

        :param game_id:
        :return:
        """
        return self._get(resource=f"game/{game_id}/linescore").json()

    def get_game_content(self, game_id: Union[str, int]) -> dict:
        """
        Returns the content for the game with the id supplied.  Can contain links to videos, goals, shots,
        headlines, description, etc.  A very large response payload.

        See documentation for get_game_live_feed() for more verbose explanation of game_id.

        :param game_id:
        :return:
        """
        return self._get(resource=f"game/{game_id}/content").json()
