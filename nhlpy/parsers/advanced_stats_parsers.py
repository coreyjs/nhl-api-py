#!/usr/bin/env python3
import json
import os
import glob
from pprint import pprint
from bs4 import BeautifulSoup
from html import unescape

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
    element (identified by its id "shotlocation-shotchart") and extracts its JSON data.
    For each entry in the "chartData" array, a new key is built (e.g. "shotChartCrease")
    with its corresponding "valueLabel".
    """
    soup = BeautifulSoup(f"<div>{html}</div>", "lxml")
    # Locate the shot chart element by its unique id
    shotchart = soup.find("sl-webc-shot-chart", id="shotlocation-shotchart")
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
    getlabel_data["averageKey"] = player.get("averageKey")
    getlabel_data["gamesPlayed"] = player.get("gamesPlayed")
    getlabel_data["goals"] = player.get("goals")
    getlabel_data["assists"] = player.get("assists")
    getlabel_data["points"] = player.get("points")

    return getlabel_data


def parse_message(data):
    """
    Processes a raw message and returns a dictionary containing the parsed data.
    For HTML messages, if the target is "shotlocation-section-content", it will also
    extract the shot chart information.
    """
    msg_type = data.get("type")
    if msg_type == "getLabel":
        return {"getLabel": parse_getlabel(data)}
    elif msg_type == "html":
        target = data.get("target", "").lstrip("#")
        if target in section_mappings:
            section_data = parse_html_section(data.get("html", ""), section_mappings[target])
            # Add shot chart info if this is the shot location section.
            if target == "shotlocation-section-content":
                shotchart_data = parse_shotchart(data.get("html", ""))
                section_data.update(shotchart_data)
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
    final_result = {}
    pprint(final_result)