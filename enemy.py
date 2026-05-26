import math

import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """Main class that manages the simple enemy."""
    
    def __init__(self, st_game):
        super().__init__()
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect
        self.settings = st_game.settings
        self.player = st_game.player

        self.color = (255, 0, 0)
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.midleft = self.screen_rect.midleft

        self.x_rect = float(self.rect.x)
        self.y_rect = float(self.rect.y)

    def update(self):
        x_vector = 0
        y_vector = 0

        distance_x = self.player.rect.centerx - self.rect.centerx
        distance_y = self.player.rect.centery - self.rect.centery

        if distance_x > 0:
            x_vector += 1
        elif distance_x < 0:
            x_vector -= 1
        if distance_y > 0:
            y_vector += 1
        elif distance_y < 0:
            y_vector -= 1

        if x_vector != 0 or y_vector != 0:
            mag = math.sqrt(x_vector**2 + y_vector**2)

            x_vector /= mag
            y_vector /= mag

            self.x_rect += x_vector * self.settings.enemy_speed
            self.y_rect += y_vector * self.settings.enemy_speed

        self.rect.x = self.x_rect
        self.rect.y = self.y_rect
        print(self.rect)

    def drawme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)