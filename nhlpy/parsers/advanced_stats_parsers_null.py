#!/usr/bin/env python3
import json
import os
import glob
from pprint import pprint
from bs4 import BeautifulSoup

# Directory where the JSON files are stored.
DATA_DIR = "/Users/harrisgordon/Documents/Development/Python/data/8478439/"

# Mapping dictionaries: for each HTML target (without the leading "#"),
# map the table row label (as it appears in the HTML) to a base key.
section_mappings = {
    "overview-section-content": {
        "Top Skating Speed (mph)": "topSkatingSpeed",
        "Speed Bursts Over 20 mph": "speedBurstsOver22mph",
        "Skating Distance (mi)": "skatingDistance",
        "Top Shot Speed (mph)": "topShotSpeed",
        "Shots on Goal": "shotsOnGoal",
        "Shooting %": "shootingpct",
        "Goals": "goals",
        "Off. Zone Time (ES)": "offZoneTimeES"
    },
    "skatingspeed-section-content": {
        "Top Speed (mph)": "topSkatingSpeed",
        "22+ mph bursts": "speedBurstsOver22mph",
        "20-22 mph bursts": "speedBurstsOver2022mph",
        "18-20 mph bursts": "speedBurstsOver1820"
    },
    "skatingdistance-section-content": {
        "Total (mi)": "totalDistance",
        "Average Per 60 (mi)": "averagePer60",
        "Top Game (mi)": "topGameDistance",
        "Top Period (mi)": "topPeriodDistance"
    },
    "shotspeed-section-content": {
        "Top Speed (mph)": "topShotSpeed",
        "Average Speed (mph)": "averageShotSpeed",
        "100+ mph shots": "shotsOver100mph",
        "90-100 mph shots": "shotsOver90100mph",
        "80-90 mph shots": "shotsOver8090mph",
        "70-80 mph shots": "shotOver7080mph"
    },
    "shotlocation-section-content": {
        "Shots on Goal": "shotsOnGoal",
        "Goals": "goals",
        "Shooting %": "shootingpct"
    },
    "zonetime-section-content": {
        "Offensive Zone": "offZonePct",
        "Neutral Zone": "neuZonePct",
        "Defensive Zone": "defZonePct"
    }
}


def parse_html_section(html, mapping):
    """
    Given an HTML string (which contains a table) and a mapping dictionary,
    parse the table and return a dictionary where each metric is split into three keys:
    the player's value, league average, and percentile.
    """
    soup = BeautifulSoup(html, "html.parser")
    section_data = {}
    
    # Find the first table in the HTML.
    table = soup.find("table")
    if not table:
        return section_data

    tbody = table.find("tbody")
    if not tbody:
        return section_data

    rows = tbody.find_all("tr")
    for row in rows:
        # Expecting each row to have one label cell and three value cells.
        cells = row.find_all(["td", "th"])
        if len(cells) < 4:
            continue

        # The first cell contains the label.
        label = cells[0].get_text(strip=True)
        if label not in mapping:
            continue
        key_base = mapping[label]

        # The next three cells are: player's value, league average, and percentile.
        player_value = cells[1].get_text(strip=True)
        league_average = cells[2].get_text(strip=True)
        percentile = cells[3].get_text(strip=True)

        section_data[key_base] = player_value
        section_data[key_base + "LeagueAverage"] = league_average
        section_data[key_base + "Percentile"] = percentile

    return section_data


def parse_getlabel(data):
    """
    Extract the player/season metadata from a 'getLabel' JSON message.
    """
    getlabel_data = {}
    params = data.get("params", {})
    player = data.get("player", {})

    getlabel_data["season"] = params.get("season")
    getlabel_data["stage"] = params.get("stage")
    getlabel_data["playerId"] = params.get("player")
    getlabel_data["team"] = player.get("team")
    getlabel_data["firstName"] = player.get("firstName")
    getlabel_data["lastName"] = player.get("lastName")
    getlabel_data["position"] = player.get("position")
    getlabel_data["laterality"] = player.get("laterality")
    getlabel_data["jerseyNumber"] = player.get("jerseyNumber")
    getlabel_data["averageKey"] = player.get("averageKey")
    getlabel_data["gamesPlayed"] = player.get("gamesPlayed")
    getlabel_data["goals"] = player.get("goals")
    getlabel_data["assists"] = player.get("assists")
    getlabel_data["points"] = player.get("points")

    return getlabel_data


def main():
    final_result = {}

    # Process each JSON file in the specified directory.
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    for file_path in json_files:
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding {file_path}: {e}")
                continue

        msg_type = data.get("type")
        if msg_type == "getLabel":
            # Process getLabel JSON
            final_result["getLabel"] = parse_getlabel(data)
        elif msg_type == "html":
            # Process HTML JSON; remove the leading '#' from the target
            target = data.get("target", "").lstrip("#")
            if target in section_mappings:
                section_data = parse_html_section(data.get("html", ""), section_mappings[target])
                final_result[target] = section_data

    # Print the final nested dictionary structure.
    pprint(final_result)


if __name__ == "__main__":
    main()