import logging
from typing import List

logger = logging.getLogger(__name__)

skater_summary_default_sorting = [
    {"property": "points", "direction": "DESC"},
    {"property": "gamesPlayed", "direction": "ASC"},
    {"property": "playerId", "direction": "ASC"},
]

skater_bios_default_sorting = [
    {"property": "lastName", "direction": "ASC_CI"},
    {"property": "skaterFullName", "direction": "ASC_CI"},
    {"property": "playerId", "direction": "ASC"},
]

faceoffs_default_sorting = [
    {"property": "totalFaceoffs", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

faceoff_wins_default_sorting = [
    {"property": "totalFaceoffWins", "direction": "DESC"},
    {"property": "faceoffWinPct", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

goalsForAgainst_default_sorting = [
    {"property": "evenStrengthGoalDifference", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]


realtime_default_sorting = [{"property": "hits", "direction": "DESC"}, {"property": "playerId", "direction": "ASC"}]

penalties_default_sorting = [
    {"property": "penaltyMinutes", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

penaltyKill_default_sorting = [
    {"property": "shTimeOnIce", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

penalty_shot_default_sorting = [
    {"property": "penaltyShotsGoals", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

powerplay_default_sorting = [
    {"property": "ppTimeOnIce", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

puckposs_default_sorting = [{"property": "satPct", "direction": "DESC"}, {"property": "playerId", "direction": "ASC"}]

summary_shooting_default_sorting = [
    {"property": "satTotal", "direction": "DESC"},
    {"property": "usatTotal", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

percentages_default_sorting = [
    {"property": "satPercentage", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

scoringratesdefault_sorting = [
    {"property": "pointsPer605v5", "direction": "DESC"},
    {"property": "goalsPer605v5", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

scoring_per_game_default_sorting = [
    {"property": "pointsPerGame", "direction": "DESC"},
    {"property": "goalsPerGame", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

shootout_default_scoring = [
    {"property": "shootoutGoals", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]

shottype_default_sorting = [
    {"property": "shootingPct", "direction": "DESC"},
    {"property": "shootingPctBat", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]


time_on_ice_default_sorting = [
    {"property": "timeOnIce", "direction": "DESC"},
    {"property": "playerId", "direction": "ASC"},
]


class SortingOptions:
    @staticmethod
    def get_default_sorting_for_report(report: str) -> List[dict]:
        """
        I know this us ugly.  But hopefully its out of sight out of mind.
        :param report:
        :return:
        """
        if report == "summary":
            return skater_summary_default_sorting
        elif report == "bios":
            return skater_bios_default_sorting
        elif report == "faceoffpercentages":
            return faceoffs_default_sorting
        elif report == "faceoffwins":
            return faceoff_wins_default_sorting
        elif report == "goalsForAgainst":
            return goalsForAgainst_default_sorting
        elif report == "realtime":
            return realtime_default_sorting
        elif report == "penalties":
            return penalties_default_sorting
        elif report == "penaltykill":
            return penaltyKill_default_sorting
        elif report == "penaltyShots":
            return penalty_shot_default_sorting
        elif report == "powerplay":
            return powerplay_default_sorting
        elif report == "puckPossessions":
            return puckposs_default_sorting
        elif report == "summaryshooting":
            return summary_shooting_default_sorting
        elif report == "percentages":
            return percentages_default_sorting
        elif report == "scoringRates":
            return scoringratesdefault_sorting
        elif report == "scoringpergame":
            return scoring_per_game_default_sorting
        elif report == "shootout":
            return shootout_default_scoring
        elif report == "shottype":
            return shottype_default_sorting
        elif report == "timeonice":
            return time_on_ice_default_sorting
        else:
            logger.info("No default sort criteria setup for this report type, defaulting to skater summary")
            return skater_summary_default_sorting
