import unittest
import sqlite3

from core import database
from core import items
from core import units


class TestDatabase(unittest.TestCase):

    def test_getting_item(self):
        item = database.get_item_from_db("Test spear")

        self.assertIsNotNone(item)
        self.assertIsInstance(item, items.Weapon)
        self.assertEqual(item.name, "Test spear")

    def test_getting_city(self):
        city = database.get_city_from_db("Unggal")

        self.assertEqual(city.name, "Unggal")

    def test_getting_text(self):
        text = database.get_text_from_db("prologue")

        self.assertIsNotNone(text)

    def test_getting_unit(self):
        unit = database.get_unit_from_db("Melcar")

        self.assertIsNotNone(unit)
        self.assertIsInstance(unit, units.Demon)

        weapon = database.get_item_from_db("Melcar Sword")

        self.assertIsNotNone(unit.right_hand)
        self.assertEqual(weapon.name, unit.right_hand.name)

    def test_getting_list_of_cities(self):
        import sqlite3
        count = 0
        with sqlite3.connect("ros.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT count(*) FROM cities;")
            count = cursor.fetchone()
            cursor.close()

        cities = database.get_list_of_cities()

        self.assertEqual(len(cities), count[0])

    def test_failed_getting_item(self):
        with self.assertRaises(sqlite3.OperationalError):
            database.get_item_from_db("YO MAMA")
