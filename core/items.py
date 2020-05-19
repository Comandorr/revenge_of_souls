"""
Source file contains all item classes of the game
"""


class Item(object):
    """
    Abstraction of Revenge Of Souls item. Exists only for inheritance
    """

    def __init__(self, args):
        self.name = args[0]
        self.description = args[1]
        self.price = args[2]
        self.type = args[3]
        self.weight = args[6]
        self.using = False

    def is_utility(self):
        """
        Checks whether self isinstance of Utility class
        """
        return isinstance(self, Utility)

    def is_weapon(self):
        """
        Checks whether self isinstance of Weapon class
        """
        return isinstance(self, Weapon)

    def is_shield(self):
        """
        Checks whether self isinstance of Shield class
        """
        return isinstance(self, Shield)

    def is_armor(self):
        """
        Checks whether self isinstance of Armor class
        """
        return isinstance(self, Armor)

    def is_using(self):
        """
        Returns 'yes' or 'not'
        """
        if self.using:
            return 'Yes'
        else:
            return 'No'


class Weapon(Item):
    """
    Implementation of RoS weapon.
    """

    def __init__(self, args):
        super().__init__(args)
        self.damage = args[4]
        self.two_handed = True if ('Two-handed' in self.type or
                                   'Spear' in self.type) else False
        self.using_as_two_handed = True if ('Two-handed' in self.type or
                                            'Spear' in self.type) else False

    def __str__(self):
        template = ("{} stats:\nDescription - {}\nType - {}\n"
                    "Damage - {}\nUsing - {}\nPrice - {} gold\n"
                    "Two-handed - {}\nUsing as two-handed - {}\n"
                    "Weight - {}\n")
        return template.format(
            self.name,
            self.description,
            self.type,
            self.damage,
            self.is_using(),
            self.price,
            'Yes' if self.two_handed else 'No',
            'Yes' if self.using_as_two_handed else 'No',
            self.weight
        )


class Armor(Item):
    """
    Implementation of all armor items in RoS.
    Instance can be helmet, chest, arms or legs.
    """

    def __init__(self, args):
        super().__init__(args)
        self.armor = args[4]
        self.block_percentage = args[5]

    def __str__(self):
        template = ("{} stats:\nDescription - {}\nType - {}\n"
                    "Armor - {}\nUsing - {}\nPrice - {} gold\n"
                    "Weight - {}\n")
        return template.format(
            self.name,
            self.description,
            self.type,
            self.armor,
            self.is_using(),
            self.price,
            self.weight
        )


class Shield(Armor):
    """
    Implementation of RoS shield.
    """

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return super().__str__()


class Utility(Item):
    """
    Implementation of RoS utility items, such as Healing Salve,
    Mana Salve, etc.
    """

    def __init__(self, args):
        super().__init__(args)
        self.healing = args[4]

    def __str__(self):
        template = ("\n{} stats:\nDescription - {}\nType - {}\n"
                    "Healing - {}\nWeight - {}\nPrice - {}\n")
        return template.format(
            self.name,
            self.description,
            self.type,
            self.healing,
            self.weight,
            self.price
        )
