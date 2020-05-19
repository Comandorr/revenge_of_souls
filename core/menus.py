"""
Source file contains all menu methods of the game
"""


import sys
import time
import os
import pickle

from typing import List, TypeVar

from prettytable import PrettyTable

from core import console, database, items, story, units, DeadHero
from core.cities import City


T = TypeVar('T')


def get_input(return_type: T) -> T:
    message = 'Only numbers are allowed'
    flag = True
    if T == str:
        message = 'Only words are allowed'
        flag = False
    try:
        if flag:
            return int(input())
        else:
            return input()
    except ValueError:
        print(message)
        return get_input(return_type)


def main_menu():
    """
    Entering game menu
    """
    console.clear()
    print("Welcome to 'Revenge of Souls'!")
    console.print_wall()
    print("1. New Game")
    print("2. Load Game")
    print("3. Quit")
    console.print_wall()
    option = get_input(int)
    options = {
        1: story.prologue,
        2: load_game,
    }
    if not 1 <= option <= 3:
        print("There's no such choice")
        main_menu()
        return
    if option != 3:
        func = options.get(option, 3)
    else:
        sys.exit("Good bye")
    try:
        func()
    except DeadHero:
        input("Press any button to continue to main menu...")
        main_menu()
        return


def load_game():
    """
    Load game menu
    """
    saves = None
    try:
        saves = os.listdir("./Saves")
    except FileNotFoundError:
        saves = []
    if len(saves) == 0:
        print("You don't have any saves!")
    quit_num = 1
    for save_number, save_name in enumerate(saves):
        file_path = os.path.join("./Saves/", save_name)
        print("{}. {}\t{}".format(
            save_number + 1,
            save_name.replace('_', ' ') if '_' in save_name else save_name,
            time.ctime(os.path.getmtime(file_path))
        ))
        quit_num += 1
    print("%d. Quit" % quit_num)
    console.print_wall()
    print("Enter number of save:", end=" ")
    save_number = get_input(int)
    if save_number == quit_num:
        main_menu()
        return
    if not 1 <= save_number < quit_num:
        print("There's no such save file")
        load_game()
        return
    with open("./Saves/" + saves[save_number - 1], 'rb') as save:
        player = pickle.load(save)
        chilling_menu(player)


def fight_menu(player: units.Player, enemies: List[units.Unit]):
    """
    Menu that provides fight between 2 units
    """
    for enemy in enemies:
        print(
            "Your next enemy is %s" % enemy.name
        )
        in_fight_menu(player, enemy)
    dropped_items_menu(player, enemies)


def in_fight_menu(player: units.Player, enemy: units.Unit):
    """
    In fight menu. Allows to heal, print enemy, player stats and use items from
    backpack
    """
    console.print_wall()
    print("1. Continue fight")
    print("2. Heal %d" % player.count_utility_items())
    print("3. Open backpack")
    print("4. Print %s stats" % enemy.name)
    print("5. Print your stats")
    console.print_wall()
    option = get_input(int)
    if not 1 <= option <= 5:
        print("There's no such option")
        in_fight_menu(player, enemy)
        return
    if option == 1:
        units.fight(player, enemy)
    elif option == 2:
        player.heal()
        in_fight_menu(player, enemy)
        return
    elif option == 3:
        equipment_model_menu(player)
        in_fight_menu(player, enemy)
        return
    elif option == 5:
        print(player)
        in_fight_menu(player, enemy)
        return
    else:
        print(enemy)
        in_fight_menu(player, enemy)
        return


def equipment_model_menu(player: units.Player):
    """
    Provide managing of player' equipment_model.
    Such as changing items, getting equipment stats, etc.
    """
    console.print_wall()
    print("1. Get equipment stats")
    print("2. Change equipment")
    print("3. Quit")
    console.print_wall()
    option = get_input(int)
    if not 1 <= option <= 3:
        print("There's no such option")
        equipment_model_menu(player)
        return
    if option == 3:
        return
    if option == 1:
        console.clear()
        console.print_wall()
        print(player.equipment_model)
        console.print_wall()
        equipment_model_menu(player)
        return
    elif option == 2:
        equipment_model_change(player)
    equipment_model_menu(player)
    return


