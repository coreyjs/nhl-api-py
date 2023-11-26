import importlib.resources

from typing import List, Optional


class Standings:
    def __init__(self, http_client):
        self.client = http_client

    def get_standings(self, date: Optional[str] = None, season: Optional[str] = None, cache=True) -> dict:
        """
        Gets the standings for the season supplied via season: param.
        :param date: str, Date in format YYYY-MM-DD.  If no date is supplied, it will default to "Today".
        :param season: The season to return the final standings from.  This takes precedence over date.
        :param cache: bool, Load from hard file of data instead of making api call.  Possible the cache gets out
            of date if I dont update this yearly.
        :return: dict
        """

        # We need to look up the last date of the season and use that as the date, since it doesnt seem to take
        # season as a param.
        if season:
            if cache:
                # load json from data/seasonal_information_manifest.json
                import json

                data_resource = importlib.resources.files("nhlpy") / "data"
                seasons = json.loads((data_resource / "seasonal_information_manifest.json").read_text())["seasons"]
            else:
                seasons = self.season_standing_manifest()

            season_data = next((s for s in seasons if s["id"] == int(season)), None)
            if not season_data:
                raise ValueError(f"Invalid Season Id {season}")
            date = season_data["standingsEnd"]

        res = date if date else "now"

        return self.client.get(resource=f"standings/{res}").json()

    def season_standing_manifest(self) -> List[dict]:
        """
        Returns information about what seems like every season.  Start date, end date, etc.

        :example
            [{
                        "id": 20232024,
                        "conferencesInUse": true,
                        "divisionsInUse": true,
                        "pointForOTlossInUse": true,
                        "regulationWinsInUse": true,
                        "rowInUse": true,
                        "standingsEnd": "2023-11-10",
                        "standingsStart": "2023-10-10",
                        "tiesInUse": false,
                        "wildcardInUse": true
                }]

        :return: dict
        """

        return self.client.get(resource="standings-season").json()["seasons"]
