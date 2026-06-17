import pygame.sprite

from Scenario.wall import Wall


class Scenario:
    """Class that manages all the scenario objects"""

    def __init__(self, st_game):
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect

        self.collideable_objects = pygame.sprite.Group()

        self.wall = Wall(st_game, 200, 50, 0, 150)
        self.wall.rect.centerx = self.screen_rect.centerx

        self.collideable_objects.add(self.wall)

    def draw_scenario(self):
        for wall in self.collideable_objects:
            wall.drawme()