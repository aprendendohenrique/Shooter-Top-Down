import math

import pygame

from Weapons.weapon import Weapon
from bullet import Bullet


class Rifle(Weapon):
    """Class that manages the Rifle weapon"""
    
    def __init__(self, st_game, player):
        super().__init__(st_game, player)
        self.bullet_distance = self.weapon_height + self.distance + 20

    def update(self, screen_x, screen_y):
        """Update the enemy every tick"""
        # Position the weapon around the player

        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_world_x = mouse_x + screen_x
        mouse_world_y = mouse_y + screen_y

        dx = mouse_world_x - self.player.rect.centerx
        dy = mouse_world_y - self.player.rect.centery

        self.angle = math.atan2(dy, dx)

        weapon_x = self.player.rect.centerx + math.cos(self.angle) * self.distance
        weapon_y = self.player.rect.centery + math.sin(self.angle) * self.distance

        angle = math.degrees(self.angle)

        self.rotated_surface = pygame.transform.rotate(self.gun_surface, -angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=(weapon_x, weapon_y))

        if self.st_game.is_shooting:
            if pygame.time.get_ticks() - self.last_time_shot  >= self.settings.firerate:
                bullet = Bullet(self.st_game, self.player, self.angle, self.bullet_distance,
                                self.damage, is_player=True)
                self.st_game.bullets.add(bullet)
                self.last_time_shot = pygame.time.get_ticks()

    def drawme(self, screen_x, screen_y):
        # Draw a rectangle inside the gun_surface
        pygame.draw.rect(self.gun_surface, self.color, (0, 0, self.weapon_width, self.weapon_height))

        # Blit(put) the rotated_surface(gun_surface but rotated) to the screen
        self.screen.blit(self.rotated_surface, self.rotated_rect.move(-screen_x, -screen_y))

        # Draw a line from the player to the mouse
        # pygame.draw.line(self.screen, "red", self.player.rect.center, pygame.mouse.get_pos(), 3)
