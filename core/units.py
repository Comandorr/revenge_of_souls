"""
Source file contains all Unit classes
"""


import random
from time import sleep
from typing import List, Optional
from prettytable import PrettyTable
from . import items, DeadHero
from . import equipment
from . import cities


class Unit(object):
    """
    Abstraction of all units in RoS.
    Only for inheritance
    """

    def __init__(self, args: list):
        self.name = args[0]
        self.hit_points = args[1]
        self.max_hit_points = args[1]
        self.damage = args[2]
        self.armor = args[3]
        self.level = args[4]
        self.reward = args[5]  # Gold
        self.reward_experience = args[6]
        self.given_damage = 0
        self.equipment_model = equipment.EquipmentModel()
        if not isinstance(self, Player):
            # FIX
            self.configure_equipment_model(args[7], args[8], args[9])

    @property
    def right_hand(self) -> Optional[items.Weapon]:
        return self.equipment_model.right_hand

    @right_hand.setter
    def right_hand(self, item: items.Item):
        self.equipment_model.right_hand = item

    @property
    def left_hand(self):
        return self.equipment_model.left_hand

    @left_hand.setter
    def left_hand(self, item: items.Item):
        self.equipment_model.left_hand = item

    @property
    def head(self):
        return self.equipment_model.head

    @head.setter
    def head(self, item: items.Item):
        self.equipment_model.head = item

    @property
    def chest(self):
        return self.equipment_model.chest

    @chest.setter
    def chest(self, item: items.Item):
        self.equipment_model.chest = item

    @property
    def arms(self):
        return self.equipment_model.arms

    @arms.setter
    def arms(self, item: items.Item):
        self.equipment_model.arms = item

    @property
    def legs(self):
        return self.equipment_model.legs

    @legs.setter
    def legs(self, item: items.Item):
        self.equipment_model.legs = item

    @property
    def ring(self):
        return self.equipment_model.ring

    @ring.setter
    def ring(self, item: items.Item):
        self.equipment_model.ring = item

    @property
    def necklace(self):
        return self.equipment_model.necklace

    @necklace.setter
    def necklace(self, item: items.Item):
        self.equipment_model.necklace = item

    @property
    def artifacts(self):
        return self.equipment_model.artifacts

    @artifacts.setter
    def artifacts(self, list_of_items: List[items.Item]):
        self.equipment_model.artifacts = (list_of_items
                                          if len(list_of_items) > 0 else None)

    def configure_equipment_model(self, right_hand=None, left_hand=None,
                                  head=None, chest=None, arms=None, legs=None,
                                  ring=None, necklace=None, artifacts=None):
        """
        Set unit equipment model' items. Not for a player.
        """
        self.equipment_model.right_hand = right_hand
        self.equipment_model.left_hand = left_hand
        self.equipment_model.head = head
        self.equipment_model.chest = chest
        self.equipment_model.arms = arms
        self.equipment_model.legs = legs
        self.equipment_model.ring = ring
        self.equipment_model.necklace = necklace
        self.equipment_model.artifacts = artifacts

        if self.right_hand is not None:
            self.damage += self.right_hand.damage

        same = self.right_hand.name == self.left_hand.name
        if self.left_hand is not None and not same:
            if isinstance(self.left_hand, items.Weapon):
                self.damage += self.left_hand.damage
            elif isinstance(self.left_hand, items.Shield):
                self.armor += self.left_hand.armor

        if self.head is not None:
            self.armor += self.head.armor

        if self.chest is not None:
            self.armor += self.chest.armor

        if self.arms is not None:
            self.armor += self.arms.armor

        if self.legs is not None:
            self.armor += self.legs.armor

        if self.ring is not None:
            # TODO: Ring setting
            pass

        if self.necklace is not None:
            # TODO: Necklace setting
            pass

        if self.artifacts is not None and len(self.artifacts) > 0:
            # TODO: Artifacts setting
            pass

    def create_armor_set(self) -> list:
        """
        Creating a list of armor that player uses.
        Sum all their armor numbers and return list of it.
        """
        armor_set = []
        if self.head is not None:
            armor_set.append(self.head.armor)
        if self.chest is not None:
            armor_set.append(self.chest.armor)
        if self.arms is not None:
            armor_set.append(self.arms.armor)
        if self.legs is not None:
            armor_set.append(self.legs.armor)

        return armor_set

    def attack(self, enemy):
        """
        Self attacking enemy
        Try not to hurt your eyes.
        :param enemy:
        :type enemy Unit
        :return:
        """
        armor_set = enemy.create_armor_set()
        if (len(armor_set) > 0 and
                enemy.left_hand is not None and
                isinstance(enemy.left_hand, items.Shield)):
            enemy_calculated_armor = enemy.armor - (
                sum(armor_set) +
                enemy.left_hand.armor
            )
            list_of_damage = enemy.calculate_block()
            enemy_calculated_armor += sum(list_of_damage)
            if (self.damage - enemy_calculated_armor) <= 0:
                return
            self.given_damage += self.damage - enemy_calculated_armor
        elif len(armor_set) > 0:
            enemy_calculated_armor = enemy.armor - sum(armor_set)
            calculated_armor_block = enemy.calculate_block()[0]
            enemy_calculated_armor += calculated_armor_block
            if (self.damage - enemy_calculated_armor) <= 0:
                return
            self.given_damage += self.damage - enemy_calculated_armor
        elif isinstance(enemy.left_hand, items.Shield):
            enemy_calculated_armor = (enemy.armor -
                                      enemy.left_hand.armor)
            calculated_shield_block = enemy.calculate_block()[0]
            enemy_calculated_armor += calculated_shield_block
            if (self.damage - enemy_calculated_armor) <= 0:
                return
            self.given_damage += self.damage - enemy_calculated_armor
        else:
            self.given_damage += self.damage - enemy.armor

    def calculate_block(self) -> list:
        """
        Calculate armor and shield block percentage
        """
        armor_set = self.create_armor_set()
        type(armor_set)
        if (self.left_hand is not None
                and isinstance(self.left_hand, items.Shield)
                and len(armor_set) > 0):
            armor_blocked_damage = Unit.calculate_block_percentage(
                sum(armor_set))
            shield_blocked_damage = Unit.calculate_block_percentage(
                self.left_hand.armor)
            return [armor_blocked_damage, shield_blocked_damage]
        elif (self.left_hand is not None
                and isinstance(self.left_hand, items.Shield)):
            return [Unit.calculate_block_percentage(self.left_hand.armor)]
        elif len(armor_set) > 0:
            return [Unit.calculate_block_percentage(sum(armor_set))]

    @staticmethod
    def calculate_block_percentage(armor) -> float:
        """
        Calculate block block_percentage
        """
        rand = random.randrange(1, 101)
        if rand in range(1, 21):
            return armor
        elif rand in range(21, 51):
            return armor * 0.5
        else:
            return armor * 0.2

    def is_enemy_alive(self, enemy) -> Optional[bool]:
        """
        Check whether enemy is alive or not
        :param enemy:
        :return bool:
        """
        if enemy.hit_points > self.given_damage:
            # Alive
            return True
        # Sadly, No
        if int(self.given_damage) == 0:
            # If enemy didn't inflict any damage
            pass
        elif not int(self.given_damage) > enemy.max_hit_points:
            # If not self inflicted more damage than enemy
            # Means that enemy won
            enemy.hit_points -= int(self.given_damage)
        else:
            # Enemy is alive
            enemy.hit_points = 0
        if int(enemy.given_damage) == 0:
            pass
        elif not int(enemy.given_damage) > self.max_hit_points:
            # Same
            self.hit_points -= int(enemy.given_damage)
        else:
            self.hit_points = 0
        fight_recap(self, enemy)  # Print info about fight
        if not isinstance(enemy, Player):
            print(
                "{} killed {} and got {} experience".format(
                    self.name,
                    enemy.name,
                    enemy.reward_experience
                )
            )
        else:
            print("Your hero is dead! Begin game again!")
            raise DeadHero  # Raise DeadHero exception to start game again
        if isinstance(self, Player):
            self.experience += enemy.reward_experience
            self.gold += enemy.reward
            armor_set = self.create_armor_set()
            if self.right_hand is not None:
                self.handle_weapon_level()
            if len(armor_set) > 0:
                self.handle_armor_level(enemy.given_damage)
            if (self.left_hand is not None
                    and isinstance(self.left_hand, items.Shield)):
                self.handle_shield_armor(self.given_damage)
            if self.hit_points > self.max_hit_points:
                self.hit_points = self.max_hit_points

        print(self)
        self.given_damage = 0
        return False

    def is_alive(self) -> bool:
        """
        Checks whether self' hit points higher than 0
        """
        return self.hit_points > 0

    def __str__(self):
        table = PrettyTable([self.name, 'Stats'])
        table.add_row(['HP',
                       '{}/{}'.format(
                           self.hit_points,
                           self.max_hit_points
                       )])
        table.add_row(['Damage', self.damage])
        table.add_row(['Armor', self.armor])
        table.add_row(['Level', self.level])
        print(table)
        return ''


