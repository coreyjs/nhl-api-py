#!/usr/bin/env python3
"""
advanced_stats_refactored.py

This module demonstrates a refactored approach for retrieving advanced NHL statistics
(via websockets) that applies a common base class for shared functionality. Two concrete
classes are provided: one for skater stats and one for team stats.
"""

import aiohttp
import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any

# Import cookie retrieval (if needed)
from nhlpy.utils.cookies import get_nhl_edge_cookies

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

###############################################################################
# Configuration Data Classes
###############################################################################

@dataclass
class BaseStatsConfig:
    """
    Base configuration for advanced stats.
    """
    season: str = "20242025"
    stage: str = "regular"
    units: str = "imperial"
    cookies: Dict[str, str] = None
    manpower: str = "all"
    shootingmetrics: str = "shots"


@dataclass
class AdvancedSkaterStatsConfig(BaseStatsConfig):
    """
    Configuration for advanced skater stats.
    """
    player_id: str = ""
    ws_template: str = "wss://edge.nhl.com/en/skater/{player_id}"


@dataclass
class AdvancedTeamStatsConfig(BaseStatsConfig):
    """
    Configuration for advanced team stats.
    """
    team: str = ""
    ws_template: str = "wss://edge.nhl.com/en/team/{team}"


###############################################################################
# Base Websocket Stats Class
###############################################################################

class AdvancedStatsBase(ABC):
    """
    Base class for retrieving advanced NHL stats (skater or team) via websocket.
    Contains common connection, handshake, and message processing logic.
    """
    def __init__(self, config: BaseStatsConfig):
        self.config = config
        self.ws_url = self._get_ws_url()
        self.messages_received: List[Dict[str, Any]] = []
        self.subsequent_sent = False

    @abstractmethod
    def _get_ws_url(self) -> str:
        """Return the websocket URL based on the configuration."""
        pass

    def _get_headers(self) -> Dict[str, str]:
        if self.config.cookies:
            cookie_header = "; ".join(f"{name}={value}" for name, value in self.config.cookies.items())
        else:
            cookie_header = ""
        return {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            ),
            "Origin": "https://edge.nhl.com",
            "Cookie": cookie_header
        }

    async def connect_and_listen(self) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(
                self.ws_url,
                headers=self._get_headers(),
                heartbeat=15,
                receive_timeout=20,
                ssl=False
            ) as ws:
                await self._handle_initial_handshake(ws)
                await self._listen_for_messages(ws)
        return self.messages_received

    async def _handle_initial_handshake(self, ws: aiohttp.ClientWebSocketResponse):
        initial_msg = self._create_initial_message()
        await ws.send_json(initial_msg)
        logger.debug("Sent initial handshake message.")

    @abstractmethod
    def _create_initial_message(self) -> Dict[str, Any]:
        """Creates the initial handshake message (skater or team specific)."""
        pass

    async def _listen_for_messages(self, ws: aiohttp.ClientWebSocketResponse):
        try:
            while True:
                msg = await ws.receive()
                await self._process_message(msg, ws)
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            logger.error("Connection error: %s", e)

    async def _process_message(self, msg: aiohttp.WSMessage, ws: aiohttp.ClientWebSocketResponse):
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
                self.messages_received.append(data)
                logger.debug("Received a new message.")
                if not self.subsequent_sent:
                    await self._send_subsequent_messages(ws)
                    self.subsequent_sent = True
            except json.JSONDecodeError:
                logger.error("Received non-JSON message.")
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            logger.info("Connection closed by server.")
        elif msg.type == aiohttp.WSMsgType.ERROR:
            logger.error("WebSocket error: %s", msg.data)

    async def _send_subsequent_messages(self, ws: aiohttp.ClientWebSocketResponse):
        messages = self._generate_subsequent_messages()
        for idx, message in enumerate(messages, start=1):
            await ws.send_json(message)
            logger.debug("Sent subsequent message %d", idx)

    @abstractmethod
    def _generate_subsequent_messages(self) -> List[Dict[str, Any]]:
        """Generates subsequent messages for additional data loads."""
        pass


###############################################################################
# Skater Stats Implementation
###############################################################################