def equipment_model_change(player: units.Player):
    """

    :param player:
    :type player units.Player:
    :return:
    """
    console.clear()
    console.print_wall()
    print("1. Change weapon")
    print("2. Change shield")
    print("3. Change armor set")
    print("4. Quit")
    console.print_wall()
    option = get_input(int)
    if not 1 <= option <= 4:
        print("There's no such option")
        equipment_model_change(player)
        return
    if option == 4:
        return
    if option == 1:
        change_weapon_menu(player)
        return
    elif option == 2:
        change_shield_menu(player)
        return
    elif option == 3:
        change_armor_set_menu(player)
        return


def change_weapon_menu(player: units.Player):
    """

    :param player:
    :type player Player
    :return:
    """
    # TODO: Split method
    console.print_wall()
    print("1. Change current weapon")
    using_as_two_handed = False
    if player.right_hand is not None:
        print("2. Current weapon is %s. Pull it off?" %
              player.right_hand.name)
        if not player.right_hand.two_handed:
            print("3. Use weapon in two hands")
            print("4. Quit")
            using_as_two_handed = True
        else:
            print("3. Quit")
    else:
        print("2. You don't use any weapon now.")
        print("3. Quit")
    console.print_wall()
    option = get_input(int)
    if not using_as_two_handed and not 1 <= option <= 3:
        print("There's no such option")
        change_weapon_menu(player)
        return
    elif not 1 <= option <= 4:
        print("There's no such option")
        change_weapon_menu(player)
        return
    if ((option == 3 and not using_as_two_handed) or (option == 4 and
                                                      using_as_two_handed)):
        return
    if option == 1:
        available_items = list()
        quit_num = 1
        for item in player.items:
            if item.is_weapon():
                available_items.append(item)
        if len(available_items) == 0:
            print("You don't have any weapons")
            change_weapon_menu(player)
            return
        console.print_wall()
        for item_number, item in enumerate(available_items):
            print("%d. %s" % (item_number + 1, item))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of item that you wanna use:", end=" ")
        item_number = get_input(int)
        if item_number == quit_num:
            return
        item_name = ''
        try:
            item_name = available_items[item_number - 1].name
        except IndexError:
            print("There's no such item")
            change_weapon_menu(player)
            return
        try:
            player.use_item(item_name)
        except NameError:
            change_weapon_menu(player)
            return
    elif option == 2:
        if player.right_hand is not None:
            print("You stopped using %s" %
                  player.right_hand.name)
            player.stop_using(player.right_hand)
            change_weapon_menu(player)
            return
        else:
            print("You don't use any weapon. You can't pull it off")
            change_weapon_menu(player)
            return
    elif option == 3:
        if player.right_hand.two_handed:
            print("Your weapon is already two-handed")
            return
        player.right_hand.using_as_two_handed = True
        player.stop_using(player.left_hand)
        print("Now you're using %s in two hands" %
              player.right_hand.name)


def change_shield_menu(player: units.Player):
    """

    :param player:
    :return:
    """
    # TODO: Split method
    console.print_wall()
    print("1. Change shield")
    if isinstance(player.left_hand, items.Shield):
        print("2. Current shield is %s. Pull it off?" %
              player.left_hand.name)
    else:
        print("2. You don't use any shield")
    print("3. Quit")
    option = get_input(int)
    if not 1 <= option <= 3:
        print("There's no such option")
        change_shield_menu(player)
        return
    if option == 3:
        return
    if option == 1:
        available_items = list()
        quit_num = 1
        for item in player.items:
            if item.is_shield():
                available_items.append(item)
        if len(available_items) == 0:
            print("You don't have any shields!")
            change_shield_menu(player)
            return
        console.print_wall()
        for item_number, item in enumerate(available_items):
            print("%d. %s" % (item_number + 1, item))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of item that you wanna use:", end=" ")
        item_number = get_input(int)
        item_name = ''
        try:
            item_name = available_items[item_number - 1].name
        except IndexError:
            print("There's no such item")
            change_shield_menu(player)
            return
        try:
            player.use_item(item_name)
        except NameError:
            change_shield_menu(player)
            return
    elif option == 2:
        if isinstance(player.left_hand, items.Shield):
            print("You stopped using %s" %
                  player.left_hand.name)
            player.stop_using(player.left_hand)
            change_shield_menu(player)
            return
        else:
            print("You don't use any shield. You can't pull if off")
            change_shield_menu(player)
            return


