import json

import pygame.sprite

from game.Scenario.object import Object
from levels.le_tileset_reader import TileSetsReader


class Scenario:
    """Class that manages all the scenario objects"""

    def __init__(self, st_game):
        self.st_game = st_game
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect
        self.settings = st_game.settings

        # Tilesets
        self.tilesets = TileSetsReader(self, st_game.TILESETS_DIR, 32, 32)

        self.non_collideable_objects = pygame.sprite.Group()
        self.collideable_objects = pygame.sprite.Group()

        self.load_scenario()

    def draw_scenario(self):
        for obj in self.collideable_objects:
            obj.drawme()
        for obj in self.non_collideable_objects:
            obj.drawme()

    def load_scenario(self):
        with open(self.st_game.BASE_DIR / "levels" / "save.json", "r") as file:
            scenario = json.load(file)
        for tileset in self.tilesets:
            for sprite in scenario[tileset]:
                tile = Object(self.st_game, self.tilesets[tileset][0]["surface"].get_width(), self.tilesets[tileset][0]["surface"].get_height(), sprite["position"][0], sprite["position"][1], image=self.tilesets[tileset][sprite["tile_id"]]["surface"])
                if sprite["collidable"]:
                    self.collideable_objects.add(tile)
                else:
                    self.non_collideable_objects.add(tile)

