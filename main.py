#!/usr/bin/env python3
"""
Main file of "Revenge of Souls" game.
Contains only main method
"""

import sys


def main():
    """
    Main method
    """
    if sys.version_info.major < 3 or (sys.version_info.major == 3 and
                                      sys.version_info.minor < 5):
        print("Our game uses Python version >=3.5.")
        sys.exit(1)

    from core.menus import main_menu
    main_menu()


if __name__ == '__main__':
    main()
