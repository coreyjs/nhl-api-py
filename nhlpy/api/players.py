from nhlpy.api import BaseNHLAPIClient


class Players(BaseNHLAPIClient):
    def get_player(self, person_id: str) -> dict:
        """
        Returns a player based on the person_id.
        :param person_id:
        :return:
        """
        return self._get(resource=f"people/{person_id}").json()["people"]

    def get_player_stats(
        self, person_id: str, season: str = None, stat_type: str = "statsSingleSeason"
    ) -> dict:
        """
        This returns a players statistics based on the param stat_type: and season:  An example of this
        may be client.players.get_player_stats(stat_type="yearByYear", season="20202021").  In some instances season:
        does not matter, such as yearByYear.
        :param person_id: int - Player ID
        :param season: str - Season in format of 20202021
        :param stat_type: str - These can be accessed programmatically via get_player_stat_types()
            or are limited to the following yearByYear, yearByYearRank, yearByYearPlayoffs,
            yearByYearPlayoffsRank, careerRegularSeason, careerPlayoffs, gameLog, playoffGameLog,
            vsTeam, vsTeamPlayoffs, vsDivision, vsDivisionPlayoffs, vsConference, vsConferencePlayoffs,
            byMonth, byMonthPlayoffs, byDayOfWeek, byDayOfWeekPlayoffs, homeAndAway, homeAndAwayPlayoffs,
            winLoss, winLossPlayoffs, onPaceRegularSeason, regularSeasonStatRankings, playoffStatRankings,
            goalsByGameSituation, goalsByGameSituationPlayoffs, statsSingleSeason, statsSingleSeasonPlayoffs

        :return:
        """
        query = f"stats={stat_type}" if stat_type else ""
        return self._get(
            resource=f"people/{person_id}/stats?season={season}&{query}"
        ).json()["stats"]

    def get_player_stat_types(self) -> dict:
        """
        Returns the full list of stat(types) that can be used in get_player_stats()'s stat_type param
        :return:
        """
        return self._get(resource="statTypes").json()
