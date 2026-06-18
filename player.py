import math

import pygame
from pygame.sprite import Sprite


class Player(Sprite):
    """Class that manages the Player"""

    def __init__(self, st_game):
        """Start the needed variables"""

        super().__init__()

        # Base
        self.st_game = st_game
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect
        self.settings = st_game.settings
        self.tick = pygame.time.get_ticks()

        # Player color
        self.color = 255, 255, 255

        # Hit animation
        self.hit_color = (255, 0, 0)
        self.current_color = self.color
        self.got_hit = False
        self.got_hit_time = self.tick
        self.hit_animation_time = 100

        # Rect & Movement
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = self.screen_rect.center

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

        # Dash
        self.dashing = False
        self.can_dash = False
        self.last_time_dashed = self.tick
        self.last_x_vector = 0
        self.last_y_vector = 0

    def update(self):
        """---Update the player every tick---"""

        self.tick = pygame.time.get_ticks()

        """Movement"""

        # Set the vectors to zero
        x_vector = 0
        y_vector = 0

        # Checking if the user is trying and can dash
        if self.dashing and self.tick - self.last_time_dashed >= self.settings.dash_cooldown:
            self.last_time_dashed = self.tick
            self.can_dash = True

        if not self.can_dash:
            # Add or subtract one to the vector
            if self.moving_down:
                y_vector += 1
            if self.moving_up:
                y_vector -= 1
            if self.moving_right:
                x_vector += 1
            if self.moving_left:
                x_vector -= 1

            self.last_x_vector = x_vector
            self.last_y_vector = y_vector

            if x_vector != 0 or y_vector != 0:

                # Normalize the vector
                mag = math.sqrt(x_vector**2 + y_vector**2)

                y_vector /= mag
                x_vector /= mag

                # Moves the Player vertically
                self.y += y_vector * self.settings.player_speed
                self.rect.y = int(self.y)

                # Check for player/walls collisions
                collisions = pygame.sprite.spritecollide(self, self.st_game.scenario.collideable_objects, False)

                for _ in range(2):
                    for obj in collisions:
                        if y_vector > 0:
                            self.rect.bottom = obj.rect.top
                        if y_vector < 0:
                            self.rect.top = obj.rect.bottom
                        self.y = self.rect.y
                    collisions = pygame.sprite.spritecollide(self, self.st_game.enemies, False)

                # Moves the Player horizontally
                self.x += x_vector * self.settings.player_speed
                self.rect.x = int(self.x)

                # Checking for player/walls collisions
                collisions = pygame.sprite.spritecollide(self, self.st_game.scenario.collideable_objects, False)

                for _ in range(2):
                    for wall in collisions:
                        if x_vector > 0:
                            self.rect.right = wall.rect.left
                        elif x_vector < 0:
                            self.rect.left = wall.rect.right
                        self.x = self.rect.x
                    collisions = pygame.sprite.spritecollide(self, self.st_game.enemies, False)

        elif (self.last_x_vector != 0 or self.last_y_vector != 0) and self.tick - self.last_time_dashed < self.settings.dash_duration:

            # Normalize the vector
            mag = math.sqrt(self.last_x_vector ** 2 + self.last_y_vector ** 2)

            self.last_y_vector /= mag
            self.last_x_vector /= mag

            # Moves the Player vertically
            self.y += self.last_y_vector * self.settings.dash_speed
            self.rect.y = int(self.y)

            # Checking for player/walls collisions
            collisions = pygame.sprite.spritecollide(self, self.st_game.scenario.collideable_objects, False)

            for wall in collisions:
                if self.last_y_vector > 0:
                    self.rect.bottom = wall.rect.top
                if self.last_y_vector < 0:
                    self.rect.top = wall.rect.bottom
                self.y = self.rect.y

            # Moves the Player horizontally
            self.x += self.last_x_vector * self.settings.dash_speed
            self.rect.x = int(self.x)

            # Checking for player/walls collisions
            collisions = pygame.sprite.spritecollide(self, self.st_game.scenario.collideable_objects, False)

            for wall in collisions:
                if self.last_x_vector > 0:
                    self.rect.right = wall.rect.left
                elif self.last_x_vector < 0:
                    self.rect.left = wall.rect.right
                self.x = self.rect.x
        else:
            self.can_dash = False
            self.dashing = False

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        """Hit"""
        # Check if the animation is still going, if not, it runs the animation
        if self.got_hit and self.tick - self.got_hit_time >= self.hit_animation_time:
            self.got_hit = False
            self.current_color = self.color

    def drawme(self):
        pygame.draw.rect(self.screen, self.current_color, self.rect.move(-self.st_game.screen_x, -self.st_game.screen_y))

    def get_hit(self, damage):
        self.settings.player_health -= damage
        self.current_color = self.hit_color
        self.got_hit = True
        self.got_hit_time = pygame.time.get_ticks()
        if self.settings.player_health <= 0:
            self.st_game.game_over()

    def reposition_me(self, position=(0, 0), center=True):
        if center:
            self.rect.center = position
            self.x = self.rect.x
            self.y = self.rect.y
        else:
            self.rect.x = position[0]
            self.rect.y = position[1]
            self.x = self.rect.x
            self.y =self.rect.y