def change_armor_set_menu(player: units.Player):
    """

    :param player:
    :type player units.Player
    :return:
    """
    # TODO: Split method
    console.print_wall()
    print("1. Change helmet")
    print("2  Change chest")
    print("3. Change arms")
    print("4. Change legs")
    print("5. Quit")
    console.print_wall()
    option = get_input(int)
    if not 1 <= option <= 5:
        print("There's no such option")
        change_armor_set_menu(player)
        return
    if option == 5:
        return
    if option == 1:
        available_items = list()
        quit_num = 1
        for item in player.items:
            if "Helmet" in item.type:
                available_items.append(item)
        if len(available_items) == 0:
            print("You don't have any helmets")
            change_armor_set_menu(player)
            return
        console.print_wall()
        for item_number, item in enumerate(available_items):
            print("%d. %s" % (item_number + 1, item))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of item that you wanna use:", end=" ")
        item_number = get_input(int)
        item_name = ''
        try:
            item_name = available_items[item_number - 1].name
        except IndexError:
            print("There's no such item")
            change_armor_set_menu(player)
            return
        try:
            player.use_item(item_name)
        except NameError:
            change_armor_set_menu(player)
            return
    elif option == 2:
        available_items = list()
        quit_num = 1
        for item in player.items:
            if "Chest" in item.type:
                available_items.append(item)
        if len(available_items) == 0:
            print("You don't have any chests")
            change_armor_set_menu(player)
            return
        console.print_wall()
        for item_number, item in enumerate(available_items):
            print("%d. %s" % (item_number + 1, item))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of item that you wanna use:", end=" ")
        item_number = get_input(int)
        item_name = ''
        try:
            item_name = available_items[item_number - 1].name
        except IndexError:
            print("There's no such item")
            change_armor_set_menu(player)
            return
        try:
            player.use_item(item_name)
        except NameError:
            change_armor_set_menu(player)
            return
    elif option == 3:
        available_items = list()
        quit_num = 1
        for item in player.items:
            if "Arms" in item.type:
                available_items.append(item)
        if len(available_items) == 0:
            print("You don't have any arms")
            change_armor_set_menu(player)
            return
        console.print_wall()
        for item_number, item in enumerate(available_items):
            print("%d. %s" % (item_number + 1, item))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of item that you wanna use:", end=" ")
        item_number = get_input(int)
        item_name = ''
        try:
            item_name = available_items[item_number - 1].name
        except IndexError:
            print("There's no such item")
            change_armor_set_menu(player)
            return
        try:
            player.use_item(item_name)
        except NameError:
            change_armor_set_menu(player)
            return
    elif option == 4:
        available_items = list()
        quit_num = 1
        for item in player.items:
            if "Legs" in item.type:
                available_items.append(item)
        if len(available_items) == 0:
            print("You don't have any legs")
            change_armor_set_menu(player)
            return
        console.print_wall()
        for item_number, item in enumerate(available_items):
            print("%d. %s" % (item_number + 1, item))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of item that you wanna use:", end=" ")
        item_number = get_input(int)
        item_name = ''
        try:
            item_name = available_items[item_number - 1].name
        except IndexError:
            print("There's no such item")
            change_armor_set_menu(player)
            return
        try:
            player.use_item(item_name)
        except NameError:
            change_armor_set_menu(player)
            return


