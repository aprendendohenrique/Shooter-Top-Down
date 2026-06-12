import pygame
from pygame.sprite import Sprite


class Wall(Sprite):
    """Class that manages a simple wall"""

    def __init__(self, st_game, width, height, x, y, color="grey"):
        super().__init__()
        self.st_game = st_game
        self.screen = st_game.screen

        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        print("hi")

    def drawme(self):
        pygame.draw.rect(self.screen, self.color, self.rect.move(-self.st_game.screen_x, -self.st_game.screen_y))

