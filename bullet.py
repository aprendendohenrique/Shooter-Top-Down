import math

from pygame.sprite import Sprite
import pygame


class Bullet(Sprite):
    """Class that creates and takes care of bullets"""

    def __init__(self, st_game, shooter, angle, bullet_distance, damage, size=10, color="black", is_player=False):
        """Start all the needed variables"""

        super().__init__()

        # Base
        self.st_game = st_game
        self.settings = st_game.settings
        self.screen = st_game.screen
        self.is_player = is_player

        # Bullet
        self.bullet_color = color
        self.bullet_damage = damage
        self.bullet_radius = size
        self.bullet_distance = bullet_distance
        self.spawn_time = pygame.time.get_ticks()

        # Surface & Rect
        self.surface = pygame.Surface((self.bullet_radius*2, self.bullet_radius*2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

        # Positioning
        self.cos_angle = math.cos(angle)
        self.sin_angle = math.sin(angle)
        self.centerx = shooter.rect.centerx
        self.centery = shooter.rect.centery

        self.bullet_x = self.centerx + self.cos_angle * self.bullet_distance
        self.bullet_y = self.centery + self.sin_angle * self.bullet_distance
        self.rect.center = (self.bullet_x, self.bullet_y)

    def update(self):
        """Update the bullet every tick"""
        # Position and make the bullet move

        self.bullet_x += self.cos_angle * self.settings.bullet_speed
        self.bullet_y += self.sin_angle * self.settings.bullet_speed
        self.rect.center = (self.bullet_x, self.bullet_y)

        # Despawn the bullet after a certain time
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.settings.bullet_despawn_time:
            self.kill()

    def drawme(self):
        pygame.draw.circle(self.surface, self.bullet_color,
                           (self.bullet_radius, self.bullet_radius), self.bullet_radius)
        self.screen.blit(self.surface, self.rect.move(-self.st_game.screen_x, -self.st_game.screen_y))