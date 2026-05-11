import sys

import pygame

import settings


class ShooterTopdown:
    """The main class that control and run the game"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _update_screen(self):
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._key_down_event(event)

    def _key_down_event(self, event):
        if event.key == pygame.K_q:
            sys.exit()

st_game = ShooterTopdown()
st_game.run_game()