#!/usr/bin/env python3
"""
advanced_parsers_team.py

This module provides parsing functions for advanced NHL team statistics.
It reuses the same section mappings (and thus metrics) as the player parser,
but adapts the getLabel parsing and any team-specific data extraction.
"""

import json
from pprint import pprint
from bs4 import BeautifulSoup
from html import unescape

# Use the same section mappings as in the original script.
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
    Parses a table from the HTML (wrapped in a dummy <div>) using lxml.
    Returns a dictionary with each metric split into:
      - player's/team's value
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

        value = cells[1].get_text(strip=True)
        league_average = cells[2].get_text(strip=True)
        percentile = cells[3].get_text(strip=True)

        section_data[key_base] = value
        section_data[key_base + "LeagueAverage"] = league_average
        section_data[key_base + "Percentile"] = percentile

    return section_data


def parse_shotchart(html):
    """
    Searches the HTML (wrapped in a dummy <div>) for the shot chart element
    (identified by its id "shotlocation-shotchart") and extracts its JSON data.
    For each entry in the "chartData" array, a new key is built (e.g. "shotChartCrease")
    with its corresponding "valueLabel".
    """
    soup = BeautifulSoup(f"<div>{html}</div>", "lxml")
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


def parse_getlabel_team(data):
    """
    Extracts team/season metadata from a 'getLabel' JSON message.
    Assumes the team message contains a "team" key.
    """
    getlabel_data = {}
    params = data.get("params", {})
    team = data.get("team", {})

    getlabel_data["season"] = params.get("season")
    getlabel_data["stage"] = params.get("stage")
    # For teams, the identifier comes from either params or the team object.
    getlabel_data["teamId"] = params.get("team") or team.get("id")
    getlabel_data["teamName"] = team.get("name")
    getlabel_data["location"] = team.get("location")
    getlabel_data["wins"] = team.get("wins")
    getlabel_data["losses"] = team.get("losses")
    getlabel_data["otl"] = team.get("otl")
    return getlabel_data


def parse_message_team(data):
    """
    Processes a raw team message and returns a dictionary containing the parsed data.
    Uses the same section_mappings as the original parser, but handles known alias targets.
    """
    # If data is None or not a dict, return an empty dict.
    if not data or not isinstance(data, dict):
        return {}
        
    msg_type = data.get("type")
    if msg_type == "getLabel":
        return {"getLabel": parse_getlabel_team(data)}
    elif msg_type == "html":
        target = data.get("target", "").lstrip("#")
        # Handle alias: if target is "skating-section-content", treat it as "skatingspeed-section-content"
        if target == "skating-section-content":
            target = "skatingspeed-section-content"
        if target in section_mappings:
            section_data = parse_html_section(data.get("html", ""), section_mappings[target])
            # If this is the shot location section, add shot chart data.
            if target == "shotlocation-section-content":
                shotchart_data = parse_shotchart(data.get("html", ""))
                section_data.update(shotchart_data)
            return {target: section_data}
    return {}

def parse_messages_team(raw_messages):
    """
    Processes a list of raw team messages and returns a unified dictionary with all parsed data.
    Instead of replacing data for a target if a later message is empty, it only updates when new data is present.
    """
    parsed_data = {}
    for msg in raw_messages:
        parsed_msg = parse_message_team(msg)
        for key, value in parsed_msg.items():
            # Only update if the new value is non-empty.
            if value:
                if key in parsed_data:
                    # If both current and new value are dictionaries, merge them.
                    if isinstance(parsed_data[key], dict) and isinstance(value, dict):
                        parsed_data[key].update(value)
                    else:
                        parsed_data[key] = value
                else:
                    parsed_data[key] = value
    return parsed_data


# For testing purposes when running this script directly:
if __name__ == "__main__":
    # Sample team messages for testing.
    sample_team_messages = [
        {
            "type": "getLabel",
            "params": {
                "season": "20242025",
                "stage": "regular",
                "team": "PHI",
                "rootName": "teamsProfiles",
                "source": "teams"
            },
            "team": {
                "name": "Flyers",
                "location": "Philadelphia",
                "id": 4,
                "wins": 24,
                "losses": 26,
                "otl": 7
            },
            "id": "PHI"
        },
        {
            "type": "html",
            "target": "#overview-section-content",
            "html": """
                <table>
                  <tbody>
                    <tr>
                      <td>Top Skating Speed (mph)</td>
                      <td>28.5</td>
                      <td>26.2</td>
                      <td>90</td>
                    </tr>
                    <tr>
                      <td>Speed Bursts Over 20 mph</td>
                      <td>15</td>
                      <td>12</td>
                      <td>80</td>
                    </tr>
                  </tbody>
                </table>
            """,
            "callback": "initializeDataElements"
        }
    ]

    parsed = parse_messages_team(sample_team_messages)
    pprint(parsed)