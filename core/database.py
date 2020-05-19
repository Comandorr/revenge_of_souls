"""
Source file contains methods that get something from database
"""


import sqlite3
import logging

from typing import List, Union

from core.units import Human, Orc, Demon
from core.items import Weapon, Armor, Utility, Shield
from core.cities import City

CONN = sqlite3.connect('ros.db')

logging.basicConfig(filename='ros.log', level=logging.DEBUG)


def get_text_from_db(story_part: str) -> str:
    """
    Get text from database where part's name equals story_part
    :param story_part:
    :return text:
    """
    if '_' in story_part:
        story_part.replace('_', ' ')
    cursor = CONN.cursor()
    try:
        cursor.execute("SELECT text FROM plot WHERE part=?", (story_part,))
    except sqlite3.OperationalError:
        raise sqlite3.OperationalError("Database is corrupted")
    result = cursor.fetchone()
    cursor.close()
    text = result[0]
    return text


def get_unit_from_db(unit_name: str) -> Union[Orc, Human, Demon]:
    """
    Get unit from database where unit's name equals unit_name
    :param unit_name:
    :return:
    """
    if '_' in unit_name:
        unit_name.replace('_', ' ')
    cursor = CONN.cursor()
    try:
        cursor.execute("SELECT * FROM units WHERE name=?", (unit_name,))
    except sqlite3.OperationalError:
        raise sqlite3.OperationalError("Database is corrupted")
    result = cursor.fetchone()
    if result is None:
        raise sqlite3.OperationalError("Unknown Unit Name")
    races = {
        "Human": Human,
        "Orc": Orc,
        "Demon": Demon
    }
    class_name = races.get(result[0], None)
    unit_info = list(result)
    unit_info.pop(0)
    unit_info[7] = get_item_from_db(unit_info[7])
    unit_info[8] = get_item_from_db(unit_info[8])
    unit_info[9] = get_item_from_db(unit_info[9])
    unit = class_name(unit_info)
    return unit


def get_item_from_db(item_name: str) -> Union[
        None, Shield, Weapon, Armor, Utility]:
    """
    Get item from database where item's name equals item_name
    :param item_name:
    :return item:
    """
    cursor = CONN.cursor()
    if item_name is None:
        return None
    if '_' in item_name:
        # Replacing underscores in item_name
        item_name = item_name.replace("_", " ")
    try:
        cursor.execute("SELECT * FROM items WHERE name=?", (item_name,))
    except sqlite3.OperationalError:
        # No ros.db
        raise sqlite3.OperationalError("Database is corrupted")
    result = cursor.fetchone()
    if result is None:
        # Wrong item_name
        raise sqlite3.OperationalError("Unknown item")
    cursor.close()
    item_types = {
        "Weapon": Weapon,
        "Utility": Utility,
        "Armor": Armor,
        "Shield": Shield,
    }
    # Choosing what are we creating
    # Weapon, Utility, Armor or Shield
    item_class = item_types.get(result[6], None)
    item_info = list(result)
    item_info.pop(6)  # Removing item type
    item = item_class(item_info)
    return item


def get_city_from_db(city_name: str) -> City:
    """
    Get city from database where city's name equals city_name
    :param city_name:
    :return city:
    """
    cursor = CONN.cursor()
    try:
        cursor.execute("SELECT * FROM cities WHERE name=?", (city_name,))
    except sqlite3.OperationalError:
        # No ros.db
        raise sqlite3.OperationalError("Database is corrupted")
    result = cursor.fetchone()
    if result is None:
        # Wrong city name
        raise sqlite3.OperationalError("Unknown city name")
    city_info = list(result)
    if city_info[3] is not None:
        # If city_items is not None
        city_info[3] = city_info[3].split()
    if city_info[4] is not None:
        # If city_missions is not None
        city_info[4] = city_info[4].split()
    city = City(city_info)
    return city


def get_list_of_cities() -> List[tuple]:
    """
    Get list of all cities from database
    :return cities:
    """
    cursor = CONN.cursor()
    try:
        cursor.execute("SELECT name FROM cities")
    except sqlite3.OperationalError:
        raise sqlite3.OperationalError("Database is corrupted")
    result = cursor.fetchall()
    cursor.close()
    if result is None:
        raise sqlite3.OperationalError("Error getting cities")
    return list(result)


def get_mission_from_db(mission_name: str) -> dict:
    """
    Get mission from database where mission's name equals mission_name
    """
    cursor = CONN.cursor()
    try:
        cursor.execute("SELECT * FROM missions WHERE name=?", (mission_name,))
    except sqlite3.OperationalError:
        raise sqlite3.OperationalError("Database is corrupted")
    result = cursor.fetchone()
    if not result:
        raise sqlite3.OperationalError("Unknown mission name")
    cursor.close()
    mission = {
        'db_name': result[0],
        'name': result[1],
        'description': result[2],
        'enemies': result[3],
        'reward': result[4],
        'reward_experience': result[5],
        'event': result[6],
        'opened': result[7],
        'done': False,
    }
    return mission


def get_event_from_db(event_name: str) -> dict:
    """
    Get event dictionary from database where event's name equals event_name
    """
    cursor = CONN.cursor()
    try:
        cursor.execute("SELECT * FROM events WHERE name=?", (event_name,))
    except sqlite3.OperationalError:
        raise sqlite3.OperationalError("Database is corrupted")
    result = cursor.fetchone()
    if not result:
        raise sqlite3.OperationalError("Error getting event")
    cursor.close()
    event = {
        "name": result[0],
        "type": result[1],
        "target": result[2],
        "text": result[3]
    }

    return event
