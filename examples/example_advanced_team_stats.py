#!/usr/bin/env python3
"""
example_advanced_team_stats.py

This script demonstrates how to use the AdvancedTeamStats API together with
the parsing functions while enforcing a timeout on the websocket connection.
"""

import asyncio
import json
from nhlpy.api.advanced_stats import TeamStats, TeamStatsConfig
from nhlpy.utils.cookies import get_nhl_edge_cookies
from nhlpy.parsers.advanced_parsers import parse_message_team

async def main():
    print("Retrieving cookies from NHL Edge...")
    cookies = get_nhl_edge_cookies(headless=True)
    
    config = TeamStatsConfig(
        team="PHI",  # Replace with the desired team identifier.
        season="20242025",
        stage="regular",
        units="imperial",
        cookies=cookies,
        manpower="es",           # Use team-relevant parameters (if applicable)
        shootingmetrics="shooting%"  # Use team-relevant parameters (if applicable)
    )
    
    adv_stats = TeamStats(config)
    
    try:
        # Wait at most 3 seconds for messages. Adjust the timeout as needed.
        raw_messages = await asyncio.wait_for(adv_stats.connect_and_listen(), timeout=3)
    except asyncio.TimeoutError:
        raw_messages = adv_stats.messages_received

    # Parse in-memory messages directly
    parsed_data = {}
    for msg in raw_messages:
        # print("Raw message:", msg)
        parsed_data.update(parse_message_team(msg))
    
    print(json.dumps(parsed_data, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
