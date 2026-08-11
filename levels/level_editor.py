import sys

import pygame

from le_settings import LESettings


class LevelEditor:

    def __init__(self):
        pygame.init()

        # Variables
        self.settings = LESettings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.settings.screen_resolution)

    def run(self):
        """The main loop that runs the Level Editor"""

        while True:
            self.check_events()

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _update_screen(self):
        pygame.display.flip()

    def check_events(self):
        """Handles every event"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._key_down_events(event)

    def _key_down_events(self, event):
        """Handles every KeyBoard Down events"""

        if event.key == pygame.K_q:
            sys.exit()


if __name__ == '__main__':
    le = LevelEditor()
    le.run()
