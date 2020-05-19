class City(object):
    """
    An implementaion of RoS cities
    """

    def __init__(self, city_info: list):
        self.name = city_info[0]  # type: str
        self.country = city_info[1]  # type: str
        self.king = city_info[2]  # type: str
        self.items = city_info[3]  # type: list
        self.missions = city_info[4]  # type: list
        self.level = city_info[5]  # type: int
        self.opened = city_info[6]  # type: bool

    def list_missions(self):
        """
        Prints out list of missions that city has
        """
        for mission in self.missions:
            print(mission)

    def __str__(self):
        return "Name: {}\nCountry: {}\nOpened: {}\n".format(
                self.name, self.country, self.opened
            )
