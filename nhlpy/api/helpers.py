import warnings
from typing import List, Optional

from nhlpy.api.standings import Standings
from nhlpy.api.schedule import Schedule
from nhlpy.api.games import Games


def _parse_team_specific_game_data(
    game_item: dict, team_side: str, game_boxscore_data: dict
) -> None:
    """
    Parser helper method
    :param team_side:
    :param game_boxscore_data:
    :return:
    """
    game_item[f"{team_side}_pim"] = game_boxscore_data[team_side]["teamStats"][
        "teamSkaterStats"
    ]["pim"]
    game_item[f"{team_side}_shots"] = game_boxscore_data[team_side]["teamStats"][
        "teamSkaterStats"
    ]["shots"]
    game_item[f"{team_side}_pp_percent"] = float(
        game_boxscore_data[team_side]["teamStats"]["teamSkaterStats"][
            "powerPlayPercentage"
        ]
    )
    game_item[f"{team_side}_pp_goals"] = game_boxscore_data[team_side]["teamStats"][
        "teamSkaterStats"
    ]["powerPlayGoals"]
    game_item[f"{team_side}_pp_opps"] = game_boxscore_data[team_side]["teamStats"][
        "teamSkaterStats"
    ]["powerPlayOpportunities"]
    game_item[f"{team_side}_fo_win_percent"] = float(
        game_boxscore_data[team_side]["teamStats"]["teamSkaterStats"][
            "faceOffWinPercentage"
        ]
    )
    game_item[f"{team_side}_shots_blocked"] = game_boxscore_data[team_side][
        "teamStats"
    ]["teamSkaterStats"]["blocked"]
    game_item[f"{team_side}_shots_takeaways"] = game_boxscore_data[team_side][
        "teamStats"
    ]["teamSkaterStats"]["takeaways"]
    game_item[f"{team_side}_shots_giveaways"] = game_boxscore_data[team_side][
        "teamStats"
    ]["teamSkaterStats"]["giveaways"]
    game_item[f"{team_side}_shots_hits"] = game_boxscore_data[team_side]["teamStats"][
        "teamSkaterStats"
    ]["hits"]


class Helpers:
    def pythagorean_expectation(
        self, goals_for: int, goals_against: int, exponent: float = 2.37
    ):
        """
        Calculates the pythagorean expectation for a team based on the goals for and goals against.
        :param goals_for:
        :param goals_against:
        :param exponent:
        :return:
        """
        return goals_for**exponent / (
            goals_for**exponent + goals_against**exponent
        )

    def league_standings(self, season: str, py_exp_ex: float = 2.37) -> List[dict]:
        """
        Returns a list of all games for the current season if no season is supplied.  Otherwise, returns the
        schedule for the season defined in the season: param.

        This is useful when you want to create a pandas Dataframe of the team standings for that season.
        This returns an array, instead of a DF to avoid the need to import pandas in this module.
        :param py_exp_ex: Exponent used in the calculation of the pythagorean expectation for each team.  Defaults
            to 2.37.
        :param season: Season in format of 20202021
        :return:
        """
        schedule_data: dict = Standings().get_standings(
            season=season, detailed_record=True
        )
        records = schedule_data["records"]
        teams = []
        for division in records:
            for team in division["teamRecords"]:
                team = {
                    "division_name": division["division"]["name"],
                    "division_id": division["division"]["id"],
                    "team_name": team["team"]["name"],
                    "team_id": team["team"]["id"],
                    "wins": team["leagueRecord"]["wins"],
                    "ot_loss": team["leagueRecord"]["ot"],
                    "losses": team["leagueRecord"]["losses"],
                    "regulation_wins": team["regulationWins"],
                    "goals_against": team["goalsAgainst"],
                    "goals_scored": team["goalsScored"],
                    "points": team["points"],
                    "games_played": team["gamesPlayed"],
                    "league_rank": team["leagueRank"],
                    "division_rank": team["divisionRank"],
                }
                team["win_pct"] = team["wins"] / team["games_played"]
                team["point_pct"] = team["points"] / (team["games_played"] * 2)
                team["py_expectation"] = self.pythagorean_expectation(
                    team["goals_scored"], team["goals_against"], exponent=py_exp_ex
                )
                team["expected_wins"] = team["py_expectation"] * team["games_played"]
                teams.append(team)
        return teams

    def get_all_game_results(
        self,
        season: str,
        detailed_game_data: bool = False,
        game_type: str = "R",
        team_ids: Optional[List[int]] = None,
    ) -> List[dict]:
        """

        :param season:
        :param detailed_game_data: If True, will return the full game data for each game.  If False, will only return simple game data.
        :param game_type:
        :param team_ids:
        :return:
        """
        warnings.warn(
            "This endpoint will query the schedule API to get the games, and then sequentially query the boxscore API"
            " for each game.  This is a slow endpoint, do not call this while in a loop, or multiple times in succession"
        )
        games = []
        game_dates = Schedule().get_schedule(
            season=season, game_type=game_type, team_ids=team_ids
        )["dates"]
        for d in game_dates:
            date = d["date"]
            for game in d["games"]:
                game_data = {
                    "date": date,
                    "home_score": game["teams"]["home"]["score"],
                    "away_score": game["teams"]["away"]["score"],
                    "game_id": game["gamePk"],
                    "game_type": game["gameType"],
                    "away_id": game["teams"]["away"]["team"]["id"],
                    "away_name": game["teams"]["away"]["team"]["name"],
                    "home_id": game["teams"]["home"]["team"]["id"],
                    "home_name": game["teams"]["home"]["team"]["name"],
                }
                games.append(game_data)

        if detailed_game_data:
            game_client = Games()
            for game in games:
                data = game_client.get_game_boxscore(game_id=game["game_id"])["teams"]
                _parse_team_specific_game_data(
                    game_item=game, team_side="away", game_boxscore_data=data
                )
                _parse_team_specific_game_data(
                    game_item=game, team_side="home", game_boxscore_data=data
                )

        return games
