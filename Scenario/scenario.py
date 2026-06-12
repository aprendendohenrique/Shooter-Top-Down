from Scenario.wall import Wall


class Scenario:
    """Class that manages all the scenario objects"""

    def __init__(self, st_game):
        self.screen = st_game.screen

        self.wall = Wall(st_game, self.screen.get_width() + 50, self.screen.get_height() + 50,0, 0)

    def draw_scenario(self, screen_x, screen_y):
        self.wall.drawme(screen_x, screen_y)