class Player(Unit):
    """
    Main hero class
    """

    def __init__(self, name):
        super().__init__(
            [name, 100, 6, 2, 1, 100, 500]
        )
        self.weight = 100
        self.current_weight = 0
        self.given_damage = 0
        self.experience = 0
        self.gold = 0
        self.current_city = None
        self.current_mission = None
        self.items = list()
        self.missions = list()
        self.finished_missions = list()
        self.opened_cities = list()
        self.opened_missions = list()
        self.events = list()

        # Levels of the type of weapon
        self.sword_level = 1
        self.sword_exp = 0
        self.th_sword_level = 1
        self.th_sword_exp = 0
        self.spear_level = 1
        self.spear_exp = 0
        self.axe_level = 1
        self.axe_exp = 0
        self.dagger_level = 1
        self.dagger_exp = 0

        # Levels of the type of shield
        self.tower_level = 1
        self.tower_exp = 0
        self.infantry_level = 1
        self.infantry_exp = 0
        self.buckler_level = 1
        self.buckler_exp = 0

        # Level of the type of armor
        self.light_armor_level = 1
        self.light_armor_exp = 0
        self.medium_armor_level = 1
        self.medium_armor_exp = 0
        self.heavy_armor_level = 1
        self.heavy_armor_exp = 0

    def handle_weapon_level(self):
        """
        Check whether player has new level of the type of weapon
        :return :
        """
        weapon = self.right_hand
        if weapon is None:
            return
        if "Two-handed sword" in weapon.type:
            if self.th_sword_level == 15:
                return
            self.th_sword_exp += 1
            if self.th_sword_exp >= (self.th_sword_level * 5):
                self.damage -= self.weapon_type_damage(weapon)
                self.th_sword_level += 1
                self.damage += self.weapon_type_damage(weapon)
                print("You proficiency level of the"
                      " Two-handed sword has increased!")
        elif "Sword" in weapon.type:
            if self.sword_level == 15:
                return
            self.sword_exp += 1
            if self.sword_exp >= (self.sword_level * 5):
                self.damage -= self.weapon_type_damage(weapon)
                self.sword_level += 1
                self.damage += self.weapon_type_damage(weapon)
                print("You proficiency level of the Sword has increased!")
        elif "Axe" in weapon.type:
            if self.axe_level == 15:
                return
            self.axe_exp += 1
            if self.axe_exp >= (self.axe_level * 5):
                self.damage -= self.weapon_type_damage(weapon)
                self.axe_level += 1
                self.damage += self.weapon_type_damage(weapon)
                print("You proficiency level of the Axe has increased!")
        elif "Spear" in weapon.type:
            if self.spear_level == 15:
                return
            self.spear_exp += 1
            if self.spear_exp >= (self.spear_level * 5):
                self.damage -= self.weapon_type_damage(weapon)
                self.spear_level += 1
                self.damage += self.weapon_type_damage(weapon)
                self.spear_exp = 0
                print("You proficiency level of the Spear has increased!")
        elif "Dagger" in weapon.type:
            if self.dagger_level == 15:
                return
            self.dagger_exp += 1
            if self.dagger_exp >= (self.dagger_level * 5):
                self.damage -= self.weapon_type_damage(weapon)
                self.dagger_level += 1
                self.damage += self.weapon_type_damage(weapon)
                print("You proficiency level of the Dagger has increased!")

    def weapon_type_damage(self, weapon) -> float:
        """
        Calculate additional weapon type damage based on proficiency level
        :param weapon:
        :type weapon items.Weapon
        :return damage:
        """
        additional_damage = {
            "1": 1.05,
            "2": 1.1,
            "3": 1.15,
            "4": 1.2,
            "5": 1.25,
            "6": 1.3,
            "7": 1.35,
            "8": 1.4,
            "9": 1.45,
            "10": 1.5,
            "11": 1.6,
            "12": 1.7,
            "13": 1.8,
            "14": 1.9,
            "15": 2
        }
        level_of_type = 0
        if "Two-handed sword" in weapon.type:
            level_of_type = self.th_sword_level
        elif "Sword" in weapon.type:
            level_of_type = self.sword_level
        elif "Axe" in weapon.type:
            level_of_type = self.axe_level
        elif "Spear" in weapon.type:
            level_of_type = self.spear_level
        elif "Dagger" in weapon.type:
            level_of_type = self.dagger_level

        damage_coefficient = additional_damage.get(str(level_of_type), None)

        return weapon.damage * damage_coefficient

    def handle_armor_level(self, given_damage):
        """
        Check whether player has new level of the type of armor
        :param given_damage:
        :return:
        """
        armor_set = [self.head, self.chest, self.arms, self.legs]

        armor_type = ""
        for armor_item in armor_set:
            if armor_item is None:
                continue
            if armor_type == "":
                armor_type = armor_item.type.split(" ")[0]
            if armor_item.type.split(" ")[0] == armor_type:
                continue
            else:
                armor_type = "mixed"
                break
        if armor_type != "mixed":
            if "Light" in armor_type:
                self.light_armor_exp += int(given_damage)
                if self.light_armor_exp > (self.light_armor_level * 500):
                    armor = [self.head, self.chest, self.arms, self.legs]
                    for item in armor:
                        if item is None:
                            continue
                        self.armor -= self.armor_type_armor(item)
                    self.light_armor_level += 1
                    for item in armor:
                        if item is None:
                            continue
                        self.armor += self.armor_type_armor(item)
            elif "Medium" in armor_type:
                self.medium_armor_exp += int(given_damage)
                if self.medium_armor_exp > (self.medium_armor_level * 500):
                    armor = [self.head, self.chest, self.arms, self.legs]
                    for item in armor:
                        if item is None:
                            continue
                        self.armor -= self.armor_type_armor(item)
                    self.medium_armor_level += 1
                    for item in armor:
                        if item is None:
                            continue
                        self.armor += self.armor_type_armor(item)
            elif "Heavy" in armor_type:
                self.heavy_armor_exp += int(given_damage)
                if self.heavy_armor_exp > (self.heavy_armor_level * 500):
                    armor = [self.head, self.chest, self.arms, self.legs]
                    for item in armor:
                        if item is None:
                            continue
                        self.armor -= self.armor_type_armor(item)
                    self.heavy_armor_level += 1
                    for item in armor:
                        if item is None:
                            continue
                        self.armor += self.armor_type_armor(item)
        else:
            for armor in armor_set:
                if armor is None:
                    continue
                if "Light" in armor.type:
                    self.light_armor_exp += int(given_damage)
                    if self.light_armor_exp > (self.light_armor_level * 500):
                        self.armor -= self.armor_type_armor(armor)
                        self.light_armor_level += 1
                        self.armor += self.armor_type_armor(armor)
                elif "Medium" in armor.type:
                    self.medium_armor_exp += int(given_damage)
                    if self.medium_armor_exp > (self.medium_armor_level * 500):
                        self.armor -= self.armor_type_armor(armor)
                        self.medium_armor_level += 1
                        self.armor += self.armor_type_armor(armor)
                elif "Heavy" in armor.type:
                    self.heavy_armor_exp += int(given_damage)
                    if self.heavy_armor_exp > (self.heavy_armor_level * 500):
                        self.armor -= self.armor_type_armor(armor)
                        self.heavy_armor_level += 1
                        self.armor += self.armor_type_armor(armor)

    def armor_type_armor(self, armor_set) -> float:
        """
        Calculate additional armor set type armor based on proficiency level
        :param armor_set:
        :return:
        """
        additional_armor = {
            "1": 1.05,
            "2": 1.1,
            "3": 1.15,
            "4": 1.2,
            "5": 1.25,
            "6": 1.3,
            "7": 1.35,
            "8": 1.4,
            "9": 1.45,
            "10": 1.5,
            "11": 1.6,
            "12": 1.7,
            "13": 1.8,
            "14": 1.9,
            "15": 2
        }
        level_of_type = 0
        if "Light" in armor_set.type:
            level_of_type = self.light_armor_level
        elif "Medium" in armor_set.type:
            level_of_type = self.medium_armor_level
        elif "Heavy" in armor_set.type:
            level_of_type = self.heavy_armor_level

        armor_coefficient = additional_armor.get(str(level_of_type), None)

        return armor_set.armor * armor_coefficient

    def handle_shield_armor(self, given_damage):
        """
        Check whether player has new level of the type of shield
        :param given_damage:
        :return:
        """
        shield = self.left_hand
        if (not isinstance(self.left_hand, items.Shield)
                or self.left_hand is None):
            return
        if "Towering" in shield.type:
            self.tower_exp += int(given_damage)
            if self.tower_exp > (self.tower_level * 500):
                self.damage -= self.shield_type_armor(shield)
                self.tower_level += 1
                self.damage += self.shield_type_armor(shield)
        elif "Infantry" in shield.type:
            self.infantry_exp += int(given_damage)
            if self.infantry_exp > (self.infantry_level * 500):
                self.damage -= self.shield_type_armor(shield)
                self.infantry_level += 1
                self.damage += self.shield_type_armor(shield)
        elif "Buckler" in shield.type:
            self.buckler_exp += int(given_damage)
            if self.buckler_exp > (self.buckler_level * 500):
                self.damage -= self.shield_type_armor(shield)
                self.buckler_level += 1
                self.damage += self.shield_type_armor(shield)

    def shield_type_armor(self, shield) -> float:
        """
        Calculate additional shield type armor based on proficiency level
        :param shield:
        :return:
        """
        additional_armor = {
            "1": 1.05,
            "2": 1.1,
            "3": 1.15,
            "4": 1.2,
            "5": 1.25,
            "6": 1.3,
            "7": 1.35,
            "8": 1.4,
            "9": 1.45,
            "10": 1.5,
            "11": 1.6,
            "12": 1.7,
            "13": 1.8,
            "14": 1.9,
            "15": 2
        }
        level_of_type = 0
        if "Towering" in shield.type:
            level_of_type = self.tower_level
        elif "Infantry" in shield.type:
            level_of_type = self.infantry_level
        elif "Buckler" in shield.type:
            level_of_type = self.buckler_level

        armor_coefficient = additional_armor.get(str(level_of_type), None)

        return shield.armor * armor_coefficient

    def add_item_to_backpack(self, item):
        """
        Add item to backpack
        :param item:
        :return:
        """
        if type(item) is list:
            for it in item:
                self.items.append(it)
                self.current_weight += it.weight
            return
        self.items.append(item)
        self.current_weight += item.weight

    def count_utility_items(self) -> int:
        """
        Counts a number of utility items in backpack
        :return:
        """
        count = 0
        for item in self.items:
            if isinstance(item, items.Utility):
                count += 1
        return count

    def find_item(self, item_name):
        """
        Find item in your backpack
        :param item_name:
        :return item or None:
        """
        result = None
        for item in self.items:
            if item.name == item_name:
                result = item
                break
        else:
            print(
                "You don't have %s in your backpack!" % item_name
            )

        return result

    def use_item(self, item_name):
        """
        Add item stats to hero stats
        :param item_name:
        :return:
        """
        item = self.find_item(item_name)
        if item is None:
            raise NameError("Missing item")
        if item.using:
            print(
                "You are already using %s." % item.name
            )
            return
        if isinstance(item, items.Weapon):
            for _item in self.items:
                if self.right_hand and _item.using:
                    self.stop_using(_item)
                    break
            if item.two_handed:
                self.stop_using(self.left_hand)
            self.damage += self.weapon_type_damage(item)
            item.using = True
            self.right_hand = item
        elif isinstance(item, items.Shield):
            for _item in self.items:
                if (self.left_hand and isinstance(self.left_hand, items.Shield)
                        and not self.left_hand == _item):
                    self.stop_using(_item)
                    break
            if self.right_hand and self.right_hand.two_handed:
                print("You can't use shield! Your weapon is two-handed!")
                print("Do you want to pull weapon off? (Yes/No)")
                answer = input()
                if 'y' in answer.lower():
                    self.stop_using(self.right_hand)
                    self.use_item(item.name)
                return
            elif (self.right_hand is not None
                  and self.right_hand.using_as_two_handed):
                print("You can't use the shield! You're using your weapon in"
                      "two hands")
                print("Do you want to use it in one hand? (Yes/No)")
                answer = input()
                if 'y' in answer.lower():
                    self.right_hand.using_as_two_handed = False
                    self.use_item(item_name)
                return
            self.armor += self.shield_type_armor(item)
            item.using = True
            self.left_hand = item
        elif isinstance(item, items.Armor):
            if "Helmet" in item.type:
                if self.head is not None:
                    self.stop_using(self.head)
                self.armor += item.armor
                item.using = True
                self.head = item
            elif "Chest" in item.type:
                if self.chest is not None:
                    self.stop_using(self.chest)
                self.armor += item.armor
                item.using = True
                self.chest = item
            elif "Arms" in item.type:
                if self.arms is not None:
                    self.stop_using(self.arms)
                self.armor += item.armor
                item.using = True
                self.arms = item
            elif "Legs" in item.type:
                if self.legs is not None:
                    self.stop_using(self.legs)
                self.armor += item.armor
                item.using = True
                self.legs = item

    def stop_using(self, item):
        """
        Detach item stats from hero
        :param item:
        :type item items.Item
        :return:
        """
        if not item:
            return
        if not item.using:
            return
        if isinstance(item, items.Weapon):
            self.damage -= self.weapon_type_damage(item)
            self.right_hand.using = False
            self.right_hand.using_as_two_handed = False
            self.right_hand = None
        elif isinstance(item, items.Shield):
            self.armor -= self.shield_type_armor(item)
            self.left_hand.using = False
            self.left_hand = None
        elif isinstance(item, items.Armor):
            self.armor -= self.armor_type_armor(item)
            if self.head.name == item.name:
                self.head.using = False
                self.head = None
            elif self.chest.name == item.name:
                self.chest.using = False
                self.chest = None
            elif self.arms.name == item.name:
                self.arms.using = False
                self.arms = None
            elif self.legs.name == item.name:
                self.legs.using(None)
                self.legs = None

    def sell_item(self, item_name):
        """
        Sell item with name=item_name
        :param item_name:
        :return:
        """
        item = self.find_item(item_name)
        if not item:
            raise NameError("Missing item")
        self.stop_using(item)
        self.gold += int(item.price * 0.5)
        self.items.pop(self.items.index(item))
        print(
            "You sold {} and got {} gold".format(
                item.name,
                int(item.price * 0.5)
            )
        )

    def remove_item(self, item_name):
        """
        Removes item from backpack and current game
        :param item_name:
        :return:
        """
        item = self.find_item(item_name)
        if not item:
            return
        self.stop_using(item)
        self.gold += item.price // 2
        self.items.pop(self.items.index(item))
        print(
            "You removed {} and got {} gold".format(
                item.name,
                item.price // 2
            )
        )

    def list_backpack(self):
        """
        Prints list of player items
        """
        for item in self.items:
            print(item)

    def go_to_city(self, city: cities.City):
        """
        Change current city to
        :param city:
        :return:
        """
        self.current_city = city.name
        #length = 5 if not self.current_weight > self.weight else 10
        #for _ in range(length):
        #    print(".")
        #    sleep(0.5)

    def add_mission(self, mission: dict):
        """
        Provides adding of mission dictionary to player mission list
        :param self
        :param mission
        :type self Player
        :type mission dict
        """
        self.missions.append(mission)

    def delete_mission(self, mission: dict):
        self.missions.remove(mission)

    def begin_mission(self, mission: dict):
        """
        Sets current_mission of the player
        """
        self.current_mission = mission['name']

    def end_mission(self, mission: dict):
        """
        Ends a player mission and clears variable
        """
        self.gold += mission['reward']
        self.experience += mission['reward_experience']
        print(("You ended '{}' mission. You got {} gold and {}"
               " experience\n").format(
                   mission['name'],
                   mission['reward'],
                   mission['reward_experience']
        ))
        self.is_new_level()
        print("Press something...")
        input()
        self.delete_mission(mission)
        self.finished_missions.append(mission['db_name']
                                      .replace(' ', '_')
                                      .lower())
        self.current_mission = None

    def heal(self):
        """
        If player has healing salves then he heals(lol)
        """
        if self.count_utility_items() == 0:
            print("You don't have any healing salves!")
            return
        for item in self.items:
            if isinstance(item, items.Utility):
                if (self.hit_points + item.healing) > self.max_hit_points:
                    self.hit_points = self.max_hit_points
                else:
                    self.hit_points += item.healing
                self.items.pop(
                    self.items.index(item)
                )
                print(
                    "{} healed {} hit points!".format(
                        self.name,
                        item.healing
                    )
                )
                print(self)
                break

    def is_new_level(self):
        """
        Check whether player has enough experience to get new level
        """
        if self.experience >= ((self.level + 1) * 1000):
            print("You got level %d!" % (self.level + 1))
            self.level += 1
            self.experience -= self.level * 1000
            self.damage += 1
            self.max_hit_points += 10
            if self.level % 4 == 0:
                self.armor += 1
            print(self)

    def __str__(self):
        table = PrettyTable([self.name, 'Stats'])
        table.add_row(['HP',
                       '{}/{}'.format(
                           self.hit_points,
                           self.max_hit_points
                       )])
        table.add_row(['Damage', int(self.damage)])
        table.add_row(['Armor', int(self.armor)])
        table.add_row(['Level', self.level])
        table.add_row(['Experience', "{}/{}".format(
            self.experience,
            (self.level + 1) * 1000
        )])
        table.add_row(['Gold', self.gold])
        table.add_row(['Weight',
                       '{0:.2f}/{1}'.format(
                           self.current_weight,
                           self.weight
                       )])
        print(table)
        return ''


class Human(Unit):
    """
    Human class
    """

    def __init__(self, args):
        super().__init__(args)


class Orc(Unit):
    """
    Orc class
    """

    def __init__(self, args):
        super().__init__(args)


class Elf(Unit):
    """
    Elf class
    """

    def __init__(self, args):
        super().__init__(args)


class Demon(Unit):
    """
    Demon class
    """

    def __init__(self, args):
        super().__init__(args)


def fight(player, enemy):
    """
    Plays a fight between 2 Units
    """
    while True:
        player.attack(enemy)
        if not player.is_enemy_alive(enemy):
            player.is_new_level()
            break
        enemy.attack(player)
        if not enemy.is_enemy_alive(player):
            break


def fight_recap(player: Unit, enemy: Unit):
    """
    Prints fight recap between 2 Unit objects
    """
    if player.given_damage <= 0:
        player.given_damage = 0
    if enemy.given_damage <= 0:
        enemy.given_damage = 0
    print("Fight recap:\n")
    print("Player total damage dealt: %.f" % player.given_damage)
    print("Enemy total damage dealt: %.f\n" % enemy.given_damage)
