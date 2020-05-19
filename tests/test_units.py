import unittest

from core import database
from core.units import Player, Human, fight
from core import DeadHero


class TestUnits(unittest.TestCase):
    def setUp(self):
        self.player = Player("Testing")

    def test_create_player(self):
        """
        Testing creation of Player
        """
        self.assertIsNotNone(self.player)
        self.assertEqual(self.player.name, "Testing")

    def test_fight(self):
        """
        Testing fight between two units
        """
        enemy = Human(["Name", 20, 5, 2, 1, 50, 50, None, None, None, None,
                       None, None, None, None, None])
        self.assertIsNotNone(enemy)

        fight(self.player, enemy)

        self.assertLessEqual(enemy.hit_points, 0)
        self.assertLessEqual(self.player.hit_points,
                             self.player.max_hit_points)
        self.assertEqual(self.player.experience, enemy.reward_experience)
        self.assertEqual(self.player.gold, enemy.reward)
        self.assertTrue(self.player.is_alive())

    def test_player_dying(self):
        """
        Testing death of main hero
        """
        enemy = Human(["Name", 20, 40, 2, 1, 50, 50, None, None, None, None,
                       None, None, None, None, None])

        self.assertIsNotNone(enemy)

        with self.assertRaises(DeadHero):
            fight(self.player, enemy)

        self.assertEqual(self.player.hit_points, 0)
        self.assertGreaterEqual(enemy.given_damage, self.player.hit_points)
        self.assertFalse(self.player.is_alive())

    def test_configuring_em(self):
        """
        Testing configuration of not player' equipment model
        """
        right_hand = database.get_item_from_db("Test spear")
        left_hand = database.get_item_from_db("Test buckler")
        helmet = database.get_item_from_db("Heavy helmet")
        chest = database.get_item_from_db("Test chest")
        arms = database.get_item_from_db("Test arms")
        legs = database.get_item_from_db("Test legs")

        human = Human(["Name", 20, 5, 2, 1, 50, 50, right_hand, left_hand,
                       helmet, chest, arms, legs, None, None, None])

        self.assertGreater(human.damage, 5)
        self.assertGreater(human.armor, 1)
        self.assertIsNotNone(human.left_hand)
        self.assertIsNotNone(human.right_hand)
        self.assertIsNotNone(human.head)

    def test_creating_armor_set(self):
        """
        Testing creation of armor set
        """
        self.player.head = database.get_item_from_db("Heavy helmet")
        self.player.chest = database.get_item_from_db("Test chest")
        self.player.arms = database.get_item_from_db("Test arms")
        self.player.legs = database.get_item_from_db("Test legs")

        self.assertIsNotNone(self.player.head)
        self.assertIsNotNone(self.player.chest)
        self.assertIsNotNone(self.player.arms)
        self.assertIsNotNone(self.player.legs)

        armor_set = self.player.create_armor_set()

        self.assertEqual(len(armor_set), 4)
        self.assertEqual(sum(armor_set), 42)

    def test_using_item(self):
        self.player.add_item_to_backpack(
            database.get_item_from_db("Test spear"))

    def test_handling_weapon_level(self):
        """
        Testing handling of weapons
        """
        self.player.hit_points = 100
        self.player.add_item_to_backpack(
            database.get_item_from_db("Test spear"))
        self.player.use_item("Test spear")

        enemies = [Human(["Name", 20, 0, 2, 1, 50, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 0, 2, 1, 50, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 0, 2, 1, 50, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 0, 2, 1, 50, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 0, 2, 1, 50, 50, None, None, None, None,
                          None, None, None, None, None]),
                  ]

        for enemy in enemies:
            fight(self.player, enemy)
            self.assertEqual(enemy.hit_points, 0)
            self.assertEqual(enemy.given_damage, 0)

        self.assertEqual(self.player.spear_level, 2)
        self.assertEqual(int(self.player.damage
                             - self.player.weapon_type_damage(
                                 self.player.right_hand)), 6)

    def test_handling_armor_level(self):
        """
        Testing handling of armor level
        """
        self.player.add_item_to_backpack(
            database.get_item_from_db("Heavy helmet"))
        self.player.add_item_to_backpack(
            database.get_item_from_db("Test chest"))
        self.player.add_item_to_backpack(
            database.get_item_from_db("Test arms"))
        self.player.add_item_to_backpack(
            database.get_item_from_db("Test legs"))

        self.player.use_item("Heavy helmet")
        self.player.use_item("Test chest")
        self.player.use_item("Test arms")
        self.player.use_item("Test legs")

        self.assertIsNotNone(self.player.head)
        self.assertIsNotNone(self.player.chest)
        self.assertIsNotNone(self.player.arms)
        self.assertIsNotNone(self.player.legs)

        self.assertEqual(self.player.armor
                         - sum(self.player.create_armor_set()), 2)

        enemies = [Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                   Human(["Name", 20, 30, 2, 1, 3, 50, None, None, None, None,
                          None, None, None, None, None]),
                  ]

        for enemy in enemies:
            fight(self.player, enemy)
            self.assertEqual(enemy.hit_points, 0)
            self.player.hit_points = self.player.max_hit_points
        self.assertEqual(self.player.heavy_armor_level, 2)


if __name__ == "__main__":
    unittest.main()
