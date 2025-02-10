#!/usr/bin/env python3
"""
example_advanced_stats.py

This script demonstrates how to use the AdvancedStats API together with
the parsing functions while enforcing a timeout on the websocket connection.
"""

import asyncio
import json
from nhlpy.api.advanced_stats import AdvancedStats, AdvancedStatsConfig
from nhlpy.utils.cookies import get_nhl_edge_cookies
from nhlpy.parsers.advanced_stats_parsers import parse_message

async def main():
    print("Retrieving cookies from NHL Edge...")
    cookies = get_nhl_edge_cookies(headless=True)
    
    config = AdvancedStatsConfig(
        player_id="8478439",  # Replace with the desired player ID.
        season="20242025",
        stage="regular",
        units="imperial",
        cookies=cookies,
        manpower="all",
        shootingmetrics="shots"
    )
    
    adv_stats = AdvancedStats(config)
    
    try:
        # Wait at most 3 second for messages. Adjust the timeout as needed.
        raw_messages = await asyncio.wait_for(adv_stats.connect_and_listen(), timeout=3)
    except asyncio.TimeoutError:
        raw_messages = adv_stats.messages_received

    # Parse in-memory messages directly
    parsed_data = {}
    for msg in raw_messages:
        parsed_data.update(parse_message(msg))
    
    print(json.dumps(parsed_data, indent=2))

if __name__ == "__main__":
    asyncio.run(main())