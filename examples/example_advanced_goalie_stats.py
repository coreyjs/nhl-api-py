#!/usr/bin/env python3
"""
example_advanced_goalie_stats.py

This script demonstrates how to use the AdvancedStatsGoalie API together with
the goalie parsing functions while enforcing a timeout on the websocket connection.
It calls for goalie data using a default goalie (player_id "8476945") and prints out the JSON.
"""

import asyncio
import json
from nhlpy.api.advanced_stats import GoalieStats, GoalieStatsConfig
from nhlpy.utils.cookies import get_nhl_edge_cookies
from nhlpy.parsers.advanced_parsers import parse_message_goalie

async def main():
    print("Retrieving cookies from NHL Edge...")
    cookies = get_nhl_edge_cookies(headless=True)
    
    # Use the goalie player ID from the provided URL.
    config = GoalieStatsConfig(
        player_id="8476945",  # Default goalie ID from https://edge.nhl.com/en/goalie/8476945
        season="20242025",
        stage="regular",
        units="imperial",
        cookies=cookies
    )
    
    adv_stats = GoalieStats(config)
    
    try:
        # Wait at most 3 seconds for messages. Adjust the timeout as needed.
        raw_messages = await asyncio.wait_for(adv_stats.connect_and_listen(), timeout=3)
    except asyncio.TimeoutError:
        raw_messages = adv_stats.messages_received

    # Print the raw messages to inspect what was received.
    # print("Raw messages:")
    # print(json.dumps(raw_messages, indent=2))
    
    # Parse in-memory messages using the goalie parser.
    parsed_data = {}
    for msg in raw_messages:
        parsed_data.update(parse_message_goalie(msg))
    
    print("Parsed JSON:")
    print(json.dumps(parsed_data, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
