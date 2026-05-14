import math

import pygame

class Player:
    """Class that creates and manages the player"""

    def __init__(self, st_game):
        """All the needed variables"""
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect
        self.settings = st_game.settings

        self.color = 255, 255, 255

        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = self.screen_rect.center

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):

        # Set the vectors to zero
        x_vector = 0
        y_vector = 0

        # Adds or subtract one to the vector
        if self.moving_down:
            y_vector += 1
        if self.moving_up:
            y_vector -= 1
        if self.moving_right:
            x_vector += 1
        if self.moving_left:
            x_vector -= 1

        # Normalize the vector and adds it to the players position
        if x_vector != 0 or y_vector != 0:
            mag = math.sqrt(x_vector**2 + y_vector**2)

            y_vector /= mag
            x_vector /= mag

            self.y += y_vector * self.settings.player_speed
            self.x += x_vector * self.settings.player_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def drawme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)