"""
Source file contains all story methods of the game
"""


from . import database
from . import menus
from . import units


def prologue():
    """ Hello, Wanderer! My name is Ezra, I am the King of Lux Patria Kingdom!
    Right now there isn't a war over here. But 10 years ago, we were in the
    middle of conflict between 3 kingdoms: Incedium, Rebus and Frigidum.
    I want to tell you a story about the greatest War in history of Vitae.
    I was just a private of Incedium scout squad.
    """
    initial_story()


def initial_story():
    """
    Initial story of the game
    """
    # Text
    player = units.Player("Rahel")  # Create player object
    # Get a few vikings from database
    viking_test = database.get_unit_from_db('Viking')
    another_viking = database.get_unit_from_db('Viking')
    viking = database.get_unit_from_db('Viking')
    # Add Salve to player's backpack
    player.add_item_to_backpack(database.get_item_from_db(
        "Small_Healing_Salve",
    ))
    player.add_item_to_backpack(database.get_item_from_db(
        "Test_buckler"
    ))
    # Begin fight between player and 3 vikings
    menus.fight_menu(player, [viking_test, another_viking, viking])
    menus.chilling_menu(player)  # Main menu after fight
