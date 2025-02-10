#!/usr/bin/env python3
"""
advanced_stats_goalie_parsers.py

This module provides functionality for parsing raw NHL EDGE goalie statistics
from HTML messages received via websockets.
"""

import json
from bs4 import BeautifulSoup
from html import unescape

# Mapping dictionaries for goalie sections

goalie_overview_mapping = {
    "GAA": "gaa",
    "Overall Save %": "overallSavePct",
    "High Danger Save %": "highDangerSavePct",
    "Mid-Range Save %": "midRangeSavePct",
    "Pct. Games > .900": "pctGamesOver900",
    "Goal Diff. Per 60": "goalDifPer60",
    "Goals For Average": "goalsForAvg",
    "Points %": "pointsPct"
}

goalie_gsaves_mapping = {
    "Goals Against": "goalsAgainst",
    "Saves": "saves",
    "Shots Against": "shotsAgainst",
    "Save %": "savePct"
}

# Updated support mapping: keys must match the HTML exactly.
goalie_support_mapping = {
    "Goals For": "goalsFor",
    "Goals Against": "goalsAgainst",
    "Differential": "goalDifferential"
}

goalie_avggames_mapping = {
    "Games > .900": "gamesOver900",
    "Pct. Games > .900": "pctGamesOver900"
}

def parse_html_section(html, mapping):
    """
    Parses a table from the HTML (wrapped in a dummy <div>) using the lxml parser.
    Returns a dictionary with each metric split into:
      - player's value
      - league average
      - percentile.
    """
    soup = BeautifulSoup(f"<div>{html}</div>", "lxml")
    section_data = {}

    table = soup.find("table")
    if not table:
        return section_data

    tbody = table.find("tbody")
    if not tbody:
        return section_data

    rows = tbody.find_all("tr")
    for row in rows:
        cells = row.find_all(["td", "th"])
        if len(cells) < 4:
            continue

        label = cells[0].get_text(strip=True)
        if label not in mapping:
            continue
        key_base = mapping[label]

        player_value = cells[1].get_text(strip=True)
        league_average = cells[2].get_text(strip=True)
        percentile = cells[3].get_text(strip=True)

        section_data[key_base] = player_value
        section_data[key_base + "LeagueAverage"] = league_average
        section_data[key_base + "Percentile"] = percentile

    return section_data

def parse_shotchart(html):
    """
    Searches the HTML (wrapped in a dummy <div> and parsed using lxml) for the shot chart
    element (identified by its unique id "gsaves-shotchart") and extracts its JSON data.
    For each entry in the "chartData" array, a new key is built (e.g. "shotChartCrease")
    with its corresponding "valueLabel".
    """
    soup = BeautifulSoup(f"<div>{html}</div>", "lxml")
    # Locate the shot chart element by its unique id for goalies
    shotchart = soup.find("sl-webc-shot-chart", id="gsaves-shotchart")
    if not shotchart:
        return {}
    data_json = shotchart.get("data-json", "")
    data_json = unescape(data_json)
    try:
        shotchart_obj = json.loads(data_json)
    except Exception as e:
        print("Error parsing shotchart JSON:", e)
        return {}
    shot_data = {
        "shotChart" + entry.get("zone"): entry.get("valueLabel")
        for entry in shotchart_obj.get("chartData", [])
        if entry.get("zone")
    }
    return shot_data

def parse_getlabel(data):
    """
    Extracts player/season metadata from a 'getLabel' JSON message.
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
    getlabel_data["gamesPlayed"] = player.get("gamesPlayed")
    # Additional goalie-specific metadata can be added here if needed.
    return getlabel_data

def parse_message(data):
    """
    Processes a raw message and returns a dictionary containing the parsed data.
    For HTML messages, it parses the content based on the target.
    For the gsaves section, it also extracts shotchart information.
    """
    # Guard against None messages.
    if data is None:
        return {}
    msg_type = data.get("type")
    if msg_type == "getLabel":
        return {"getLabel": parse_getlabel(data)}
    elif msg_type == "html":
        target = data.get("target", "").lstrip("#")
        if target == "goverview-section-content":
            section_data = parse_html_section(data.get("html", ""), goalie_overview_mapping)
            return {target: section_data}
        elif target == "gsaves-section-content":
            section_data = parse_html_section(data.get("html", ""), goalie_gsaves_mapping)
            # Additionally, extract shotchart data from the gsaves section.
            shotchart_data = parse_shotchart(data.get("html", ""))
            section_data.update(shotchart_data)
            return {target: section_data}
        elif target == "support-section-content":
            section_data = parse_html_section(data.get("html", ""), goalie_support_mapping)
            return {target: section_data}
        elif target == "avggames-section-content":
            section_data = parse_html_section(data.get("html", ""), goalie_avggames_mapping)
            return {target: section_data}
    return {}

def parse_messages(raw_messages):
    """
    Processes a list of raw messages and returns a unified dictionary with all parsed data.
    """
    parsed_data = {}
    for msg in raw_messages:
        parsed_data.update(parse_message(msg))
    return parsed_data

# For testing purposes when running this file directly:
if __name__ == "__main__":
    from pprint import pprint
    # For a quick test, you can load raw messages from a JSON file.
    # Usage: python advanced_stats_goalie_parsers.py <raw_messages.json>
    import sys
    if len(sys.argv) < 2:
        print("Usage: advanced_stats_goalie_parsers.py <raw_messages.json>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_messages = json.load(f)
    parsed = parse_messages(raw_messages)
    pprint(parsed)