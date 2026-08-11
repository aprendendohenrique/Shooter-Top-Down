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

        x_of = self.settings.x_offset
        y_of = self.settings.y_offset

        for x in range(0 + x_of, width - x_of, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(x, 0 + y_of), end_pos=(x, height - y_of), width=1)

        for y in range(0 + y_of, height - y_of, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(0 + x_of, y), end_pos=(width - x_of, y), width=1)


if __name__ == '__main__':
    le = LevelEditor()
    le.run()
