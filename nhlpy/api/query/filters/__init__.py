from abc import ABC, abstractmethod
from typing import Union, List


class QueryBase(ABC):
    @abstractmethod
    def to_query(self) -> str:
        pass

    @abstractmethod
    def validate(self) -> Union[bool, None]:
        return True


def _goalie_stats_sorts(report: str) -> List[dict]:
    """
    This is default criteria for sorting on goalie stats.  I hate this method
    :param report:
    :return:
    """
    if report == "summary":
        return [
            {"property": "wins", "direction": "DESC"},
            {"property": "gamesPlayed", "direction": "ASC"},
            {"property": "playerId", "direction": "ASC"},
        ]
    elif report == "advanced":
        return [
            {"property": "qualityStart", "direction": "DESC"},
            {"property": "goalsAgainstAverage", "direction": "ASC"},
            {"property": "playerId", "direction": "ASC"},
        ]
    elif report == "bios":
        return [
            {"property": "lastName", "direction": "ASC_CI"},
            {"property": "goalieFullName", "direction": "ASC_CI"},
            {"property": "playerId", "direction": "ASC"},
        ]
    elif report == "daysrest":
        return [
            {"property": "wins", "direction": "DESC"},
            {"property": "savePct", "direction": "DESC"},
            {"property": "playerId", "direction": "ASC"},
        ]
    elif report == "penaltyShots":
        return [
            {"property": "penaltyShotsSaves", "direction": "DESC"},
            {"property": "penaltyShotSavePct", "direction": "DESC"},
            {"property": "playerId", "direction": "ASC"},
        ]
    elif report == "savesByStrength":
        return [
            {"property": "wins", "direction": "DESC"},
            {"property": "savePct", "direction": "DESC"},
            {"property": "playerId", "direction": "ASC"},
        ]
    elif report == "shootout":
        return [
            {"property": "shootoutWins", "direction": "DESC"},
            {"property": "shootoutSavePct", "direction": "DESC"},
            {"property": "playerId", "direction": "ASC"},
        ]
    elif report == "startedVsRelieved":
        return [
            {"property": "gamesStarted", "direction": "DESC"},
            {"property": "gamesStartedSavePct", "direction": "DESC"},
            {"property": "playerId", "direction": "ASC"},
        ]
    else:
        return [{}]
