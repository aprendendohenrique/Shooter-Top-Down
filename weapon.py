import math

import pygame


class Weapon:
    """The class that create and manages the player's weapon."""

    def __init__(self, st_game, player):
        """All the needed variables"""
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect
        self.settings = st_game.settings
        self.player = player

        self.color = 50, 50, 50
        self.weapon_width = 55
        self.weapon_height = 12
        self.distance = 40

        self.gun_surface = pygame.Surface((self.weapon_width, self.weapon_height), pygame.SRCALPHA)

    def update(self):
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.player.rect.centerx
        dy = mouse_y - self.player.rect.centery

        self.angle = math.atan2(dy, dx)

        weapon_x = self.player.rect.centerx + math.cos(self.angle) * self.distance
        weapon_y = self.player.rect.centery + math.sin(self.angle) * self.distance

        angle = math.degrees(self.angle)

        self.rotated_surface = pygame.transform.rotate(self.gun_surface, -angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=(weapon_x, weapon_y))

    def drawme(self):
        pygame.draw.rect(self.gun_surface, self.color, (0, 0, self.weapon_width, self.weapon_height))
        # Draw a line from the player to the mouse
        pygame.draw.line(self.screen, "red", self.player.rect.center, pygame.mouse.get_pos(), 3)
        self.screen.blit(self.rotated_surface, self.rotated_rect)