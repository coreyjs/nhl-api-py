from typing import List

from nhlpy.api.standings import Standings


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
