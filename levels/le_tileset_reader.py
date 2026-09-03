import pygame


class TileSetReader:

    def __new__(cls, le_editor, tileset, x_tile_size, y_tile_size):
        image = pygame.image.load(tileset).convert()

        if image.get_width() % x_tile_size == 0 and image.get_height() % y_tile_size == 0:
            tiles = []
            tiles_count = int(image.get_width() / x_tile_size)

            for count in range(tiles_count):
                tile = image.subsurface(x_tile_size * count, y_tile_size * count, x_tile_size, y_tile_size).convert()
                tiles.append(tile)

            return tiles

        raise TypeError

