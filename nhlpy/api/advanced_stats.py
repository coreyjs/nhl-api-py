#!/usr/bin/env python3
"""
Combined advanced stats module for NHL skaters, goalies, and teams.

Usage (from the command line):
    python advanced_stats.py <type> <id>

Where:
  - <type> is one of "skater", "goalie", or "team"
  - <id> is the player's (or team's) identifier
"""

import aiohttp
import asyncio
import json
import logging
import sys
from dataclasses import dataclass
from typing import List, Dict, Any

# Optional: import cookie retrieval if available
try:
    from nhlpy.utils.cookies import get_nhl_edge_cookies
except ImportError:
    get_nhl_edge_cookies = None
# Optional: debug
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Base WebSocket Client for Advanced Stats
# -----------------------------------------------------------------------------
class AdvancedStatsBase:
    def __init__(self, cookies: Dict[str, str] = None):
        self.cookies = cookies
        self.messages_received: List[Dict[str, Any]] = []
        self.subsequent_sent = False

    def _get_headers(self) -> Dict[str, str]:
        cookie_header = (
            "; ".join(f"{name}={value}" for name, value in self.cookies.items())
            if self.cookies
            else ""
        )
        return {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            ),
            "Origin": "https://edge.nhl.com",
            "Cookie": cookie_header,
        }

    async def connect_and_listen(self) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(
                self.ws_url,
                headers=self._get_headers(),
                heartbeat=15,
                receive_timeout=20,
                ssl=False,
            ) as ws:
                await self._handle_initial_handshake(ws)
                if self.should_send_subsequent_immediately():
                    await self._send_subsequent_messages(ws)
                    self.subsequent_sent = True
                await self._listen_for_messages(ws)
        return self.messages_received

    async def _listen_for_messages(self, ws: aiohttp.ClientWebSocketResponse):
        try:
            while True:
                msg = await ws.receive()
                await self._process_message(msg, ws)
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            logger.error("Connection error: %s", e)

    async def _process_message(self, msg: aiohttp.WSMessage, ws: aiohttp.ClientWebSocketResponse):
        raise NotImplementedError

    async def _handle_initial_handshake(self, ws: aiohttp.ClientWebSocketResponse):
        raise NotImplementedError

    async def _send_subsequent_messages(self, ws: aiohttp.ClientWebSocketResponse):
        raise NotImplementedError

    def should_send_subsequent_immediately(self) -> bool:
        """
        Determines when to send subsequent messages. By default, send these upon
        receiving the first message (i.e. for skaters and teams). For goalies,
        we send immediately after the handshake.
        """
        return False

# -----------------------------------------------------------------------------
# Skater Advanced Stats
# -----------------------------------------------------------------------------
@dataclass
class SkaterStatsConfig:
    player_id: str
    ws_template: str = "wss://edge.nhl.com/en/skater/{player_id}"
    season: str = "20242025"
    stage: str = "regular"
    units: str = "imperial"
    cookies: Dict[str, str] = None
    manpower: str = "all"
    shootingmetrics: str = "shots"

class SkaterStats(AdvancedStatsBase):
    def __init__(self, config: SkaterStatsConfig):
        super().__init__(config.cookies)
        self.config = config
        self.ws_url = config.ws_template.format(player_id=config.player_id)

    async def _handle_initial_handshake(self, ws: aiohttp.ClientWebSocketResponse):
        initial_msg = self._create_initial_message()
        await ws.send_json(initial_msg)
        logger.debug("Sent initial handshake message for skater.")

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
                        "source": "players",
                    }
                },
            },
        }

    async def _process_message(self, msg: aiohttp.WSMessage, ws: aiohttp.ClientWebSocketResponse):
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
                self.messages_received.append(data)
                logger.debug("Received a new message for skater.")
                if not self.subsequent_sent:
                    await self._send_subsequent_messages(ws)
                    self.subsequent_sent = True
            except json.JSONDecodeError:
                logger.error("Received non-JSON message for skater.")
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            logger.info("Connection closed by server for skater.")
        elif msg.type == aiohttp.WSMsgType.ERROR:
            logger.error("WebSocket error for skater: %s", msg.data)

    async def _send_subsequent_messages(self, ws: aiohttp.ClientWebSocketResponse):
        messages = self._generate_subsequent_messages()
        for idx, message in enumerate(messages, start=1):
            await ws.send_json(message)
            logger.debug("Sent subsequent message %d for skater", idx)

    def _generate_subsequent_messages(self) -> List[Dict[str, Any]]:
        base_params = {
            "type": "skaters",
            "player": self.config.player_id,
            "rootName": "skatersProfiles",
            "source": "players",
        }
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
                        "callbackFunction": "initializeDataElements",
                    },
                },
            }
            for render_func, target in [
                ("renderPlayerCard", "#profile-playercard"),
                ("renderProfilePlayerSection", "#profile-section"),
            ]
        ]
        section_configs = [
            ("overview", "#overview-section-content", {}),
            ("skatingspeed", "#skatingspeed-section-content", {}),
            ("skatingdistance", "#skatingdistance-section-content", {"manpower": self.config.manpower}),
            ("shotspeed", "#shotspeed-section-content", {}),
            ("shotlocation", "#shotlocation-section-content", {"shootingmetrics": self.config.shootingmetrics, "shotlocation": "all"}),
            ("zonetime", "#zonetime-section-content", {"manpower": self.config.manpower}),
        ]
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
                            **extra_params,
                        },
                        "callbackFunction": "runClientFns",
                    },
                },
            }
            for section_name, target, extra_params in section_configs
        ]
        return profile_messages + section_messages

