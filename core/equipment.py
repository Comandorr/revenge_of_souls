"""
Source file contains equipment player model.
It allows to manage player' weapon and armor
"""

import prettytable

from core import items


class EquipmentModel(object):

    def __init__(self):
        """
        Weapon and shield:
        right_hand
        left_hand

        Armor:
        head
        chest
        arms
        legs

        Additions:
        ring
        necklace
        3 artifacts (list)
        """
        self.right_hand = None
        self.left_hand = None
        self.head = None
        self.chest = None
        self.arms = None
        self.legs = None
        self.ring = None
        self.necklace = None
        self.artifacts = []

    def __str__(self):
        template_table = prettytable.PrettyTable(['Name of stat', 'Stat'])

        if self.right_hand is not None:
            template_table.add_row([self.right_hand.name,
                                    "%d damage" % self.right_hand.damage])
        if self.left_hand is not None:
            if isinstance(self.left_hand, items.Weapon):
                template_table.add_row([self.left_hand.name,
                                        "%d damage" % self.left_hand.damage])
            elif isinstance(self.left_hand, items.Shield):
                template_table.add_row([self.left_hand.name,
                                        "%d armor" % self.left_hand.armor])
            elif self.right_hand == self.left_hand:
                pass

        if self.head is not None:
            template_table.add_row([self.head.name,
                                    "%d armor" % self.head.armor])

        if self.chest is not None:
            template_table.add_row([self.chest.name,
                                    "%d armor" % self.chest.armor])

        if self.arms is not None:
            template_table.add_row([self.arms.name,
                                    "%d armor" % self.arms.armor])

        if self.legs is not None:
            template_table.add_row([self.legs.name,
                                    "%d armor" % self.legs.armor])

        if self.ring is not None:
            template_table.add_row([self.ring.name,
                                    "%s" % self.ring.description])

        if self.necklace is not None:
            template_table.add_row([self.necklace.name,
                                    "%s" % self.necklace.description])

        if len(self.artifacts) > 0:
            for num, value in enumerate(self.artifacts):
                template_table.add_row([value.name,
                                        "%s" % value.description])
        print(template_table)
        return ''