def player_missions_menu(player: units.Player):
    """
    List player missions and allows player to pick mission
    """
    # TODO: Split method
    console.clear()
    console.print_wall()
    print("1. Start mission")
    print("2. Finished missions")
    print("3. Quit")
    console.print_wall()
    option = get_input(int)
    if not 1 <= option <= 3:
        print("There's no such option")
        player_missions_menu(player)
        return
    if option == 3:
        return
    if option == 1:
        console.print_wall()
        print("%s missions:" % player.name)
        console.print_wall()
        quit_num = 1
        not_finished_missions = list()
        for mission in player.missions:
            if not mission['done']:
                not_finished_missions.append(mission)
        if len(not_finished_missions) == 0:
            print("You didn't take any missions!")
        else:
            for value, mission in enumerate(not_finished_missions):
                print(value + 1)
                mission_table = PrettyTable(["What", "Values"])
                mission_table.add_row(["Name", mission['name']])
                mission_table.add_row(["Description", mission['description']])
                mission_table.add_row(["Reward",
                                       (str(mission['reward']) + ' gold')])
                print(mission_table)
                quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        option = get_input(int)
        if option == quit_num:
            return
        else:
            try:
                mission = not_finished_missions[option - 1]
            except IndexError:
                print("There's no such mission")
                player_missions_menu(player)
                return
            player.current_city = None
            mission_menu(player, mission)
            return
    elif option == 2:
        finished_missions = list()
        for mission in player.missions:
            if mission['done']:
                finished_missions.append(mission)
        console.print_wall()
        if len(finished_missions) == 0:
            print("You don't have any finished missions")
        else:
            for value, mission in enumerate(finished_missions):
                print(value + 1)
                mission_table = PrettyTable(["What", "Values"])
                mission_table.add_row(["Name", mission['name']])
                mission_table.add_row(["Description", mission['description']])
                mission_table.add_row(["Reward",
                                       (str(mission['reward']) + ' gold')])
                print(mission_table)
        print("To quit press something ..")
        console.print_wall()
        input()
        player_missions_menu(player)
        return


def mission_menu(player: units.Player, mission: dict):
    """
    Menu for player' current mission
    :param player
    :type player units.Player
    :param mission
    :type mission dict
    """
    player.begin_mission(mission)
    enemies = list()
    enemies_split = mission['enemies'].split(' ')
    for enemy in enemies_split:
        unit = database.get_unit_from_db(enemy)
        enemies.append(unit)
    fight_menu(player, enemies)
    if player.is_alive():
        mission_index = player.missions.index(mission)
        player.missions[mission_index]['done'] = True
        print("Mission complete! To get a reward comeback to %s" %
              mission['city'])


def dropped_items_menu(player: units.Player, enemies: List[units.Unit]):
    """
    Control item dropping process
    :param player:
    :param enemies:
    :type enemies list[units.Unit]
    :return:
    """
    # TODO: Split method
    dropped_items = list()
    for enemy in enemies:
        armor_set = enemy.create_armor_set()
        if enemy.right_hand:
            dropped_items.append(enemy.right_hand)
        if len(armor_set) > 0:
            for item in armor_set:
                dropped_items.append(item)
        if isinstance(enemy.left_hand, items.Shield):
            dropped_items.append(enemy.left_hand)
    if len(dropped_items) < 1:
        return
    print("There's %d dropped items. Do you wanna look on them?" %
          len(dropped_items))
    print("1. Yes\n2. No\n3. Take 'em all")
    option = get_input(int)
    if not 1 <= option <= 3:
        print("There's no such option")
        dropped_items_menu(player, enemies)
        return
    if option == 1:
        console.print_wall()
        quit_num = 1
        for value, item in enumerate(dropped_items):
            print("{}. {}".format(
                value + 1,
                item
            ))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter numbers of items that you wanna take:", end=' ')
        numbers = input().split()
        for num in numbers:
            if not 1 <= int(num) < quit_num:
                print("There's no such item")
                dropped_items_menu(player, enemies)
                return
        for number in numbers:
            player.add_item_to_backpack(dropped_items[int(number) - 1])
    elif option == 2:
        pass
    elif option == 3:
        player.add_item_to_backpack(dropped_items)


