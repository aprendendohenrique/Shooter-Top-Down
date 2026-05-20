import math

from pygame.sprite import Sprite
import pygame


class Bullet(Sprite):
    """Class that creates and takes care of bullets"""

    def __init__(self,st_game):
        super().__init__()
        self.settings = st_game.settings
        self.screen = st_game.screen

        self.bullet_color = "black"
        self.bullet_radius = 10
        self.bullet_distance = 80

        self.surface = pygame.Surface((self.bullet_radius*2, self.bullet_radius*2), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect()

        self.cos_angle = math.cos(st_game.weapon.angle)
        self.sin_angle = math.sin(st_game.weapon.angle)
        self.centerx = st_game.player.rect.centerx
        self.centery = st_game.player.rect.centery

    def update(self):
        bullet_x = self.centerx + self.cos_angle * self.bullet_distance
        bullet_y = self.centery + self.sin_angle * self.bullet_distance
        self.surface_rect.center = (bullet_x, bullet_y)
        self.bullet_distance += self.settings.bullet_speed

    def drawme(self):
        pygame.draw.circle(self.surface, self.bullet_color,
                           (self.bullet_radius, self.bullet_radius), self.bullet_radius)
        self.screen.blit(self.surface, self.surface_rect)