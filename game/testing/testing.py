import sys

import pygame

from settings import Settings


class Testing:
    """The main class for me test general things on pygame"""

    def __init__(self):
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.settings.screen_resolution, True, True
        )

    def run_game(self):
        while True:
            # All game events
            self._check_events()

            # Updates the screen
            self._update_screen()

            # Set the fps
            self.clock.tick(self.settings.fps)

    def _update_screen(self):
        self.screen.fill(self.settings.background_color)
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


testing = Testing()
testing.run_game()
