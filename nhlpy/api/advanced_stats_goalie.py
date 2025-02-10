#!/usr/bin/env python3
"""
advanced_stats_goalie.py

This module provides functionality for retrieving advanced NHL goalie statistics
via websockets from the NHL EDGE site. It is designed to be imported and used
within the nhl-api-py package, following the same structural and documentation
conventions as the existing HTTP endpoints.
"""

import aiohttp
import asyncio
import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any

# Import cookie retrieval from the refactored utility module.
from nhlpy.utils.cookies import get_nhl_edge_cookies

logger = logging.getLogger(__name__)

@dataclass
class AdvancedStatsGoalieConfig:
    """
    Configuration for connecting to the NHL EDGE websocket endpoint for goalies.

    Attributes:
        player_id (str): The unique goalie identifier.
        ws_template (str): The websocket URL template.
        season (str): The season identifier (e.g., "20242025").
        stage (str): The stage of the season (e.g., "regular").
        units (str): The units for any numerical data (e.g., "imperial").
        cookies (Dict[str, str], optional): A dictionary of cookies for authentication.
    """
    player_id: str
    ws_template: str = "wss://edge.nhl.com/en/goalie/{player_id}"
    season: str = "20242025"
    stage: str = "regular"
    units: str = "imperial"
    cookies: Dict[str, str] = None

class AdvancedStatsGoalie:
    """
    AdvancedStatsGoalie handles websocket communication to retrieve advanced NHL goalie stats.
    """
    def __init__(self, config: AdvancedStatsGoalieConfig):
        self.config = config
        self.ws_url = config.ws_template.format(player_id=config.player_id)
        self.messages_received: List[Dict[str, Any]] = []
        self.subsequent_sent = False

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
                await self._send_subsequent_messages(ws)
                await self._listen_for_messages(ws)
        return self.messages_received

    async def _handle_initial_handshake(self, ws: aiohttp.ClientWebSocketResponse):
        # Send the getLabel message first.
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
                        "stage": self.config.stage
                    }
                }
            }
        }
        await ws.send_json(initial_msg)
        logger.debug("Sent initial handshake message for goalie.")

    async def _send_subsequent_messages(self, ws: aiohttp.ClientWebSocketResponse):
        # Build subsequent messages that match the browser messages.
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
                            "sectionName": "goverview",  # exactly as seen in browser
                            "units": self.config.units,
                            "season": self.config.season,
                            "stage": self.config.stage,
                            "feed": "goaliesProfiles",
                            "id": self.config.player_id
                        },
                        "callbackFunction": "runClientFns"
                    }
                }
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
                            "id": self.config.player_id
                        },
                        "callbackFunction": "runClientFns"
                    }
                }
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
                            "id": self.config.player_id
                        },
                        "callbackFunction": "runClientFns"
                    }
                }
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
                            "id": self.config.player_id
                        },
                        "callbackFunction": "runClientFns"
                    }
                }
            }
        ]
        for idx, message in enumerate(messages, start=1):
            await ws.send_json(message)
            logger.debug("Sent subsequent message %d for goalie", idx)
        self.subsequent_sent = True

    async def _listen_for_messages(self, ws: aiohttp.ClientWebSocketResponse):
        try:
            while True:
                msg = await ws.receive()
                await self._process_message(msg, ws)
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            logger.error("Connection error for goalie: %s", e)

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

# For testing purposes when running this file directly:
if __name__ == "__main__":
    import sys
    from pprint import pprint
    if len(sys.argv) < 2:
        print("Usage: advanced_stats_goalie.py <player_id>")
        sys.exit(1)
    player_id = sys.argv[1]
    config = AdvancedStatsGoalieConfig(player_id=player_id)
    goalie_stats = AdvancedStatsGoalie(config)
    loop = asyncio.get_event_loop()
    messages = loop.run_until_complete(goalie_stats.connect_and_listen())
    pprint(messages)