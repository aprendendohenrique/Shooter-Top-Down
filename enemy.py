import math
from math import atan2

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
        self.damage = 1

        # 1000 = 1 second
        self.enemy_attack_speed = 1000
        self.last_hit = pygame.time.get_ticks()


        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.midleft = self.screen_rect.midleft

        self.x_rect = float(self.rect.x)
        self.y_rect = float(self.rect.y)

    def update(self):

        distance_x = self.player.rect.centerx - self.rect.centerx
        distance_y = self.player.rect.centery - self.rect.centery

        angle = math.atan2(distance_y, distance_x)

        if not self.rect.colliderect(self.player.rect):
            self.x_rect += math.cos(angle) * self.settings.enemy_speed
            self.y_rect += math.sin(angle) * self.settings.enemy_speed
        elif pygame.time.get_ticks() - self.last_hit >= self.enemy_attack_speed:
            self.last_hit = pygame.time.get_ticks()
            self.player.get_hit(self.damage)

        self.rect.x = self.x_rect
        self.rect.y = self.y_rect

    def drawme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)