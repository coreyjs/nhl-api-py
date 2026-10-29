from typing import Dict, Any, Union

from nhlpy.http_client import Endpoint, HttpClient

RANKING_CATEGORIES = {
    1: "North American Skater",
    2: "International Skater",
    3: "North American Goalie",
    4: "International Goalie",
}
DRAFT_ROUNDS = (1, 2, 3, 4, 5, 6, 7)


class Draft:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    def rankings(self, year: str = None, category: int = 1) -> Dict[str, Any]:
        """Gets NHL Central Scouting draft prospect rankings.

        Args:
            year (str, optional): Draft year (e.g., "2025"). Defaults to the upcoming/most recent draft.
            category (int, optional): Ranking list. Only used when ``year`` is given; without a year the API
                always returns category 1. Defaults to 1.
                1: North American Skater
                2: International Skater
                3: North American Goalie
                4: International Goalie

        Returns:
            Dict[str, Any]: The ranking list plus the available draft years and categories.

        Key Response Fields:
            draftYear (int): Draft year of the rankings
            categoryId (int): Ranking category ID
            categories (list): All categories, each as {id, name, consumerKey}
            draftYears (list[int]): Draft years with rankings
            rankings (list): Ranked prospects
            rankings[].finalRank (int): Final ranking (``midtermRank`` for the midterm list)
            rankings[].firstName / lastName (str): Prospect name
            rankings[].lastAmateurClub / lastAmateurLeague (str): Current amateur team and league

        Raises:
            ValueError: If ``category`` is not 1-4

        Response Docs:
            docs/draft.md

        Example:
            client.draft.rankings()
            client.draft.rankings(year="2025", category=2)
        """
        if category not in RANKING_CATEGORIES:
            raise ValueError(f"Invalid category '{category}'. Valid values: {', '.join(map(str, RANKING_CATEGORIES))}")
        resource = "draft/rankings/now" if year is None else f"draft/rankings/{year}/{category}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def picks(self, year: str = None, draft_round: Union[int, str] = "all") -> Dict[str, Any]:
        """Gets the picks made in an NHL draft.

        Args:
            year (str, optional): Draft year (e.g., "2024"). Defaults to the current/most recent draft.
            draft_round (int | str, optional): Round 1-7, or "all" for every round. Only used when ``year`` is
                given; without a year the API returns its default round. Defaults to "all".

        Returns:
            Dict[str, Any]: Draft picks plus the available draft years and rounds.

        Key Response Fields:
            draftYear (int): Draft year
            state (str): Draft state (e.g., "over")
            selectableRounds (list[int]): Rounds available for this draft
            picks (list): Picks in order
            picks[].overallPick (int): Overall pick number
            picks[].round / pickInRound (int): Round and pick within the round
            picks[].teamAbbrev (str): Drafting team abbreviation
            picks[].firstName.default / lastName.default (str): Drafted player's name

        Raises:
            ValueError: If ``draft_round`` is not 1-7 or "all"

        Response Docs:
            docs/draft.md

        Example:
            client.draft.picks()
            client.draft.picks(year="2024", draft_round=1)
        """
        if str(draft_round) not in ("all", *map(str, DRAFT_ROUNDS)):
            raise ValueError(
                f"Invalid draft_round '{draft_round}'. Valid values: all, {', '.join(map(str, DRAFT_ROUNDS))}"
            )
        resource = "draft/picks/now" if year is None else f"draft/picks/{year}/{draft_round}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def tracker(self, year: str = None) -> Dict[str, Any]:
        """Gets the live draft tracker: the picks in the draft's current round.

        This backs the draft tracker widget on nhl.com. During a draft it follows the round in progress;
        once a draft is over it returns round 1. Use ``picks()`` for any round of a past draft.

        Args:
            year (str, optional): Draft year (e.g., "2025"). Defaults to the current/most recent draft.

        Returns:
            Dict[str, Any]: Tracker state and the current round's picks.

        Key Response Fields:
            currentDraftDate (str): Date of the draft day in progress, YYYY-MM-DD
            round (int): Round shown
            state (str): Draft state (e.g., "over")
            tvBroadcasts (list): Broadcasts of the draft
            picks (list): Picks in the round
            picks[].overallPick (int): Overall pick number
            picks[].teamAbbrev (str): Drafting team abbreviation
            picks[].firstName.default / lastName.default (str): Drafted player's name

        Response Docs:
            docs/draft.md

        Example:
            client.draft.tracker()
            client.draft.tracker(year="2025")
        """
        resource = "draft-tracker/picks/now" if year is None else f"draft-tracker/picks/{year}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()
