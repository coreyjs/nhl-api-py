import asyncio
import json
from nhlpy.api.advanced_stats import AdvancedStats, AdvancedStatsConfig, get_nhl_edge_cookies

def main():
    # Option 1: Retrieve cookies dynamically using Selenium.
    cookies = get_nhl_edge_cookies(headless=True)

    # Option 2: If you already have cookie values, you can set them manually:
    # cookies = {
    #     "AWSALB": "your_value",
    #     "AWSALBCORS": "your_value",
    #     "__cf_bm": "your_value",
    #     "OptanonConsent": "your_value"
    # }

    # Specify the player ID along with other configuration details.
    config = AdvancedStatsConfig(
        player_id="8478439",
        season="20242025",
        stage="regular",
        units="imperial",
        cookies=cookies  # Pass in the retrieved cookies.
    )

    adv_stats = AdvancedStats(config)
    
    # Run the asynchronous websocket connection and get the messages.
    messages = asyncio.run(adv_stats.connect_and_listen())
    
    # Save the messages as a JSON file.
    output_filename = "advanced_stats_output.json"
    try:
        with open(output_filename, "w") as outfile:
            json.dump(messages, outfile, indent=2)
        print(f"Saved messages to {output_filename}")
    except Exception as e:
        print(f"Error saving messages: {e}")

if __name__ == "__main__":
    main()