# -----------------------------------------------------------------------------
# Goalie Advanced Stats
# -----------------------------------------------------------------------------
@dataclass
class GoalieStatsConfig:
    player_id: str
    ws_template: str = "wss://edge.nhl.com/en/goalie/{player_id}"
    season: str = "20242025"
    stage: str = "regular"
    units: str = "imperial"
    cookies: Dict[str, str] = None

class GoalieStats(AdvancedStatsBase):
    def __init__(self, config: GoalieStatsConfig):
        super().__init__(config.cookies)
        self.config = config
        self.ws_url = config.ws_template.format(player_id=config.player_id)

    def should_send_subsequent_immediately(self) -> bool:
        # For goalies, send subsequent messages immediately after the handshake.
        return True

    async def _handle_initial_handshake(self, ws: aiohttp.ClientWebSocketResponse):
        initial_msg = {
            "type": "action",
            "event": {
                "domain": "edge.nhl.com",
                "uri": f"/en/goalie/{self.config.player_id}",
                "action": "getLabel",
                "data": {
                    "params": {
                        "type": "goalies",
                        "player": self.config.player_id,
                        "rootName": "goaliesProfiles",
                        "source": "players",
                        "season": self.config.season,
                        "stage": self.config.stage,
                    }
                },
            },
        }
        await ws.send_json(initial_msg)
        logger.debug("Sent initial handshake message for goalie.")

    async def _send_subsequent_messages(self, ws: aiohttp.ClientWebSocketResponse):
        messages = [
            {
                "type": "action",
                "event": {
                    "domain": "edge.nhl.com",
                    "uri": f"/en/goalie/{self.config.player_id}",
                    "action": "load",
                    "data": {
                        "renderFunction": "renderProfileContent",
                        "target": "#goverview-section-content",
                        "params": {
                            "sectionName": "goverview",
                            "units": self.config.units,
                            "season": self.config.season,
                            "stage": self.config.stage,
                            "feed": "goaliesProfiles",
                            "id": self.config.player_id,
                        },
                        "callbackFunction": "runClientFns",
                    },
                },
            },
            {
                "type": "action",
                "event": {
                    "domain": "edge.nhl.com",
                    "uri": f"/en/goalie/{self.config.player_id}",
                    "action": "load",
                    "data": {
                        "renderFunction": "renderProfileContent",
                        "target": "#gsaves-section-content",
                        "params": {
                            "sectionName": "gsaves",
                            "units": self.config.units,
                            "shotlocation": "all",
                            "goaliemetrics": "saves",
                            "season": self.config.season,
                            "stage": self.config.stage,
                            "feed": "goaliesProfiles",
                            "id": self.config.player_id,
                        },
                        "callbackFunction": "runClientFns",
                    },
                },
            },
            {
                "type": "action",
                "event": {
                    "domain": "edge.nhl.com",
                    "uri": f"/en/goalie/{self.config.player_id}",
                    "action": "load",
                    "data": {
                        "renderFunction": "renderProfileContent",
                        "target": "#support-section-content",
                        "params": {
                            "sectionName": "support",
                            "units": self.config.units,
                            "rates": "total",
                            "season": self.config.season,
                            "stage": self.config.stage,
                            "feed": "goaliesProfiles",
                            "id": self.config.player_id,
                        },
                        "callbackFunction": "runClientFns",
                    },
                },
            },
            {
                "type": "action",
                "event": {
                    "domain": "edge.nhl.com",
                    "uri": f"/en/goalie/{self.config.player_id}",
                    "action": "load",
                    "data": {
                        "renderFunction": "renderProfileContent",
                        "target": "#avggames-section-content",
                        "params": {
                            "sectionName": "avggames",
                            "units": self.config.units,
                            "season": self.config.season,
                            "stage": self.config.stage,
                            "feed": "goaliesProfiles",
                            "id": self.config.player_id,
                        },
                        "callbackFunction": "runClientFns",
                    },
                },
            },
        ]
        for idx, message in enumerate(messages, start=1):
            await ws.send_json(message)
            logger.debug("Sent subsequent message %d for goalie", idx)

    async def _process_message(self, msg: aiohttp.WSMessage, ws: aiohttp.ClientWebSocketResponse):
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
                self.messages_received.append(data)
                logger.debug("Received a new message for goalie.")
            except json.JSONDecodeError:
                logger.error("Received non-JSON message for goalie.")
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            logger.info("Connection closed by server for goalie.")
        elif msg.type == aiohttp.WSMsgType.ERROR:
            logger.error("WebSocket error for goalie: %s", msg.data)

