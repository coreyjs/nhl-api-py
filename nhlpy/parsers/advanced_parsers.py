#!/usr/bin/env python3
"""
Combined Advanced Parsers for NHL Statistics

This module provides functions to parse raw HTML/JSON messages (as received
via websockets) and extract advanced statistics. It supports three modes:

  - "goalie":  for advanced goalie stats
  - "player":  for advanced player (non-goalie) stats
  - "team":    for advanced team stats

Usage:
    python combined_advanced_parsers.py <mode: goalie|player|team> <raw_messages.json>
"""

import json
from bs4 import BeautifulSoup
from html import unescape


# -----------------------------------------------------------------------------
# Common Utility Functions
# -----------------------------------------------------------------------------

def parse_html_section(html, mapping):
    """
    Given an HTML snippet containing a table and a mapping dictionary,
    extract the data into a dictionary.
    
    Each table row is assumed to have at least four cells:
      - label (must match a key in mapping)
      - value
      - league average
      - percentile
      
    The returned dictionary will contain keys for the value, league average,
    and percentile (with "LeagueAverage" and "Percentile" appended to the base key).
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


def parse_shotchart(html, shotchart_id):
    """
    Looks for the shot chart element (with a given id) in the HTML and
    returns a dictionary with the shot chart data.
    
    For each entry in the shot chart's "chartData" array, a key is built as
      "shotChart" + <zone>
    and its corresponding "valueLabel" is stored.
    """
    soup = BeautifulSoup(f"<div>{html}</div>", "lxml")
    shotchart = soup.find("sl-webc-shot-chart", id=shotchart_id)
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


# -----------------------------------------------------------------------------
# Mapping Dictionaries
# -----------------------------------------------------------------------------

# For advanced goalie stats (the keys here match the HTML exactly)
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
goalie_support_mapping = {
    "Goals For": "goalsFor",
    "Goals Against": "goalsAgainst",
    "Differential": "goalDifferential"
}
goalie_avggames_mapping = {
    "Games > .900": "gamesOver900",
    "Pct. Games > .900": "pctGamesOver900"
}

# For advanced player (non-goalie) and team stats the HTML sections share the same mappings:
player_team_section_mappings = {
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


# -----------------------------------------------------------------------------
# getLabel Parsers
# -----------------------------------------------------------------------------

def parse_getlabel_goalie(data):
    """
    Extract goalie-specific metadata from a getLabel message.
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
    return getlabel_data


def parse_getlabel_player(data):
    """
    Extract player-specific metadata from a getLabel message.
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


def parse_getlabel_team(data):
    """
    Extract team-specific metadata from a getLabel message.
    """
    getlabel_data = {}
    params = data.get("params", {})
    team = data.get("team", {})
    getlabel_data["season"] = params.get("season")
    getlabel_data["stage"] = params.get("stage")
    getlabel_data["teamId"] = params.get("team") or team.get("id")
    getlabel_data["teamName"] = team.get("name")
    getlabel_data["location"] = team.get("location")
    getlabel_data["wins"] = team.get("wins")
    getlabel_data["losses"] = team.get("losses")
    getlabel_data["otl"] = team.get("otl")
    return getlabel_data


# -----------------------------------------------------------------------------
# Message Parsers by Mode
# -----------------------------------------------------------------------------

def parse_message_goalie(data):
    """
    Parse a single message (JSON dict) for goalie advanced stats.
    """
    if data is None:
        return {}
    msg_type = data.get("type")
    if msg_type == "getLabel":
        return {"getLabel": parse_getlabel_goalie(data)}
    elif msg_type == "html":
        target = data.get("target", "").lstrip("#")
        if target == "goverview-section-content":
            section_data = parse_html_section(data.get("html", ""), goalie_overview_mapping)
            return {target: section_data}
        elif target == "gsaves-section-content":
            section_data = parse_html_section(data.get("html", ""), goalie_gsaves_mapping)
            # Use the goalie-specific shotchart id
            shotchart_data = parse_shotchart(data.get("html", ""), "gsaves-shotchart")
            section_data.update(shotchart_data)
            return {target: section_data}
        elif target == "support-section-content":
            section_data = parse_html_section(data.get("html", ""), goalie_support_mapping)
            return {target: section_data}
        elif target == "avggames-section-content":
            section_data = parse_html_section(data.get("html", ""), goalie_avggames_mapping)
            return {target: section_data}
    return {}


def parse_message_player(data):
    """
    Parse a single message (JSON dict) for player (non-goalie) advanced stats.
    """
    msg_type = data.get("type")
    if msg_type == "getLabel":
        return {"getLabel": parse_getlabel_player(data)}
    elif msg_type == "html":
        target = data.get("target", "").lstrip("#")
        if target in player_team_section_mappings:
            section_data = parse_html_section(data.get("html", ""), player_team_section_mappings[target])
            # For the shot location section, add shotchart data.
            if target == "shotlocation-section-content":
                shotchart_data = parse_shotchart(data.get("html", ""), "shotlocation-shotchart")
                section_data.update(shotchart_data)
            return {target: section_data}
    return {}


def parse_message_team(data):
    """
    Parse a single message (JSON dict) for team advanced stats.
    Note: some team messages alias "skating-section-content" to "skatingspeed-section-content".
    """
    if not data or not isinstance(data, dict):
        return {}
    msg_type = data.get("type")
    if msg_type == "getLabel":
        return {"getLabel": parse_getlabel_team(data)}
    elif msg_type == "html":
        target = data.get("target", "").lstrip("#")
        if target == "skating-section-content":
            target = "skatingspeed-section-content"
        if target in player_team_section_mappings:
            section_data = parse_html_section(data.get("html", ""), player_team_section_mappings[target])
            if target == "shotlocation-section-content":
                shotchart_data = parse_shotchart(data.get("html", ""), "shotlocation-shotchart")
                section_data.update(shotchart_data)
            return {target: section_data}
    return {}


def parse_messages(raw_messages, mode="player"):
    """
    Process a list of raw messages and return a single dictionary containing all parsed data.
    
    The mode parameter should be one of:
      - "goalie"  for goalie advanced stats,
      - "player"  for player (non-goalie) advanced stats,
      - "team"    for team advanced stats.
    """
    parsed_data = {}
    for msg in raw_messages:
        if mode == "goalie":
            parsed_msg = parse_message_goalie(msg)
        elif mode == "team":
            parsed_msg = parse_message_team(msg)
        else:
            parsed_msg = parse_message_player(msg)
        # Merge parsed_msg into parsed_data
        for key, value in parsed_msg.items():
            if value:
                if key in parsed_data and isinstance(parsed_data[key], dict) and isinstance(value, dict):
                    parsed_data[key].update(value)
                else:
                    parsed_data[key] = value
    return parsed_data


# -----------------------------------------------------------------------------
# Main (for testing/demo purposes)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    from pprint import pprint

    if len(sys.argv) < 3:
        print("Usage: combined_advanced_parsers.py <mode: goalie|player|team> <raw_messages.json>")
        sys.exit(1)

    mode = sys.argv[1]
    filename = sys.argv[2]

    with open(filename, "r") as f:
        raw_messages = json.load(f)

    result = parse_messages(raw_messages, mode)
    pprint(result)