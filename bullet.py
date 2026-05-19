import math

from pygame.sprite import Sprite
import pygame


class Bullet(Sprite):
    """Class that creates and takes care of bullets"""

    def __init__(self,st_game):
        super().__init__()
        self.setting = st_game.settings
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect
        self.weapon = st_game.weapon
        self.player = st_game.player

        self.bullet_color = "black"
        self.bullet_radius = 10
        self.bullet_distance = 80

        self.surface = pygame.Surface((self.bullet_radius*2, self.bullet_radius*2), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()

    def update(self):
        bullet_x = self.player.rect.centerx + math.cos(self.weapon.angle) * self.bullet_distance
        bullet_y = self.player.rect.centery + math.sin(self.weapon.angle) * self.bullet_distance
        self.surface_rect.center = (bullet_x, bullet_y)

    def drawme(self):
        pygame.draw.circle(self.surface, self.bullet_color,
                           (self.bullet_radius, self.bullet_radius), self.bullet_radius)
        self.screen.blit(self.surface, self.surface_rect)