from typing import List, Optional

from nhlpy.http_client import Endpoint


class Standings:
    def __init__(self, http_client):
        self.client = http_client

    def league_standings(self, date: Optional[str] = None, season: Optional[str] = None) -> dict:
        """Gets NHL league standings for a specific date or season.

        Retrieves the full league standings snapshot.  When ``season`` is
        provided, the method resolves the last day of that season via
        ``season_standing_manifest()`` and uses it as the date.  If both
        ``date`` and ``season`` are supplied, ``season`` takes precedence.
        Passing neither returns today's standings.

        Args:
            date (str, optional): Date in YYYY-MM-DD format.
                Defaults to the current date when neither param is provided.
            season (str, optional): Season identifier (e.g., "20232024").
                Overrides ``date`` -- the final standings date for the season
                is looked up automatically.

        Returns:
            dict: Standings response with the following key fields:

                - ``wildCardIndicator`` (bool): Whether the wild-card format
                  is in effect for this snapshot.
                - ``standings`` (list[dict]): List of 32 team standing entries.
                  Each entry contains:

                  - ``teamName`` (dict): ``{"default": "..."}`` team name.
                  - ``teamAbbrev`` (dict): ``{"default": "..."}`` abbreviation.
                  - ``points`` (int): Total standings points.
                  - ``wins`` (int): Wins.
                  - ``losses`` (int): Losses.
                  - ``otLosses`` (int): Overtime losses.
                  - ``gamesPlayed`` (int): Games played.
                  - ``conferenceSequence`` (int): Rank within conference.
                  - ``divisionSequence`` (int): Rank within division.

        Raises:
            ValueError: If the provided ``season`` is not found in the
                season standing manifest.

        See Also:
            https://api-web.nhle.com/v1/standings/{date}
        """

        # We need to look up the last date of the season and use that as the date, since it doesnt seem to take
        # season as a param.
        if season:
            seasons = self.season_standing_manifest()

            season_data = next((s for s in seasons if s.get("id") == int(season)), None)
            if not season_data:
                raise ValueError(f"Invalid Season Id {season}")
            date = season_data.get("standingsEnd")

        res = date if date else "now"

        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=f"standings/{res}").json()

    def season_standing_manifest(self) -> List[dict]:
        """Gets metadata for every historical NHL season.

        Returns a list of all seasons with their date ranges, structural
        flags (conferences, divisions, ties), and scoring-rule indicators.
        Used internally by ``league_standings()`` to resolve a season to its
        final standings date.

        Returns:
            List[dict]: List of season metadata dicts. Each entry contains:

                - ``id`` (int): Season identifier (e.g., 20232024).
                - ``conferencesInUse`` (bool): Whether conferences were active.
                - ``divisionsInUse`` (bool): Whether divisions were active.
                - ``pointForOTlossInUse`` (bool): OT-loss point rule in effect.
                - ``regulationWinsInUse`` (bool): Regulation-wins tiebreaker.
                - ``rowInUse`` (bool): ROW (regulation + overtime wins) in use.
                - ``standingsEnd`` (str): Last date of the standings period
                  (YYYY-MM-DD).
                - ``standingsStart`` (str): First date of the standings period
                  (YYYY-MM-DD).
                - ``tiesInUse`` (bool): Whether ties were possible.
                - ``wildcardInUse`` (bool): Wild-card playoff format in effect.

        See Also:
            https://api-web.nhle.com/v1/standings-season
        """
        response = self.client.get(endpoint=Endpoint.API_WEB_V1, resource="standings-season").json()
        return response.get("seasons", [])
