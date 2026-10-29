from typing import Dict, Any, List, Optional, Sequence

from nhlpy.http_client import HttpClient, Endpoint

# Allowed values for the top-10 leaderboard endpoints, taken from nhl.com's EDGE pages.
# The API answers an unknown sort with a 404 and an unknown position group with an empty list,
# so these are validated before any request is made.
POSITION_GROUPS = ("all", "forwards", "defense")
STRENGTHS = ("all", "es", "pp", "pk")
SHOT_SPEED_SORTS = ("max", "over-100", "90-99", "80-89", "70-79")
SKATING_SPEED_SORTS = ("max", "over-22", "20-22", "18-20")
SKATING_DISTANCE_SORTS = ("total", "per-60", "max-game", "max-period")
ZONE_TIME_SORTS = ("offensive", "neutral", "defensive")
SHOT_LOCATION_AREAS = ("all", "high", "mid", "long")
SHOT_LOCATION_CATEGORIES = ("sog", "goals", "shooting-pctg")
GOALIE_SHOT_LOCATION_CATEGORIES = ("save-pctg", "saves", "goals-against", "shots-against")
GOALIE_5V5_SORTS = ("save-pctg", "save-pctg-close", "shots", "shots-per-60")
GOALIE_SAVE_PCTG_SORTS = ("pctg", "games")


def _check(name: str, value: str, allowed: Sequence[str]) -> str:
    if value not in allowed:
        raise ValueError(f"Invalid {name} '{value}'. Valid values: {', '.join(allowed)}")
    return value


def _with_period(resource: str, season: Optional[str], game_type: int) -> str:
    """Appends ``/now`` or ``/{season}/{game_type}`` to an EDGE resource path."""
    return f"{resource}/now" if season is None else f"{resource}/{season}/{game_type}"


