import math

import pygame

from Weapons.weapon import Weapon
from bullet import Bullet


class Shotgun(Weapon):
    """Class that manages the Shotgun weapon."""

    def __init__(self, st_game, player):
        super().__init__(st_game, player)
        self.color = 100, 10, 10
        self.weapon_width = 48
        self.weapon_height = 22
        self.bullet_distance = self.weapon_height + self.distance + 8

        self.gun_surface = pygame.Surface((self.weapon_width, self.weapon_height), pygame.SRCALPHA)

        # Shotgun unique parameters
        self.spread = 0.1

    def update(self):
        """Update the enemy every tick"""
        # Position the weapon around the player

        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.player.rect.centerx
        dy = mouse_y - self.player.rect.centery

        self.angle = math.atan2(dy, dx)

        weapon_x = self.player.rect.centerx + math.cos(self.angle) * self.distance
        weapon_y = self.player.rect.centery + math.sin(self.angle) * self.distance

        angle = math.degrees(self.angle)

        self.rotated_surface = pygame.transform.rotate(self.gun_surface, -angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=(weapon_x, weapon_y))

        if self.is_shooting:
            if pygame.time.get_ticks() - self.last_time_shot  >= self.settings.firerate:
                self.angle += self.spread * 2
                for _ in range(5):
                    bullet = Bullet(self.st_game, self.player, self.angle, self.bullet_distance,
                                    self.settings.player_damage, is_player=True, size=7)
                    self.st_game.bullets.add(bullet)
                    self.angle -= self.spread
                self.last_time_shot = pygame.time.get_ticks()

    def drawme(self):
        # Draw a rectangle inside the gun_surface
        pygame.draw.rect(self.gun_surface, self.color, (0, 0, self.weapon_width, self.weapon_height))

        # Blit(put) the rotated_surface(gun_surface but rotated) to the screen
        self.screen.blit(self.rotated_surface, self.rotated_rect)

        # Draw a line from the player to the mouse
        pygame.draw.line(self.screen, "red", self.player.rect.center, pygame.mouse.get_pos(), 3)