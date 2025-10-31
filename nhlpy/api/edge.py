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
        """
        if season is None:
            resource = f"edge/team-skating-speed-detail/{team_id}/now"
        else:
            resource = f"edge/team-skating-speed-detail/{team_id}/{season}/{game_type}"
        return self.client.get(endpoint=Endpoint.API_WEB_V1, resource=resource).json()
