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
        self.screen.fill(self.settings.background_color)

        self.draw_lines()

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

    def draw_lines(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        for x in range(0, width, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(x, 0), end_pos=(x, height), width=1)

        for y in range(0, height, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(0, y), end_pos=(width, y), width=1)


if __name__ == '__main__':
    le = LevelEditor()
    le.run()