def chilling_menu(player: units.Player):
    """
    Menu that appears after mission completion, main story mission, etc.
    """
    console.print_wall()
    if player.current_city is not None:
        print(
            "Current city is %s" % player.current_city
        )
    print("1. Next story part (unavailable)")
    print("2. Player' missions")
    print("3. Equipment menu")
    print("4. Player menu")
    if player.current_city is None:
        print("5. Go to city")
    else:
        print("5. %s menu" % player.current_city)
    print("6. Heal %d" % player.count_utility_items())
    print("7. Save")
    print("8. Quit")
    option = get_input(int)
    if not 1 <= option <= 8:
        print("There's no such choice")
        chilling_menu(player)
        return
    if option == 2:
        player_missions_menu(player)
        chilling_menu(player)
    elif option == 3:
        equipment_model_menu(player)
        chilling_menu(player)
    elif option == 4:
        player_menu(player)
        chilling_menu(player)
    elif option == 5:
        if player.current_city is None:
            choose_city(player)
        else:
            city_menu(player, database.get_city_from_db(
                player.current_city
            ))
        chilling_menu(player)
    elif option == 6:
        player.heal()
        chilling_menu(player)
    elif option == 7:
        save_game(player)
        chilling_menu(player)
    else:
        autosave(player)
        main_menu()


def player_menu(player: units.Player):
    """

    :param player:
    :type player Player
    :return:
    """
    console.print_wall()
    print("1. Print my stats")
    print("2. Print levels of item types")
    print("3. Quit")
    console.print_wall()
    option = get_input(int)
    if not 1 <= option <= 3:
        print("There's no such option")
        player_menu(player)
        return
    if option == 3:
        return
    elif option == 1:
        print(player)
        player_menu(player)
        return
    elif option == 2:
        console.clear()
        console.print_wall()
        weapon_table = PrettyTable(['Weapon Type', 'Level', 'Kills   '])
        weapon_table.align['Weapon Type'] = 'l'
        weapon_table.add_row(['Sword',
                              player.sword_level,
                              "{}/{}".format(
                                  player.sword_exp,
                                  player.sword_level * 5
                              )])
        weapon_table.add_row(['TH sword',
                              player.th_sword_level,
                              "{}/{}".format(
                                  player.th_sword_exp,
                                  player.th_sword_level * 5
                              )])
        weapon_table.add_row(['Axe',
                              player.axe_level,
                              "{}/{}".format(
                                  player.axe_exp,
                                  player.axe_level * 5
                              )])
        weapon_table.add_row(['Spear',
                              player.spear_level,
                              "{}/{}".format(
                                  player.spear_exp,
                                  player.spear_level * 5
                              )])
        weapon_table.add_row(['Dagger',
                              player.dagger_level,
                              "{}/{}".format(
                                  player.dagger_exp,
                                  player.dagger_level * 5
                              )])
        print(weapon_table)

        print()
        shield_table = PrettyTable(['Shield Type', 'Level', 'Abs. dmg'])
        shield_table.align['Shield Type'] = 'l'
        shield_table.add_row(['Tower',
                              player.tower_level,
                              "{}/{}".format(
                                  player.tower_exp,
                                  player.tower_level * 500
                              )])
        shield_table.add_row(['Infantry ',
                              player.infantry_level,
                              "{}/{}".format(
                                  player.infantry_exp,
                                  player.infantry_level * 500
                              )])
        shield_table.add_row(['Buckler',
                              player.buckler_level,
                              "{}/{}".format(
                                  player.buckler_exp,
                                  player.buckler_level * 500
                              )])
        print(shield_table)
        print()
        armor_table = PrettyTable(['Armor Type ', 'Level', 'Abs. dmg'])
        armor_table.align['Armor Type '] = 'l'
        armor_table.add_row(['Light',
                             player.light_armor_level,
                             '{}/{}'.format(
                                 player.light_armor_exp,
                                 player.light_armor_level * 500
                             )])
        armor_table.add_row(['Medium',
                             player.medium_armor_level,
                             '{}/{}'.format(
                                 player.medium_armor_exp,
                                 player.medium_armor_level * 500
                             )])
        armor_table.add_row(['Heavy',
                             player.heavy_armor_level,
                             '{}/{}'.format(
                                 player.heavy_armor_exp,
                                 player.heavy_armor_level * 500
                             )])
        print(armor_table)
        player_menu(player)
        return


