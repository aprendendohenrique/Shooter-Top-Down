import math

import pygame


class Weapon:
    """The class that create and manages the player's weapon."""

    def __init__(self, st_game, player):
        """Start the needed variables"""

        # Basic
        self.st_game = st_game
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect
        self.settings = st_game.settings
        self.player = player

        # Weapon
        self.damage = 1
        self.color = 50, 50, 50
        self.weapon_width = 55
        self.weapon_height = 12
        self.distance = 40
        self.last_time_shot = pygame.time.get_ticks()

        self.gun_surface = pygame.Surface((self.weapon_width, self.weapon_height), pygame.SRCALPHA)