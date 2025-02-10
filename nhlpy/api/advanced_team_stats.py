#!/usr/bin/env python3
"""
advanced_team_stats.py

This module provides functionality for retrieving advanced NHL team statistics
via websockets from the NHL edge site. It follows the same structure as the
existing advanced_stats (skater) module, but adapts the endpoints and payloads
to work with team data.
"""

import aiohttp
import asyncio
import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any

# Import cookie retrieval from the utility module (if needed)
from nhlpy.utils.cookies import get_nhl_edge_cookies

logger = logging.getLogger(__name__)


@dataclass
class AdvancedTeamStatsConfig:
    """
    Configuration for connecting to the NHL edge websocket endpoint for team stats.

    Attributes:
        team (str): The team identifier (e.g., "PHI").
        ws_template (str): The websocket URL template.
        season (str): The season identifier (e.g., "20242025").
        stage (str): The stage of the season (e.g., "regular").
        units (str): The units for numerical data (e.g., "imperial").
        cookies (Dict[str, str], optional): A dictionary of cookies for authentication.
        manpower (str): The manpower configuration (if applicable).
        shootingmetrics (str): The shooting metrics configuration (if applicable).
    """
    team: str
    ws_template: str = "wss://edge.nhl.com/en/team/{team}"
    season: str = "20242025"
    stage: str = "regular"
    units: str = "imperial"
    cookies: Dict[str, str] = None
    manpower: str = "all"         # You may or may not need these for team stats
    shootingmetrics: str = "shots"


class AdvancedTeamStats:
    """
    Handles websocket communication to retrieve advanced NHL team stats.
    """
    def __init__(self, config: AdvancedTeamStatsConfig):
        self.config = config
        self.ws_url = config.ws_template.format(team=config.team)
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
                await self._listen_for_messages(ws)
        return self.messages_received

    async def _handle_initial_handshake(self, ws: aiohttp.ClientWebSocketResponse):
        initial_msg = self._create_initial_message()
        await ws.send_json(initial_msg)
        logger.debug("Sent initial handshake message.")

    def _create_initial_message(self) -> Dict[str, Any]:
        # Note the differences compared to the skater version:
        #   - The URI now points to /en/team/{team}
        #   - The params include "type": "teams" and use "team" rather than "player"
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

    def _generate_subsequent_messages(self) -> List[Dict[str, Any]]:
        # Base parameters for team messages; note the differences from the skater code.
        base_params = {
            "type": "teams",
            "team": self.config.team,
            "rootName": "teamsProfiles",
            "source": "teams"
        }

        # Adjust the sections as needed for team data. The sections below are examples.
        # You may need to update the section names, target selectors, and extra parameters
        # to match what the team page expects.
        section_configs = [
            ("overview", "#overview-section-content", {}),
            ("skatingspeed", "#skating-section-content", {}),  # or "#skatingspeed-section-content" if available
            ("skatingdistance", "#skatingdistance-section-content", {"manpower": self.config.manpower}),
            ("shotspeed", "#shotspeed-section-content", {}),
            ("shotlocation", "#shotlocation-section-content", {"shootingmetrics": self.config.shootingmetrics, "shotlocation": "all"}),
            ("zonetime", "#zonetime-section-content", {"manpower": self.config.manpower}),
        ]
        messages = []

        # Profile messages (for example, to render a team card/section)
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


# For testing purposes when running this file directly:
if __name__ == "__main__":
    async def main():
        # Retrieve cookies if needed for authentication.
        cookies = get_nhl_edge_cookies()
        config = AdvancedTeamStatsConfig(team="PHI", cookies=cookies)
        team_stats = AdvancedTeamStats(config)
        messages = await team_stats.connect_and_listen()
        # Pretty-print the messages received from the websocket.
        print(json.dumps(messages, indent=2))

    asyncio.run(main())