class AdvancedSkaterStats(AdvancedStatsBase):
    """
    Retrieves advanced NHL skater stats via websocket.
    """
    def __init__(self, config: AdvancedSkaterStatsConfig):
        super().__init__(config)

    def _get_ws_url(self) -> str:
        return self.config.ws_template.format(player_id=self.config.player_id)

    def _create_initial_message(self) -> Dict[str, Any]:
        return {
            "type": "action",
            "event": {
                "domain": "edge.nhl.com",
                "uri": f"/en/skater/{self.config.player_id}",
                "action": "getLabel",
                "data": {
                    "params": {
                        "type": "skaters",
                        "player": self.config.player_id,
                        "rootName": "skatersProfiles",
                        "source": "players"
                    }
                }
            }
        }

    def _generate_subsequent_messages(self) -> List[Dict[str, Any]]:
        base_params = {
            "type": "skaters",
            "player": self.config.player_id,
            "rootName": "skatersProfiles",
            "source": "players"
        }
        section_configs = [
            ("overview", "#overview-section-content", {}),
            ("skatingspeed", "#skatingspeed-section-content", {}),
            ("skatingdistance", "#skatingdistance-section-content", {"manpower": self.config.manpower}),
            ("shotspeed", "#shotspeed-section-content", {}),
            ("shotlocation", "#shotlocation-section-content", {"shootingmetrics": self.config.shootingmetrics, "shotlocation": "all"}),
            ("zonetime", "#zonetime-section-content", {"manpower": self.config.manpower}),
        ]
        messages = []

        # Profile messages (e.g. player card/section)
        profile_messages = [
            {
                "type": "action",
                "event": {
                    "domain": "edge.nhl.com",
                    "uri": f"/en/skater/{self.config.player_id}",
                    "action": "load",
                    "data": {
                        "renderFunction": render_func,
                        "target": target,
                        "params": base_params,
                        "callbackFunction": "initializeDataElements"
                    }
                }
            } for render_func, target in [
                ("renderPlayerCard", "#profile-playercard"),
                ("renderProfilePlayerSection", "#profile-section")
            ]
        ]
        messages.extend(profile_messages)

        # Section messages
        section_messages = [
            {
                "type": "action",
                "event": {
                    "domain": "edge.nhl.com",
                    "uri": f"/en/skater/{self.config.player_id}",
                    "action": "load",
                    "data": {
                        "renderFunction": "renderProfileContent",
                        "target": target,
                        "params": {
                            "sectionName": section_name,
                            "units": self.config.units,
                            "season": self.config.season,
                            "stage": self.config.stage,
                            "feed": "skatersProfiles",
                            "id": self.config.player_id,
                            **extra_params
                        },
                        "callbackFunction": "runClientFns"
                    }
                }
            } for section_name, target, extra_params in section_configs
        ]
        messages.extend(section_messages)
        return messages


###############################################################################
# Team Stats Implementation
###############################################################################

class AdvancedTeamStats(AdvancedStatsBase):
    """
    Retrieves advanced NHL team stats via websocket.
    """
    def __init__(self, config: AdvancedTeamStatsConfig):
        super().__init__(config)

    def _get_ws_url(self) -> str:
        return self.config.ws_template.format(team=self.config.team)

    def _create_initial_message(self) -> Dict[str, Any]:
        return {
            "type": "action",
            "event": {
                "domain": "edge.nhl.com",
                "uri": f"/en/team/{self.config.team}",
                "action": "getLabel",
                "data": {
                    "params": {
                        "type": "teams",
                        "team": self.config.team,
                        "rootName": "teamsProfiles",
                        "source": "teams"
                    }
                }
            }
        }

    def _generate_subsequent_messages(self) -> List[Dict[str, Any]]:
        base_params = {
            "type": "teams",
            "team": self.config.team,
            "rootName": "teamsProfiles",
            "source": "teams"
        }
        section_configs = [
            ("overview", "#overview-section-content", {}),
            ("skating", "#skating-section-content", {"manpower": self.config.manpower}),
            ("shooting", "#shooting-section-content", {"shootingmetrics": self.config.shootingmetrics}),
            ("zonetime", "#zonetime-section-content", {"manpower": self.config.manpower}),
        ]
        messages = []

        # Profile messages (e.g. team card/section)
        profile_messages = [
            {
                "type": "action",
                "event": {
                    "domain": "edge.nhl.com",
                    "uri": f"/en/team/{self.config.team}",
                    "action": "load",
                    "data": {
                        "renderFunction": render_func,
                        "target": target,
                        "params": base_params,
                        "callbackFunction": "initializeDataElements"
                    }
                }
            } for render_func, target in [
                ("renderTeamCard", "#profile-teamcard"),
                ("renderProfileTeamSection", "#profile-section")
            ]
        ]
        messages.extend(profile_messages)

        # Section messages
        section_messages = [
            {
                "type": "action",
                "event": {
                    "domain": "edge.nhl.com",
                    "uri": f"/en/team/{self.config.team}",
                    "action": "load",
                    "data": {
                        "renderFunction": "renderProfileContent",
                        "target": target,
                        "params": {
                            "sectionName": section_name,
                            "units": self.config.units,
                            "season": self.config.season,
                            "stage": self.config.stage,
                            "feed": "teamsProfiles",
                            "id": self.config.team,
                            **extra_params
                        },
                        "callbackFunction": "runClientFns"
                    }
                }
            } for section_name, target, extra_params in section_configs
        ]
        messages.extend(section_messages)
        return messages


###############################################################################
# Testing the Implementation
###############################################################################

if __name__ == "__main__":
    async def main():
        # Uncomment one of the following sections to test skater or team stats.
        
        # --- Test Skater Stats ---
        # cookies = get_nhl_edge_cookies()
        # skater_config = AdvancedSkaterStatsConfig(player_id="8478402", cookies=cookies)
        # skater_stats = AdvancedSkaterStats(skater_config)
        # messages = await skater_stats.connect_and_listen()
        # print("Skater Stats Messages:")
        # print(json.dumps(messages, indent=2))
        
        # --- Test Team Stats ---
        cookies = get_nhl_edge_cookies()
        team_config = AdvancedTeamStatsConfig(team="PHI", cookies=cookies)
        team_stats = AdvancedTeamStats(team_config)
        messages = await team_stats.connect_and_listen()
        print("Team Stats Messages:")
        print(json.dumps(messages, indent=2))
        
    asyncio.run(main())