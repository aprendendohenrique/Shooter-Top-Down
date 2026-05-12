import pygame

class Player:
    """Class that creates and manages the player"""

    def __init__(self, st_game):
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
        if self.moving_down:
            self.y += self.settings.player_speed
        if self.moving_up:
            self.y += self.settings.player_speed * -1
        if self.moving_right:
            self.x += self.settings.player_speed
        if self.moving_left:
            self.x += self.settings.player_speed * -1
        self.rect.x = self.x
        self.rect.y = self.y

    def drawme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)