from typing import Dict, Any

from nhlpy.http_client import HttpClient, Endpoint


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
