import json

import pygame.sprite

from game.Scenario.object import Object
from levels.le_tileset_reader import TileSetReader


class Scenario:
    """Class that manages all the scenario objects"""

    def __init__(self, st_game):
        self.st_game = st_game
        self.screen = st_game.screen
        self.screen_rect = st_game.screen_rect

        # Tilesets
        self.grass_tileset = TileSetReader(self, st_game.ASSETS_DIR / "grass_tileset.png", 32, 32)

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
        for obj in scenario[0]["grass_tileset"]:
            tile = Object(self.st_game, self.grass_tileset[0].get_width(), self.grass_tileset[0].get_height(), obj["position"][0], obj["position"][1], image=self.grass_tileset[obj["tile_id"]])
            self.non_collideable_objects.add(tile)

