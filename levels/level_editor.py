import json
import sys
from pathlib import Path

import pygame

from le_settings import LESettings
from le_buttons import Button
from le_buttons import SegmentedButton
from le_tileset_reader import TileSetReader
from le_objects import Tile
from levels.le_objects import UIObject


class LevelEditor:

    def __init__(self):
        pygame.init()

        # Variables
        self.settings = LESettings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.settings.screen_resolution)
        self.screen_rect = self.screen.get_rect()

        self.BASE_DIR = Path(__file__).resolve().parent
        self.ASSETS_DIR = self.BASE_DIR / "images" / "assets"

        self.grass_tileset = TileSetReader(self, self.ASSETS_DIR / "grass_tileset.png", 32, 32)

        self.show_grid = True

        self.tile = None
        self.tile_id = None
        self.tiles = pygame.sprite.Group()

        #Save
        self.save = [{"grass_tileset": []}]

        # UI Objects
        self.seg_button = SegmentedButton(self, 25, 0, 5, images=self.grass_tileset, vertical=True)
        self.seg_button.center_y()

        cover_color = (220, 220, 220)
        self.upper_cover = UIObject(self, 0, 0, self.screen.get_width(), 100, color=cover_color)
        self.left_cover = UIObject(self, 0, 0, 100, self.screen.get_height(), color=cover_color)

    def run(self):
        """The main loop that runs the Level Editor"""

        while True:
            self.check_events()

            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _update_screen(self):
        self.screen.fill(self.settings.background_color)

        if self.show_grid:
            self.draw_lines()

        # UIObjects
        for tile in self.tiles:
            tile.draw_me()

        self.upper_cover.draw_me()
        self.left_cover.draw_me()
        self.seg_button.draw_me()

        horizontal = pygame.draw.line(self.screen, "red", (self.screen.get_width()/2, 0), (self.screen.get_width()/2, self.screen.get_height()))
        vertical = pygame.draw.line(self.screen, "red", (0, self.screen.get_height()/2), (self.screen.get_width(), self.screen.get_height()/2))

        pygame.display.flip()

    def check_events(self):
        """Handles every event"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._save_things()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._key_down_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_down_events()

    def _key_down_events(self, event):
        """Handles every KeyBoard Down events"""

        if event.key == pygame.K_q:
            self._save_things()
            sys.exit()
        elif event.key == pygame.K_g:
            if self.show_grid:
                self.show_grid = False
            else:
                self.show_grid = True

    def _save_things(self):
        with open("save.json", "w") as file:
            json.dump(self.save, file, indent=4)

    def _mouse_down_events(self):
        x, y = pygame.mouse.get_pos()

        # Grid clicked
        self._grid_clicked(x, y)

        # Asset seg button clicked
        self._asset_clicked()

    def _grid_clicked(self, x, y):
        if not self.left_cover.rect.collidepoint(x, y) and not self.upper_cover.rect.collidepoint(x, y):
            if (x > -self.settings.grid_size and y > -self.settings.grid_size) and (x < self.screen_rect.width + self.settings.grid_size and y < self.screen_rect.height + self.settings.grid_size):
                x_grid = x // 32
                y_grid = y // 32

                print(f"x: {x_grid + 1} y: {y_grid + 1}")

                if self.tile is not None:
                    # If any tile, replace the tile
                    if self.tiles:
                        for tile in self.tiles:
                            tile.clicked(destroy=True)

                    tile = Tile(self, x_grid * self.settings.TILE_SIZE, y_grid * self.settings.TILE_SIZE, self.tile)
                    self.tiles.add(tile)

                    self.save[0]["grass_tileset"].append({"tile_id": self.tile_id, "position": [tile.rect.x, tile.rect.y]})
                else:
                    for tile in self.tiles:
                        tile.clicked(destroy=True)

    def _asset_clicked(self):
        button_id = self.seg_button.clicked()
        if button_id is not None:
            if self.tile != self.seg_button.images[button_id]:
                self.tile = self.seg_button.images[button_id]
                self.tile_id = button_id
            else:
                self.tile = None

    def draw_lines(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        for x in range(0 - self.settings.grid_size, width + self.settings.grid_size, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(x, -self.settings.grid_size), end_pos=(x, height + self.settings.grid_size), width=self.settings.grid_width)

        for y in range(0 - self.settings.grid_size, height + self.settings.grid_size, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(-self.settings.grid_size, y), end_pos=(width + self.settings.grid_size, y), width=self.settings.grid_width)

if __name__ == '__main__':
    le = LevelEditor()
    le.run()
