import pygame


class TileSetReader:

    def __new__(cls, le_editor, tileset, x_tile_size, y_tile_size):
        """Reads the image and returns a list with each tile"""

        # Load the image from the path and convert it
        image = pygame.image.load(tileset).convert()

        # Checks if its possible to separate the image in tiles with the given size
        if image.get_width() % x_tile_size == 0 and image.get_height() % y_tile_size == 0:
            tiles = []

            # Get the number of tiles the image has
            tiles_count = int(image.get_width() / x_tile_size)

            # Get each tile and add it to the list
            for count in range(tiles_count):
                tile = image.subsurface(x_tile_size * count, y_tile_size * count, x_tile_size, y_tile_size).convert()
                tiles.append({"surface": tile, "collidable": False})

            return tiles

        # Raise an error if the given size is wrong
        raise TypeError

class TileSetsReader:

    def __new__(cls, le_editor, dir_path, x_tile_size, y_tile_size):
        """Reads a directory with images/tilesets and return each tileset with its tiles"""

        tilesets = {}

        # Get each tileset path
        for tileset in dir_path.iterdir():
            tilesets[tileset.name] = TileSetReader(le_editor, tileset, x_tile_size, y_tile_size)

        return tilesets
