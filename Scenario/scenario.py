from Scenario.wall import Wall


class Scenario:
    """Class that manages all the scenario objects"""

    def __init__(self, st_game):
        self.screen = st_game.screen

        self.wall = Wall(st_game, self.screen.get_width(), self.screen.get_height(),-25, -25)

    def draw_scenario(self):
        self.wall.drawme()