def choose_city(player: units.Player):
    """
    Choose city to go
    """
    # TODO: Split method
    console.print_wall()
    cities = database.get_list_of_cities()
    list_all = 1
    city_number = 0
    for city in cities:
        city_obj = database.get_city_from_db(city[0])
        is_city_opened = (city_obj.opened or
                          city_obj.name in player.opened_cities)
        if city_obj.level <= player.level and is_city_opened:
            print(
                "{}. {}".format(
                    city_number + 1,
                    city[0]
                )
            )
            city_number += 1
            list_all += 1
    print("%d. List all cities (even if player' level is too low)" % list_all)
    print("%d. Quit" % (list_all + 1))
    console.print_wall()
    print("Enter number of city that you wanna visit:", end=" ")
    option = get_input(int)
    quit_num = 1
    if option == list_all + 1:
        return
    elif option == list_all:
        for city_number, city in enumerate(cities):
            city_obj = database.get_city_from_db(city[0])
            if city_obj.level > player.level:
                print(
                    "{}. {} (Required level is {})".format(
                        city_number + 1,
                        city[0],
                        city_obj.level
                    )
                )
                quit_num += 1
            elif city_obj.opened or city_obj.name in player.opened_cities:
                print(
                    "{}. {}".format(
                        city_number + 1,
                        city[0]
                    )
                )
                quit_num += 1
        print("%d. Quit" % quit_num)
        print("Enter number of city that you wanna visit:", end=" ")
        option = get_input(int)
        if option == quit_num:
            return
        city = database.get_city_from_db(
            cities[option - 1][0])  # type: cities.City
        if city.level > player.level:
            print("You can't go to %s, your level is too low!" % city.name)
            choose_city(player)
            return
        player.go_to_city(city)
        chilling_menu(player)
    else:
        for city_name in cities:
            city_obj = database.get_city_from_db(city_name[0])
            if city_obj.level > player.level:
                cities.remove(city_name)
        city = database.get_city_from_db(
            cities[option - 1][0])  # type: cities.City
        if city.level > player.level:
            print("You can't go to %s, your level is too low!" % city.name)
            choose_city(player)
            return
        player.go_to_city(city)
        chilling_menu(player)


def city_menu(player: units.Player, city: City):
    """
    City menu. Contains shop and mission list
    """
    console.clear()
    console.print_wall()
    print("Welcome to %s" % city.name)
    print("1. Shop")
    print("2. City missions")
    print("3. Leave city menu")
    print("4. Leave the city at all")
    option = get_input(int)
    console.print_wall()
    if option == 1:
        shop_menu(player, city)
        city_menu(player, city)
        return
    elif option == 2:
        city_missions(player, city)
    elif option == 3:
        pass
    elif option == 4:
        player.current_city = None
        chilling_menu(player)
        return
    else:
        print("Option out of range, try again")
        city_menu(player, city)
    chilling_menu(player)


