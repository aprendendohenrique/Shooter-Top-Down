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
        self.screen_rect = self.screen.get_rect()

        self.show_grid = True

        self.button = Button(self, 420, 430, 50, 50)

    def run(self):
        """The main loop that runs the Level Editor"""

        while True:
            self.check_events()

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _update_screen(self):
        self.screen.fill(self.settings.background_color)

        self.button.draw_me()

        if self.show_grid:
            self.draw_lines()

        pygame.display.flip()

    def check_events(self):
        """Handles every event"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._key_down_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_down_events()

    def _key_down_events(self, event):
        """Handles every KeyBoard Down events"""

        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_g:
            if self.show_grid:
                self.show_grid = False
            else:
                self.show_grid = True

    def _mouse_down_events(self):
        x, y = pygame.mouse.get_pos()
        cor_x = x - self.settings.x_offset
        cor_y = y - self.settings.y_offset

        x_border = self.screen.get_width() - self.settings.x_offset
        y_border = self.screen.get_height() - self.settings.y_offset
        if (cor_x > 0 and cor_y > 0) and (x < x_border and y < y_border):
            x_grid = (x - self.settings.x_offset) // 32
            y_grid = (y - self.settings.y_offset) // 32

            print(f"x: {x_grid + 1} y: {y_grid + 1}")
        elif self.button.rect.collidepoint(x, y):
            print("Clicked Button!")

    def draw_lines(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        x_of = self.settings.x_offset
        y_of = self.settings.y_offset

        for x in range(0 + x_of, width - x_of, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(x, 0 + y_of), end_pos=(x, height - y_of), width=self.settings.grid_width)

        for y in range(0 + y_of, height - y_of, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(0 + x_of, y), end_pos=(width - x_of, y), width=self.settings.grid_width)

class Button:

    def __init__(self, le_editor, x, y, width, height, color=(0, 0, 0)):
        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect

        self.color = color

        self.rect = pygame.Rect(x, y, width, height)

    def draw_me(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class SegmentedButton:

    def __init__(self):
        """Class that creates many buttons that only one can be selected."""
        ...

if __name__ == '__main__':
    le = LevelEditor()
    le.run()
