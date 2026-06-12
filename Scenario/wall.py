import pygame
from pygame.sprite import Sprite


class Wall(Sprite):
    """Class that manages a simple wall"""

    def __init__(self, st_game, width, height, x, y, color="grey"):
        super().__init__()
        self.screen = st_game.screen

        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.xi = 0

    def drawme(self, screen_x, screen_y):
        pygame.draw.rect(self.screen, self.color, self.rect.move(-screen_x, -screen_y))