def city_missions(player: units.Player, city: City):
    """
    Menu contains city missions.
    Provides player to take missions
    """
    console.print_wall()
    print("1. Take a mission")
    print("2. End mission")
    print("3. Quit")
    console.print_wall()
    option = get_input(int)
    if not 1 <= option <= 3:
        print("There's no such option")
        city_missions(player, city)
        return
    if option == 3:
        city_menu(player, city)
        return
    elif option == 1:
        missions = list()
        if city.missions is not None:
            for mis in city.missions:
                mis_dic = database.get_mission_from_db(mis)
                if (mis not in player.finished_missions and
                        (mis_dic['opened'] or mis in player.opened_missions)):
                    if len(player.missions) == 0:
                        pass
                    else:
                        for mission in player.missions:
                            if mission['name'] == mis_dic['name']:
                                return
                    missions.append(mis_dic)
        quit_num = 1
        console.print_wall()
        if len(missions) == 0:
            print("There's no missions available\n")
        else:
            for value, mission in enumerate(missions):
                print(value + 1)
                mission_table = PrettyTable(["What", "Values"])
                mission_table.add_row(["Name", mission['name']])
                mission_table.add_row(["Description", mission['description']])
                mission_table.add_row(["Reward",
                                       (str(mission['reward']) + ' gold')])
                print(mission_table)
                quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of mission that you wanna take:", end=" ")
        option = get_input(int)
        if option == quit_num:
            return
        if not 1 <= option < quit_num:
            print("There's no such mission")
            city_missions(player, city)
            return
        mission = missions[option - 1]
        mission['city'] = city.name
        mission_name = mission['name']
        try:
            player.add_mission(mission)
        except IndexError:
            print("There's no mission with such number")
            city_missions(player, city)
            return
        mission_name = mission_name.replace(' ', '_').lower()
        for mission in city.missions:
            if mission == mission_name:
                city.missions.pop(
                    city.missions.index(mission_name)
                )
        city_missions(player, city)
    elif option == 2:
        missions = list()
        for mission in player.missions:
            if mission['city'] == city.name and mission['done']:
                missions.append(mission)
        quit_num = 1
        console.print_wall()
        for mission_number, mission in enumerate(missions):
            print("%d. %s" % (mission_number + 1, mission['name']))
            print("Description - {}\nDone - {}".format(
                mission['description'],
                mission['done']
            ))
            quit_num += 1
        console.print_wall()
        print("Enter number of mission that you wanna end:", end=" ")
        mission_number = get_input(int)
        mission = None
        try:
            mission = missions[mission_number - 1]
        except IndexError:
            print("There's no such mission")
            city_missions(player, city)
            return
        player.end_mission(mission)
        if mission['event'] is not None:
            event = database.get_event_from_db(mission['event'])
            start_event(player, event)
    city_menu(player, city)


def start_event(player: units.Player, event: dict):
    """
    Execute mission event
    """
    player.events.append(event['name'])
    if event['type'] == 'open_city':
        player.opened_cities.append(event['target'])
        print(event['text'])
        input('Press something')
        return
    elif event['type'] == 'open_mission':
        player.opened_missions.append(event['target'])
        print(event['text'])
        input('Press something')
        return


