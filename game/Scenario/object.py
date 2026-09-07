import pygame
from pygame.sprite import Sprite


class Object(Sprite):
    """Class that manages a simple object"""

    def __init__(self, st_game, width, height, x, y, color="grey", image=None):
        super().__init__()
        self.st_game = st_game
        self.screen = st_game.screen
        self.player = self.st_game.player

        self.image = image
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def drawme(self):
        if self.image:
            self.screen.blit(self.image, (self.rect.x - self.st_game.screen_x, self.rect.y - self.st_game.screen_y))
        else:
            pygame.draw.rect(
                self.screen,
                self.color,
                self.rect.move(-self.st_game.screen_x, -self.st_game.screen_y),
            )
