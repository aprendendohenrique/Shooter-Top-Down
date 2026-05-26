import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """Main class that manages the simple enemy."""
    
    def __init__(self, st_game):
        super().__init__()
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect
        self.settings = st_game.settings

        self.color = (255, 0, 0)
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.midleft = self.screen_rect.midleft

    def drawme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)