def shop_menu(player: units.Player, city: City):
    """
    Menu, where you can buy items from city
    """
    # TODO: Split method
    print("1. Buy item")
    print("2. Buy utility item")
    print("3. Sell item")
    print("4. Quit to city menu")
    option = get_input(int)
    console.print_wall()
    if option == 1:
        quit_num = 1
        for item_number, item_name in enumerate(city.items):
            item = database.get_item_from_db(item_name)
            print("%d. %s" % (item_number + 1, item))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of item that you wanna buy:", end=" ")
        options = None
        options = input()
        try:
            options = list(map(int, options.split()))
        except ValueError:
            print("Only numbers allowed")
            shop_menu(player, city)
            return
        if options[0] == quit_num:
            return
        names = list()
        for number in options:
            try:
                names.append(city.items[number - 1])
            except IndexError:
                print("There's no such item with number %d" % number)
                shop_menu(player, city)
                return
        items_to_buy = None
        price = 0
        if len(names) == 1:
            items_to_buy = database.get_item_from_db(names[0])
            price = items_to_buy.price
            items_to_buy = [items_to_buy]
        else:
            items_to_buy = list()
            for name in names:
                item = database.get_item_from_db(name)
                items_to_buy.append(item)
                price += item.price
        if player.gold < price:
            if len(items_to_buy) == 1:
                print("You don't have enough money to buy %s" %
                      items_to_buy[0].name)
            else:
                print("You don't have enough money to buy %s" %
                      (str(len(items_to_buy)) + ' items'))
            shop_menu(player, city)
            return
        player.add_item_to_backpack(items_to_buy)
        player.gold -= price
        if len(items_to_buy) == 1:
            print("You bought {} for {} gold".format(
                items_to_buy[0].name, price))
        else:
            print("You bought {} items for {} gold".format(
                len(items_to_buy), price))
        shop_menu(player, city)
        return
    elif option == 2:
        quit_num = 1
        available_items = list()
        available_items.append(database.get_item_from_db('Small_Healing_Salve'))
        for item_number, item in enumerate(available_items):
            print("%d. %s" % (item_number + 1, item))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of item you wanna buy:", end=" ")
        item_number = get_input(int)
        if item_number == quit_num:
            shop_menu(player, city)
            return
        if not 1 <= item_number < quit_num:
            print("Number is out of range")
            shop_menu(player, city)
            return
        item = available_items[item_number - 1]
        print("How much items do you wanna buy?", end=" ")
        quantity = get_input(int)
        console.print_wall()
        if quantity < 0:
            print("There's no such number")
            shop_menu(player, city)
            return
        if quantity == 0:
            shop_menu(player, city)
            return
        if player.gold < item.price * quantity:
            print("You don't have enough money to buy %s" % item.name)
            shop_menu(player, city)
            return
        for _ in range(quantity):
            player.add_item_to_backpack(item)
        player.gold -= (item.price * quantity)
        if quantity == 1:
            print("You bought %s for %d gold" %
                  (item.name, item.price * quantity))
        else:
            print("You bought %d %s for %d gold" %
                  (quantity, item.name, item.price * quantity))
        shop_menu(player, city)
        return
    elif option == 3:
        quit_num = 1
        available_items = list()
        for item in player.items:
            if not item.is_utility():
                available_items.append(item)
        console.print_wall()
        if len(available_items) == 0:
            print("You don't have any item to sell")
            shop_menu(player, city)
            return
        for item_number, item in enumerate(available_items):
            print("%d. %s" % (item_number + 1, item))
            quit_num += 1
        print("%d. Quit" % quit_num)
        console.print_wall()
        print("Enter number of item that you wanna sell:", end=" ")
        item_number = get_input(int)
        if item_number == quit_num:
            return
        item_name = ''
        try:
            item_name = available_items[item_number - 1].name
        except IndexError:
            print("There's no such item")
            console.print_wall()
            shop_menu(player, city)
            return
        try:
            player.sell_item(item_name)
        except NameError:
            shop_menu(player, city)
            return
        if ' ' in item_name:
            item_name = item_name.replace(' ', '_')
        city.items.append(item_name)
        shop_menu(player, city)
        return
    city_menu(player, city)


def save_game(player: units.Player):
    """
    Saves player object to .save file
    """
    if not os.path.exists("./Saves"):
        os.mkdir("Saves")
    console.print_wall()
    print("Name your save:", end=" ")
    name = input()
    console.print_wall()
    if ' ' in name:
        name = name.replace(' ', '_')
    with open("./Saves/" + name + ".save", 'wb') as save:
        pickle.dump(player, save)


def autosave(player: units.Player):
    """
    Create autosave file
    """
    if not os.path.exists("./Saves"):
        os.mkdir("Saves")
    name = "autosave_" + str(int(time.time()))
    with open('./Saves/' + name + ".save", 'wb') as save:
        pickle.dump(player, save)
    time.sleep(0.5)


def list_saved_games():
    """
    Lists saved games
    """
    saves = os.listdir("./Saves")
    for file in saves:
        print(file)
