import math

from pygame.sprite import Sprite
import pygame


class Bullet(Sprite):
    """Class that creates and takes care of bullets"""

    def __init__(self, st_game, shooter, angle, damage, size=10, color="black"):
        """Start all the needed variables"""

        super().__init__()

        # Base
        self.settings = st_game.settings
        self.screen = st_game.screen

        # Bullet
        self.bullet_color = color
        self.bullet_damage = damage
        self.bullet_radius = size
        self.bullet_distance = 80
        self.spawn_time = pygame.time.get_ticks()

        # Surface & Rect
        self.surface = pygame.Surface((self.bullet_radius*2, self.bullet_radius*2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        # Positioning
        self.cos_angle = math.cos(angle)
        self.sin_angle = math.sin(angle)
        self.centerx = shooter.rect.centerx
        self.centery = shooter.rect.centery

    def update(self):
        """Update the bullet every tick"""
        # Position and make the bullet move

        bullet_x = self.centerx + self.cos_angle * self.bullet_distance
        bullet_y = self.centery + self.sin_angle * self.bullet_distance
        self.rect.center = (bullet_x, bullet_y)
        self.bullet_distance += self.settings.bullet_speed

        # Despawn the bullet after a certain time
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.settings.bullet_despawn_time:
            self.kill()

    def drawme(self):
        pygame.draw.circle(self.surface, self.bullet_color,
                           (self.bullet_radius, self.bullet_radius), self.bullet_radius)
        self.screen.blit(self.surface, self.rect)