# -----------------------------------------------------------------------------
# Team Advanced Stats
# -----------------------------------------------------------------------------
@dataclass
class TeamStatsConfig:
    team: str
    ws_template: str = "wss://edge.nhl.com/en/team/{team}"
    season: str = "20242025"
    stage: str = "regular"
    units: str = "imperial"
    cookies: Dict[str, str] = None
    manpower: str = "all"
    shootingmetrics: str = "shots"

class TeamStats(AdvancedStatsBase):
    def __init__(self, config: TeamStatsConfig):
        super().__init__(config.cookies)
        self.config = config
        self.ws_url = config.ws_template.format(team=config.team)

    async def _handle_initial_handshake(self, ws: aiohttp.ClientWebSocketResponse):
        initial_msg = self._create_initial_message()
        await ws.send_json(initial_msg)
        logger.debug("Sent initial handshake message for team.")

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
                        "source": "teams",
                    }
                },
            },
        }

    async def _process_message(self, msg: aiohttp.WSMessage, ws: aiohttp.ClientWebSocketResponse):
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
                self.messages_received.append(data)
                logger.debug("Received a new message for team.")
                if not self.subsequent_sent:
                    await self._send_subsequent_messages(ws)
                    self.subsequent_sent = True
            except json.JSONDecodeError:
                logger.error("Received non-JSON message for team.")
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            logger.info("Connection closed by server for team.")
        elif msg.type == aiohttp.WSMsgType.ERROR:
            logger.error("WebSocket error for team: %s", msg.data)

    async def _send_subsequent_messages(self, ws: aiohttp.ClientWebSocketResponse):
        messages = self._generate_subsequent_messages()
        for idx, message in enumerate(messages, start=1):
            await ws.send_json(message)
            logger.debug("Sent subsequent message %d for team", idx)

    def _generate_subsequent_messages(self) -> List[Dict[str, Any]]:
        base_params = {
            "type": "teams",
            "team": self.config.team,
            "rootName": "teamsProfiles",
            "source": "teams",
        }
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
                        "callbackFunction": "initializeDataElements",
                    },
                },
            }
            for render_func, target in [
                ("renderTeamCard", "#profile-teamcard"),
                ("renderProfileTeamSection", "#profile-section"),
            ]
        ]
        section_configs = [
            ("overview", "#overview-section-content", {}),
            ("skatingspeed", "#skating-section-content", {}),
            ("skatingdistance", "#skatingdistance-section-content", {"manpower": self.config.manpower}),
            ("shotspeed", "#shotspeed-section-content", {}),
            ("shotlocation", "#shotlocation-section-content", {"shootingmetrics": self.config.shootingmetrics, "shotlocation": "all"}),
            ("zonetime", "#zonetime-section-content", {"manpower": self.config.manpower}),
        ]
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
                            **extra_params,
                        },
                        "callbackFunction": "runClientFns",
                    },
                },
            }
            for section_name, target, extra_params in section_configs
        ]
        return profile_messages + section_messages

# -----------------------------------------------------------------------------
# Main Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import pprint

    async def main():
        if len(sys.argv) < 3:
            print("Usage: {} <type> <id>".format(sys.argv[0]))
            print("  type: skater, goalie, team")
            sys.exit(1)

        stat_type = sys.argv[1].lower()
        identifier = sys.argv[2]

        cookies = get_nhl_edge_cookies() if get_nhl_edge_cookies else None

        if stat_type == "skater":
            config = SkaterStatsConfig(player_id=identifier, cookies=cookies)
            client = SkaterStats(config)
        elif stat_type == "goalie":
            config = GoalieStatsConfig(player_id=identifier, cookies=cookies)
            client = GoalieStats(config)
        elif stat_type == "team":
            config = TeamStatsConfig(team=identifier, cookies=cookies)
            client = TeamStats(config)
        else:
            print("Unknown type '{}'. Must be one of: skater, goalie, team.".format(stat_type))
            sys.exit(1)

        messages = await client.connect_and_listen()
        pprint.pprint(messages)

    asyncio.run(main())