class Edge:
    def __init__(self, http_client: HttpClient) -> None:
        self.client = http_client

    # ========================
    # SKATER ENDPOINTS
    # ========================

    def skater_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE skater detail statistics for a specific player.

        Retrieves detailed EDGE statistics including shot speed, skating speed, distance traveled,
        and zone time data for a skater.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024). Defaults to current season.
            game_type (int, optional): Type of games (defaults to 2):
                2: Regular season
                3: Playoffs

        Returns:
            dict: Dictionary containing detailed EDGE statistics for the skater

        Key Response Fields:
            player.firstName.default (str): Player first name
            player.lastName.default (str): Player last name
            player.goals (int): Total goals scored
            player.points (int): Total points
            topShotSpeed.imperial (float): Top shot speed in mph
            skatingSpeed.speedMax.imperial (float): Maximum skating speed in mph
            totalDistanceSkated.imperial (float): Total distance skated in miles
            zoneTimeDetails.offensiveZonePctg (float): Offensive zone time percentage

        Response Docs:
            docs/edge.md

        Example:
            client.edge.skater_detail(player_id=8478402)
            client.edge.skater_detail(player_id=8478402, season=20232024, game_type=2)
        """
        if season is None:
            resource = f"edge/skater-detail/{player_id}/now"
        else:
            resource = f"edge/skater-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def skater_shot_speed_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE shot speed details for a specific skater.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Shot speed statistics including maximum and average speeds

        Key Response Fields:
            shotSpeedData (list): Shot speed entries with percentiles
            topShotSpeed.imperial (float): Top shot speed in mph
            averageShotSpeed.imperial (float): Average shot speed in mph

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/skater-shot-speed-detail/{player_id}/now"
        else:
            resource = f"edge/skater-shot-speed-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def skater_skating_speed_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE skating speed details for a specific skater.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Skating speed statistics including burst speed and average speed

        Key Response Fields:
            skatingSpeedData (list): Skating speed entries with burst counts
            speedMax.imperial (float): Maximum skating speed in mph
            burstCount (int): Number of speed bursts

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/skater-skating-speed-detail/{player_id}/now"
        else:
            resource = f"edge/skater-skating-speed-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def skater_shot_location_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE shot location details for a specific skater.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Shot location data including shooting patterns and heat maps

        Key Response Fields:
            shotLocations (list): Shot data grouped by area
            area (str): Ice zone identifier
            shotCount (int): Number of shots from each area

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/skater-shot-location-detail/{player_id}/now"
        else:
            resource = f"edge/skater-shot-location-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def skater_skating_distance_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE skating distance details for a specific skater.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Distance traveled statistics per game and per shift

        Key Response Fields:
            distanceData (list): Distance entries per game
            totalDistance.imperial (float): Total distance skated in miles
            gameMax.imperial (float): Maximum distance skated in a single game in miles

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/skater-skating-distance-detail/{player_id}/now"
        else:
            resource = f"edge/skater-skating-distance-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def skater_comparison(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE comparison statistics for a specific skater.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Comparison data relative to league averages

        Key Response Fields:
            comparisonData (list): Comparison metrics vs league
            leagueAverage (float): League average value for each metric
            playerValue (float): Player value for each metric

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/skater-comparison/{player_id}/now"
        else:
            resource = f"edge/skater-comparison/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def skater_zone_time(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE zone time details for a specific skater.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Time spent in offensive, defensive, and neutral zones

        Key Response Fields:
            offensiveZonePctg (float): Offensive zone time percentage
            defensiveZonePctg (float): Defensive zone time percentage
            neutralZonePctg (float): Neutral zone time percentage

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/skater-zone-time/{player_id}/now"
        else:
            resource = f"edge/skater-zone-time/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def skater_landing(self, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE skater landing page data.

        Retrieves league-wide skater EDGE statistics overview.

        Args:
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Overview of league-wide skater EDGE statistics

        Key Response Fields:
            leaders.hardestShot (list): League leaders for hardest shot
            leaders.maxSkatingSpeed (list): League leaders for max skating speed
            leaders.totalDistanceSkated (list): League leaders for total distance skated

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = "edge/skater-landing/now"
        else:
            resource = f"edge/skater-landing/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def cat_skater_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL CAT (Catch All Tracking) EDGE skater details.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: CAT EDGE statistics for the skater

        Key Response Fields:
            player (dict): Compact player summary with EDGE highlights
            shotSpeed (dict): Condensed shot speed data
            skatingSpeed (dict): Condensed skating speed data

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"cat/edge/skater-detail/{player_id}/now"
        else:
            resource = f"cat/edge/skater-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def skater_skating_speed_top_10(
        self, position_group: str = "all", sort: str = "max", season: str = None, game_type: int = 2
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 skaters by NHL EDGE skating speed.

        Args:
            position_group (str, optional): "all", "forwards" or "defense". Defaults to "all".
            sort (str, optional): "max" (top speed), or speed-burst counts "over-22", "20-22", "18-20" (mph).
                Defaults to "max".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten skaters, ranked by ``sort``

        Key Response Fields:
            player.firstName.default (str): Player first name
            player.lastName.default (str): Player last name
            player.team.abbrev (str): Player's team abbreviation
            maxSpeed.imperial (float): Top skating speed in mph (``metric`` for km/h)
            maxSpeed.overlay (dict): The game the top speed happened in
            burstsOver22 (int): Bursts over 22 mph
            bursts20To22 (int): Bursts between 20 and 22 mph
            bursts18To20 (int): Bursts between 18 and 20 mph

        Raises:
            ValueError: If ``position_group`` or ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.skater_skating_speed_top_10()
            client.edge.skater_skating_speed_top_10(position_group="defense", sort="over-22", season="20242025")
        """
        resource = (
            f"edge/skater-speed-top-10/{_check('position_group', position_group, POSITION_GROUPS)}"
            f"/{_check('sort', sort, SKATING_SPEED_SORTS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def skater_shot_speed_top_10(
        self, position_group: str = "all", sort: str = "max", season: str = None, game_type: int = 2
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 skaters by NHL EDGE shot speed.

        Args:
            position_group (str, optional): "all", "forwards" or "defense". Defaults to "all".
            sort (str, optional): "max" (hardest shot), or shot-attempt counts "over-100", "90-99", "80-89",
                "70-79" (mph). Defaults to "max".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten skaters, ranked by ``sort``

        Key Response Fields:
            player.firstName.default (str): Player first name
            player.lastName.default (str): Player last name
            player.team.abbrev (str): Player's team abbreviation
            hardestShot.imperial (float): Hardest shot in mph (``metric`` for km/h)
            hardestShot.overlay (dict): The game the hardest shot happened in
            shotAttemptsOver100 (int): Shot attempts over 100 mph
            shotAttempts90To100 (int): Shot attempts between 90 and 100 mph
            shotAttempts80To90 (int): Shot attempts between 80 and 90 mph

        Raises:
            ValueError: If ``position_group`` or ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.skater_shot_speed_top_10()
            client.edge.skater_shot_speed_top_10(position_group="forwards", sort="over-100")
        """
        resource = (
            f"edge/skater-shot-speed-top-10/{_check('position_group', position_group, POSITION_GROUPS)}"
            f"/{_check('sort', sort, SHOT_SPEED_SORTS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def skater_skating_distance_top_10(
        self,
        position_group: str = "all",
        strength: str = "all",
        sort: str = "total",
        season: str = None,
        game_type: int = 2,
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 skaters by NHL EDGE distance skated.

        Args:
            position_group (str, optional): "all", "forwards" or "defense". Defaults to "all".
            strength (str, optional): "all", "es" (even strength), "pp" (power play) or "pk" (penalty kill).
                Defaults to "all".
            sort (str, optional): "total", "per-60", "max-game" or "max-period". Defaults to "total".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten skaters, ranked by ``sort``

        Key Response Fields:
            player.firstName.default (str): Player first name
            player.lastName.default (str): Player last name
            player.team.abbrev (str): Player's team abbreviation
            distanceTotal.imperial (float): Total distance skated in miles (``metric`` for km)
            distancePer60.imperial (float): Distance per 60 minutes in miles
            distanceMaxPerGame.imperial (float): Most distance in a single game, with ``overlay`` game info
            distanceMaxPerPeriod.imperial (float): Most distance in a single period, with ``overlay`` game info

        Raises:
            ValueError: If ``position_group``, ``strength`` or ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.skater_skating_distance_top_10()
            client.edge.skater_skating_distance_top_10(position_group="defense", strength="pk", sort="per-60")
        """
        resource = (
            f"edge/skater-distance-top-10/{_check('position_group', position_group, POSITION_GROUPS)}"
            f"/{_check('strength', strength, STRENGTHS)}/{_check('sort', sort, SKATING_DISTANCE_SORTS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def skater_zone_time_top_10(
        self,
        position_group: str = "all",
        strength: str = "all",
        sort: str = "offensive",
        season: str = None,
        game_type: int = 2,
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 skaters by NHL EDGE zone time percentage.

        Args:
            position_group (str, optional): "all", "forwards" or "defense". Defaults to "all".
            strength (str, optional): "all", "es" (even strength), "pp" (power play) or "pk" (penalty kill).
                Defaults to "all".
            sort (str, optional): "offensive", "neutral" or "defensive". Defaults to "offensive".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten skaters, ranked by ``sort``

        Key Response Fields:
            player.firstName.default (str): Player first name
            player.lastName.default (str): Player last name
            player.team.abbrev (str): Player's team abbreviation
            offensiveZoneTime (float): Share of time in the offensive zone (0-1)
            neutralZoneTime (float): Share of time in the neutral zone (0-1)
            defensiveZoneTime (float): Share of time in the defensive zone (0-1)

        Raises:
            ValueError: If ``position_group``, ``strength`` or ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.skater_zone_time_top_10()
            client.edge.skater_zone_time_top_10(position_group="forwards", strength="es", sort="defensive")
        """
        resource = (
            f"edge/skater-zone-time-top-10/{_check('position_group', position_group, POSITION_GROUPS)}"
            f"/{_check('strength', strength, STRENGTHS)}/{_check('sort', sort, ZONE_TIME_SORTS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def skater_shot_location_top_10(
        self,
        position_group: str = "all",
        category: str = "sog",
        area: str = "all",
        season: str = None,
        game_type: int = 2,
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 skaters by NHL EDGE shot location stats.

        Args:
            position_group (str, optional): "all", "forwards" or "defense". Defaults to "all".
            category (str, optional): Stat to rank by: "sog" (shots on goal), "goals" or "shooting-pctg".
                Defaults to "sog".
            area (str, optional): Rink area to rank by: "all", "high" (high danger), "mid" (mid range) or
                "long" (long range). Defaults to "all".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten skaters, ranked by ``category`` in ``area``

        Key Response Fields:
            player.firstName.default (str): Player first name
            player.lastName.default (str): Player last name
            player.team.abbrev (str): Player's team abbreviation
            all (int | float): ``category`` value from all areas
            highDanger (int | float): ``category`` value from high-danger areas
            midRange (int | float): ``category`` value from mid range
            longRange (int | float): ``category`` value from long range

        Raises:
            ValueError: If ``position_group``, ``category`` or ``area`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.skater_shot_location_top_10()
            client.edge.skater_shot_location_top_10(category="goals", area="high")
        """
        resource = (
            f"edge/skater-shot-location-top-10/{_check('position_group', position_group, POSITION_GROUPS)}"
            f"/{_check('category', category, SHOT_LOCATION_CATEGORIES)}/{_check('area', area, SHOT_LOCATION_AREAS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    # ========================
    # GOALIE ENDPOINTS
    # ========================

    def goalie_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE goalie detail statistics for a specific player.

        Retrieves detailed EDGE statistics including save percentages, shot location data,
        and 5v5 performance metrics for a goalie.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024). Defaults to current season.
            game_type (int, optional): Type of games (defaults to 2):
                2: Regular season
                3: Playoffs

        Returns:
            dict: Dictionary containing detailed EDGE statistics for the goalie

        Key Response Fields:
            player.wins (int): Total wins
            player.savePctg (float): Overall save percentage
            stats.goalsAgainstAvg.value (float): Goals against average
            stats.gamesAbove900.value (float): Games with save pct above .900
            shotLocationSummary (list): Save data grouped by shot area

        Response Docs:
            docs/edge.md

        Example:
            client.edge.goalie_detail(player_id=8476945)
            client.edge.goalie_detail(player_id=8476945, season=20232024, game_type=2)
        """
        if season is None:
            resource = f"edge/goalie-detail/{player_id}/now"
        else:
            resource = f"edge/goalie-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def goalie_shot_location_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE shot location details for a specific goalie.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Shot location data faced by the goalie including save percentages by zone

        Key Response Fields:
            shotLocations (list): Save data grouped by shot location
            area (str): Ice zone identifier
            savePctg (float): Save percentage for each area

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/goalie-shot-location-detail/{player_id}/now"
        else:
            resource = f"edge/goalie-shot-location-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def goalie_5v5_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE 5v5 performance details for a specific goalie.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: 5-on-5 performance statistics and save percentages

        Key Response Fields:
            fiveOnFiveStats (dict): 5-on-5 performance metrics
            savePctg5v5 (float): Save percentage at 5-on-5
            goalsAgainstAvg5v5 (float): Goals against average at 5-on-5

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/goalie-5v5-detail/{player_id}/now"
        else:
            resource = f"edge/goalie-5v5-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def goalie_comparison(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE comparison statistics for a specific goalie.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Comparison data relative to league averages

        Key Response Fields:
            comparisonData (list): Comparison metrics vs league
            leagueAverage (float): League average value for each metric
            playerValue (float): Player value for each metric

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/goalie-comparison/{player_id}/now"
        else:
            resource = f"edge/goalie-comparison/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def goalie_save_percentage_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE save percentage details for a specific goalie.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Detailed save percentage breakdowns by situation and location

        Key Response Fields:
            savePctgBreakdown (list): Save percentage by situation type
            overallSavePctg (float): Overall save percentage
            highDangerSavePctg (float): Save percentage on high-danger chances

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/goalie-save-percentage-detail/{player_id}/now"
        else:
            resource = f"edge/goalie-save-percentage-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def goalie_landing(self, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE goalie landing page data.

        Retrieves league-wide goalie EDGE statistics overview.

        Args:
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Overview of league-wide goalie EDGE statistics

        Key Response Fields:
            leaders (dict): League leaders for goalie EDGE stats
            topSavePctg (list): Leaders by save percentage
            topGamesAbove900 (list): Leaders by games above .900

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = "edge/goalie-landing/now"
        else:
            resource = f"edge/goalie-landing/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def cat_goalie_detail(self, player_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL CAT (Catch All Tracking) EDGE goalie details.

        Args:
            player_id (str): The unique identifier for the NHL player
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: CAT EDGE statistics for the goalie

        Key Response Fields:
            player (dict): Compact goalie summary with EDGE highlights
            savePctg (float): Condensed save percentage data
            goalsAgainstAvg (float): Condensed goals against average

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"cat/edge/goalie-detail/{player_id}/now"
        else:
            resource = f"cat/edge/goalie-detail/{player_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def goalie_5v5_top_10(self, sort: str = "save-pctg", season: str = None, game_type: int = 2) -> List[Dict[str, Any]]:
        """Get the league's top 10 goalies by NHL EDGE 5-on-5 stats.

        Args:
            sort (str, optional): "save-pctg", "save-pctg-close" (close-game save %), "shots" or "shots-per-60".
                Defaults to "save-pctg".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten goalies, ranked by ``sort``

        Key Response Fields:
            player.firstName.default (str): Goalie first name
            player.lastName.default (str): Goalie last name
            player.team.abbrev (str): Goalie's team abbreviation
            savePctg (float): 5-on-5 save percentage
            savePctgClose (float): 5-on-5 save percentage in close games
            shots (int): 5-on-5 shots faced
            shotsPer60 (float): 5-on-5 shots faced per 60 minutes

        Raises:
            ValueError: If ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.goalie_5v5_top_10()
            client.edge.goalie_5v5_top_10(sort="shots-per-60", season="20242025")
        """
        resource = f"edge/goalie-5v5-top-10/{_check('sort', sort, GOALIE_5V5_SORTS)}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def goalie_save_percentage_top_10(
        self, sort: str = "pctg", season: str = None, game_type: int = 2
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 goalies by games with a .900+ save percentage.

        Args:
            sort (str, optional): "pctg" (share of games over .900) or "games" (number of games over .900).
                Defaults to "pctg".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten goalies, ranked by ``sort``

        Key Response Fields:
            player.firstName.default (str): Goalie first name
            player.lastName.default (str): Goalie last name
            player.team.abbrev (str): Goalie's team abbreviation
            gamesOver900 (int): Games with a save percentage over .900
            pctgGamesOver900 (float): Share of games with a save percentage over .900

        Raises:
            ValueError: If ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.goalie_save_percentage_top_10()
            client.edge.goalie_save_percentage_top_10(sort="games")
        """
        resource = f"edge/goalie-edge-save-pctg-top-10/{_check('sort', sort, GOALIE_SAVE_PCTG_SORTS)}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def goalie_shot_location_top_10(
        self, category: str = "save-pctg", area: str = "all", season: str = None, game_type: int = 2
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 goalies by NHL EDGE shot location stats.

        Args:
            category (str, optional): Stat to rank by: "save-pctg", "saves", "goals-against" or "shots-against".
                Defaults to "save-pctg".
            area (str, optional): Rink area to rank by: "all", "high" (high danger), "mid" (mid range) or
                "long" (long range). Defaults to "all".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten goalies, ranked by ``category`` in ``area``

        Key Response Fields:
            player.id (int): Goalie player ID
            player.firstName.default (str): Goalie first name
            player.lastName.default (str): Goalie last name
            all (int | float): ``category`` value from all areas
            highDanger (int | float): ``category`` value from high-danger areas
            midRange (int | float): ``category`` value from mid range
            longRange (int | float): ``category`` value from long range

        Raises:
            ValueError: If ``category`` or ``area`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.goalie_shot_location_top_10()
            client.edge.goalie_shot_location_top_10(category="saves", area="high")
        """
        resource = (
            f"edge/goalie-shot-location-top-10/{_check('category', category, GOALIE_SHOT_LOCATION_CATEGORIES)}"
            f"/{_check('area', area, SHOT_LOCATION_AREAS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    # ========================
    # TEAM ENDPOINTS
    # ========================

    def team_detail(self, team_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE team detail statistics for a specific team.

        Retrieves detailed EDGE statistics including team skating metrics, shot data,
        and zone time information.

        Args:
            team_id (str): The unique identifier for the NHL team
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024). Defaults to current season.
            game_type (int, optional): Type of games (defaults to 2):
                2: Regular season
                3: Playoffs

        Returns:
            dict: Dictionary containing detailed EDGE statistics for the team

        Key Response Fields:
            team.abbrev (str): Team abbreviation
            team.wins (int): Total wins
            team.points (int): Total points
            shotSpeed.topShotSpeed.imperial (float): Top shot speed in mph
            skatingSpeed.speedMax.imperial (float): Maximum skating speed in mph
            distanceSkated.total.imperial (float): Total distance skated in miles
            zoneTimeDetails.offensiveZonePctg (float): Offensive zone time percentage

        Response Docs:
            docs/edge.md

        Example:
            client.edge.team_detail(team_id=10)
            client.edge.team_detail(team_id=10, season=20232024, game_type=2)
        """
        if season is None:
            resource = f"edge/team-detail/{team_id}/now"
        else:
            resource = f"edge/team-detail/{team_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def team_skating_distance_detail(self, team_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE skating distance details for a specific team.

        Args:
            team_id (str): The unique identifier for the NHL team
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Team skating distance statistics per game and per player

        Key Response Fields:
            distanceData (list): Distance entries per game and per player
            totalDistance.imperial (float): Total team distance skated in miles
            perGameAvg.imperial (float): Average distance per game in miles

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/team-skating-distance-detail/{team_id}/now"
        else:
            resource = f"edge/team-skating-distance-detail/{team_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def team_zone_time_details(self, team_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE zone time details for a specific team.

        Args:
            team_id (str): The unique identifier for the NHL team
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Team time spent in offensive, defensive, and neutral zones

        Key Response Fields:
            offensiveZonePctg (float): Offensive zone time percentage
            defensiveZonePctg (float): Defensive zone time percentage
            neutralZonePctg (float): Neutral zone time percentage

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/team-zone-time-details/{team_id}/now"
        else:
            resource = f"edge/team-zone-time-details/{team_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def team_shot_location_detail(self, team_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE shot location details for a specific team.

        Args:
            team_id (str): The unique identifier for the NHL team
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Team shot location data including shooting patterns and heat maps

        Key Response Fields:
            shotLocations (list): Shot data grouped by area
            area (str): Ice zone identifier
            shotCount (int): Number of shots from each area

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/team-shot-location-detail/{team_id}/now"
        else:
            resource = f"edge/team-shot-location-detail/{team_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def team_landing(self, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE team landing page data.

        Retrieves league-wide team EDGE statistics overview.

        Args:
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Overview of league-wide team EDGE statistics

        Key Response Fields:
            leaders (dict): Team EDGE leaders across categories
            topShotSpeed (list): Leaders by team shot speed
            topSkatingSpeed (list): Leaders by team skating speed

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = "edge/team-landing/now"
        else:
            resource = f"edge/team-landing/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def team_shot_speed_detail(self, team_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE shot speed details for a specific team.

        Args:
            team_id (str): The unique identifier for the NHL team
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Team shot speed statistics including maximum and average speeds

        Key Response Fields:
            shotSpeedData (list): Shot speed entries by player
            topShotSpeed.imperial (float): Top team shot speed in mph
            averageShotSpeed.imperial (float): Average team shot speed in mph

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/team-shot-speed-detail/{team_id}/now"
        else:
            resource = f"edge/team-shot-speed-detail/{team_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def team_skating_speed_detail(self, team_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE skating speed details for a specific team.

        Args:
            team_id (str): The unique identifier for the NHL team
            season (str, optional): Season in YYYYYYYY format (e.g., 20232024)
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Team skating speed statistics including burst speed and average speed

        Key Response Fields:
            skatingSpeedData (list): Skating speed entries by player
            speedMax.imperial (float): Maximum team skating speed in mph
            averageSpeed.imperial (float): Average team skating speed in mph

        Response Docs:
            docs/edge.md
        """
        if season is None:
            resource = f"edge/team-skating-speed-detail/{team_id}/now"
        else:
            resource = f"edge/team-skating-speed-detail/{team_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def team_comparison(self, team_id: str, season: str = None, game_type: int = 2) -> Dict[str, Any]:
        """Get NHL EDGE comparison statistics for a specific team.

        This is the data behind the team view of the EDGE comparison tool on nhl.com.

        Args:
            team_id (str): The unique identifier for the NHL team (e.g., "22" for Edmonton)
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            dict: Team EDGE stats for side-by-side comparison

        Key Response Fields:
            team.abbrev (str): Team abbreviation
            shotSpeedDetails.topShotSpeed (dict): Hardest team shot
            skatingSpeedDetails.maxSkatingSpeed (dict): Fastest team skating speed
            skatingDistanceDetails.distanceTotal (dict): Total team distance skated
            skatingDistanceLast10 (list): Distance skated in each of the last 10 games
            shotLocationTotals (list): Shot totals by rink area
            zoneTimeDetails.offensiveZonePctg (float): Offensive zone time share, with league average
            shotDifferential.shotAttemptDifferential (float): Shot attempt differential

        Response Docs:
            docs/edge.md

        Example:
            client.edge.team_comparison(team_id="22")
            client.edge.team_comparison(team_id="22", season="20242025", game_type=3)
        """
        resource = _with_period(f"edge/team-comparison/{team_id}", season, game_type)
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()

    def team_skating_speed_top_10(
        self, position_group: str = "all", sort: str = "max", season: str = None, game_type: int = 2
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 teams by NHL EDGE skating speed.

        Args:
            position_group (str, optional): Which of the team's skaters count: "all", "forwards" or "defense".
                Defaults to "all".
            sort (str, optional): "max" (top speed), or speed-burst counts "over-22", "20-22", "18-20" (mph).
                Defaults to "max".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten teams, ranked by ``sort``

        Key Response Fields:
            team.abbrev (str): Team abbreviation
            team.commonName.default (str): Team name
            maxSkatingSpeed.imperial (float): Team's top skating speed in mph, with ``overlay`` player/game info
            burstsOver22 (int): Bursts over 22 mph
            bursts20To22 (int): Bursts between 20 and 22 mph
            bursts18To20 (int): Bursts between 18 and 20 mph

        Raises:
            ValueError: If ``position_group`` or ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.team_skating_speed_top_10()
            client.edge.team_skating_speed_top_10(sort="over-22")
        """
        resource = (
            f"edge/team-skating-speed-top-10/{_check('position_group', position_group, POSITION_GROUPS)}"
            f"/{_check('sort', sort, SKATING_SPEED_SORTS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def team_shot_speed_top_10(
        self, position_group: str = "all", sort: str = "max", season: str = None, game_type: int = 2
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 teams by NHL EDGE shot speed.

        Args:
            position_group (str, optional): Which of the team's skaters count: "all", "forwards" or "defense".
                Defaults to "all".
            sort (str, optional): "max" (hardest shot), or shot-attempt counts "over-100", "90-99", "80-89",
                "70-79" (mph). Defaults to "max".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten teams, ranked by ``sort``

        Key Response Fields:
            team.abbrev (str): Team abbreviation
            team.commonName.default (str): Team name
            hardestShot.imperial (float): Team's hardest shot in mph, with ``overlay`` player/game info
            shotAttemptsOver100 (int): Shot attempts over 100 mph
            shotAttempts90To100 (int): Shot attempts between 90 and 100 mph
            shotAttempts80To90 (int): Shot attempts between 80 and 90 mph

        Raises:
            ValueError: If ``position_group`` or ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.team_shot_speed_top_10()
            client.edge.team_shot_speed_top_10(position_group="defense", sort="90-99")
        """
        resource = (
            f"edge/team-shot-speed-top-10/{_check('position_group', position_group, POSITION_GROUPS)}"
            f"/{_check('sort', sort, SHOT_SPEED_SORTS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def team_skating_distance_top_10(
        self,
        position_group: str = "all",
        strength: str = "all",
        sort: str = "total",
        season: str = None,
        game_type: int = 2,
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 teams by NHL EDGE distance skated.

        Args:
            position_group (str, optional): Which of the team's skaters count: "all", "forwards" or "defense".
                Defaults to "all".
            strength (str, optional): "all", "es" (even strength), "pp" (power play) or "pk" (penalty kill).
                Defaults to "all".
            sort (str, optional): "total", "per-60", "max-game" or "max-period". Defaults to "total".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten teams, ranked by ``sort``

        Key Response Fields:
            team.abbrev (str): Team abbreviation
            team.commonName.default (str): Team name
            distanceTotal.imperial (float): Total distance skated in miles (``metric`` for km)
            distancePer60.imperial (float): Distance per 60 minutes in miles
            distanceMaxPerGame.imperial (float): Most distance in a single game, with ``overlay`` game info
            distanceMaxPerPeriod.imperial (float): Most distance in a single period, with ``overlay`` game info

        Raises:
            ValueError: If ``position_group``, ``strength`` or ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.team_skating_distance_top_10()
            client.edge.team_skating_distance_top_10(strength="pp", sort="per-60")
        """
        resource = (
            f"edge/team-skating-distance-top-10/{_check('position_group', position_group, POSITION_GROUPS)}"
            f"/{_check('strength', strength, STRENGTHS)}/{_check('sort', sort, SKATING_DISTANCE_SORTS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def team_zone_time_top_10(
        self, strength: str = "all", sort: str = "offensive", season: str = None, game_type: int = 2
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 teams by NHL EDGE zone time percentage.

        Args:
            strength (str, optional): "all", "es" (even strength), "pp" (power play) or "pk" (penalty kill).
                Defaults to "all".
            sort (str, optional): "offensive", "neutral" or "defensive". Defaults to "offensive".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten teams, ranked by ``sort``

        Key Response Fields:
            team.abbrev (str): Team abbreviation
            team.commonName.default (str): Team name
            offensiveZoneTime (float): Share of time in the offensive zone (0-1)
            neutralZoneTime (float): Share of time in the neutral zone (0-1)
            defensiveZoneTime (float): Share of time in the defensive zone (0-1)

        Raises:
            ValueError: If ``strength`` or ``sort`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.team_zone_time_top_10()
            client.edge.team_zone_time_top_10(strength="pk", sort="defensive")
        """
        resource = (
            f"edge/team-zone-time-top-10/{_check('strength', strength, STRENGTHS)}"
            f"/{_check('sort', sort, ZONE_TIME_SORTS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()

    def team_shot_location_top_10(
        self,
        position_group: str = "all",
        category: str = "sog",
        area: str = "all",
        season: str = None,
        game_type: int = 2,
    ) -> List[Dict[str, Any]]:
        """Get the league's top 10 teams by NHL EDGE shot location stats.

        Args:
            position_group (str, optional): Which of the team's skaters count: "all", "forwards" or "defense".
                Defaults to "all".
            category (str, optional): Stat to rank by: "sog" (shots on goal), "goals" or "shooting-pctg".
                Defaults to "sog".
            area (str, optional): Rink area to rank by: "all", "high" (high danger), "mid" (mid range) or
                "long" (long range). Defaults to "all".
            season (str, optional): Season in YYYYYYYY format (e.g., 20242025). Defaults to current season.
            game_type (int, optional): Type of games (2: Regular season, 3: Playoffs). Defaults to 2.

        Returns:
            List[Dict[str, Any]]: Ten teams, ranked by ``category`` in ``area``

        Key Response Fields:
            team.id (int): Team ID
            team.abbrev (str): Team abbreviation
            all (int | float): ``category`` value from all areas
            highDanger (int | float): ``category`` value from high-danger areas
            midRange (int | float): ``category`` value from mid range
            longRange (int | float): ``category`` value from long range

        Raises:
            ValueError: If ``position_group``, ``category`` or ``area`` is not an allowed value

        Response Docs:
            docs/edge.md

        Example:
            client.edge.team_shot_location_top_10()
            client.edge.team_shot_location_top_10(category="goals", area="high")
        """
        resource = (
            f"edge/team-shot-location-top-10/{_check('position_group', position_group, POSITION_GROUPS)}"
            f"/{_check('category', category, SHOT_LOCATION_CATEGORIES)}/{_check('area', area, SHOT_LOCATION_AREAS)}"
        )
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=_with_period(resource, season, game_type)).json()
