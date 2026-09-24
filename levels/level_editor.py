import json
import sys
from pathlib import Path

import pygame

from le_file_utils import FileUtils
from le_settings import LESettings
from le_buttons import Button
from le_buttons import SegmentedButton
from le_tileset_reader import TileSetReader
from le_objects import Tile
from le_objects import CameraObject
from levels.le_objects import UIObject


class LevelEditor:

    def __init__(self):
        pygame.init()

        """Base Variables"""

        self.settings = LESettings()
        self.screen = pygame.display.set_mode(self.settings.screen_resolution)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        # Directors
        self.BASE_DIR = Path(__file__).resolve().parent
        self.TILESETS_DIR = self.BASE_DIR / "images" / "tilesets"
        self.UI_DIR = self.BASE_DIR / "images" / "UI"

        """Other Variables"""

        # Tile/Tileset
        self.tilesets = {}
        self.current_tileset = None

        self.tiles = pygame.sprite.Group()

        # Selected tile on the segmented button
        self.tile = None

        # Tile id of the selected tile
        self.tile_id = None

        self.show_grid = True

        self.left_mouse_button_down = False
        self.right_mouse_button_down = False

        """Camera"""

        self.camera_object = CameraObject(self, 0, 0, 32, 32).center()
        self.last_mouse_position = [0, 0]
        self.screen_x = 0
        self.screen_y = 0

        """UI Objects"""

        # Group that has the seg and arrow buttons
        self.seg_group_buttons = pygame.sprite.Group()

        # Arrows
        left_arrow_image = pygame.image.load(self.UI_DIR / "left_arrow.png")
        self.left_arrow_button = Button(self, 0, 0, 16, 16, image=left_arrow_image, scale=2, command=lambda: self.change_tileset(-1), lock_pos=True)
        self.left_arrow_button.center_y().move_me(-2, -140)

        right_arrow_image = pygame.image.load(self.UI_DIR / "right_arrow.png")
        self.right_arrow_button = Button(self, 0, 0, 16, 16, image=right_arrow_image, scale=2, command=lambda: self.change_tileset(1), lock_pos=True)
        self.right_arrow_button.center_y().move_me(52, -140)

        self.seg_group_buttons.add(self.left_arrow_button)
        self.seg_group_buttons.add(self.right_arrow_button)

        load_tileset_btn_image = pygame.image.load(self.UI_DIR / "clipboard.png")
        self.load_tileset_button = Button(self, 25, 25, 64, 64, scale=0.7, command=self.load_tileset, image=load_tileset_btn_image, lock_pos=True)

        save_map_btn_image = pygame.image.load(self.UI_DIR / "save.png")
        self.save_map_button = Button(self, 70, 22, 64, 64, scale=0.8, command=self.save_map, image=save_map_btn_image, lock_pos=True)

        # Segmented button, is where you choose which tile to paint
        self.seg_button = None

        self.seg_button_x = 25
        self.seg_button_y = 40

        # Tile covers, covers that show when the collision is On/Off
        self.seg_button_covers = pygame.sprite.Group()

        self.tile_collision_covers = pygame.sprite.Group()

        # Big Screen Covers
        big_covers_color = (220, 220, 220)
        self.upper_cover = UIObject(self, 0, 0, self.screen.get_width(), 100, color=big_covers_color, lock_pos=True)
        self.left_cover = UIObject(self, 0, 0, 100, self.screen.get_height(), color=big_covers_color, lock_pos=True)

        """Save"""

        self.current_save = {}
        self.load_map()

    def run(self):
        """The main loop that runs the Level Editor"""

        while True:
            # Check for mouse/keyboard events
            self.check_events()
            self._mouse_events()

            self._camera()

            self._update_screen()

            self.clock.tick(self.settings.fps)

    def _update_screen(self):
        """Updates everything to the screen"""

        # Fill the screen with a color "background"
        self.screen.fill(self.settings.background_color)

        # If grid is on, show it
        if self.show_grid:
            self.draw_lines()

        """UI Objects"""

        # Draw all the painted tiles and it's covers
        for tile in self.tiles:
            tile.draw_me()

        for tile_coll_cover in self.tile_collision_covers:
            tile_coll_cover.draw_me()

        # Big Screen Covers
        self.upper_cover.draw_me()
        self.left_cover.draw_me()

        # Buttons
        if self.seg_button:
            for button in self.seg_group_buttons:
                button.draw_me()

        for seg_btn_cover in self.seg_button_covers:
            seg_btn_cover.draw_me()

        self.load_tileset_button.draw_me()
        self.save_map_button.draw_me()

        # Lines that shows the middle of the screen
        horizontal = pygame.draw.line(self.screen, "red", (self.screen.get_width()/2, 0), (self.screen.get_width()/2, self.screen.get_height()))
        vertical = pygame.draw.line(self.screen, "red", (0, self.screen.get_height()/2), (self.screen.get_width(), self.screen.get_height()/2))

        # Update the screen
        pygame.display.flip()

    def _camera(self):
        """Update the values that makes the camera follow the player"""

        self.screen_x = (self.camera_object.rect.x + self.camera_object.rect.width / 2) - self.screen_rect.width // 2
        self.screen_y = (self.camera_object.rect.y + self.camera_object.rect.height / 2) - self.screen_rect.height // 2

    def check_events(self):
        """Handles every event"""

        # Gets every event
        for event in pygame.event.get():

            # Closing the game
            if event.type == pygame.QUIT:
                sys.exit()

            # Keydown events
            elif event.type == pygame.KEYDOWN:
                self._key_down_events(event)

            # Mouse button down events
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Left mouse button down
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.left_mouse_button_down = True
                    self._left_mouse_down_events()

                # Right mouse button down
                elif pygame.mouse.get_pressed(num_buttons=3)[2]:
                    self.right_mouse_button_down = True
                    self._right_mouse_down_events()

            # Mouse button up events
            elif event.type == pygame.MOUSEBUTTONUP:

                # Left mouse button up
                if not pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.left_mouse_button_down = False

                # Right mouse button down
                if not pygame.mouse.get_pressed(num_buttons=3)[2]:
                    self.right_mouse_button_down = False
                    self._right_mouse_up_events()

    def _key_down_events(self, event):
        """Handles every KeyBoard Down events"""

        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_g:
            if self.show_grid:
                self.show_grid = False
            else:
                self.show_grid = True

    def save_map(self):
        """Simple save function"""

        save_path = FileUtils.save_json()
        try:
            with open(save_path, "w") as file:
                json.dump(self.current_save, file, indent=4)
            with open(self.BASE_DIR / "last_save.json", "w") as file:
                file.write(str(save_path))
        except PermissionError:
            pass

    def _mouse_events(self):
        """Every mouse event, that can be clicked and hold"""

        # Get mouse position
        x, y = pygame.mouse.get_pos()

        # Right mouse button down
        if self.right_mouse_button_down:

            # Change the cursor to the hand
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

            # Distance that the mouse traveled
            distance_x = self.last_mouse_position[0] - x
            distance_y = self.last_mouse_position[1] - y

            # Moves the camera object using that distance
            self.camera_object.move_me(distance_x, distance_y)

        # Right mouse button down
        elif self.left_mouse_button_down:

            # Grid clicked
            self._grid_clicked(x + self.screen_x, y + self.screen_y, x, y)

        self.last_mouse_position = [x, y]

    def _left_mouse_down_events(self):
        """Handles only click events"""

        # Buttons
        if self.seg_button:
            self.left_arrow_button.clicked()
            self.right_arrow_button.clicked()

        self.load_tileset_button.clicked()

        self.save_map_button.clicked()

        self._asset_clicked()

    def _right_mouse_down_events(self):
        """Handles only click events"""

        # If any of the segmented button was clicked, receive its id
        if self.seg_button:
            button_id = self.seg_button.clicked()
        else:
            button_id = None

        # Check if any segmented button was clicked
        if button_id != None:

            # If collidable is on, make it false and hide cover
            if self.tilesets[self.current_tileset][button_id]["collidable"]:
                self.tilesets[self.current_tileset][button_id]["collidable"] = False
                self.seg_button_covers.sprites()[button_id].visible = False

            # If collidable is off, make it true and show cover
            else:
                self.tilesets[self.current_tileset][button_id]["collidable"] = True
                self.seg_button_covers.sprites()[button_id].visible = True
            print(self.tilesets[self.current_tileset][button_id]["collidable"])

    def _right_mouse_up_events(self):
        """Handles every right mouse button up event"""

        # Sets the mouse cursor back to normal
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

    def _grid_clicked(self, x, y, fixed_x, fixed_y):
        """Handles what happens if the grid is clicked"""

        # Check if the mouse is not on the covers
        if not self.left_cover.rect.collidepoint(fixed_x, fixed_y) and not self.upper_cover.rect.collidepoint(fixed_x, fixed_y):

            # Check if you're clicking on the grid, by comparing the mouse position with its size
            if (x > -self.settings.grid_size and y > -self.settings.grid_size) and (x < self.screen_rect.width + self.settings.grid_size and y < self.screen_rect.height + self.settings.grid_size):

                # Gets the position of the clicked grid
                x_grid = x // 32
                y_grid = y // 32

                print(f"x: {x_grid + 1} y: {y_grid + 1}")

                # Check if any tile on the segmented button was selected
                if self.tile is not None:

                    # Replaces the tile and its cover, if there was already one on the place
                    if self.tiles:
                        for tile in self.tiles:
                            if tile.clicked(destroy=True):
                                for tileset in self.tilesets:
                                    self.current_save[tileset] = [d for d in self.current_save[tileset] if d.get("position") != [x_grid * self.settings.TILE_SIZE, y_grid * self.settings.TILE_SIZE]]

                                # Destroy the cover on top of the tile
                                for cover in self.tile_collision_covers:
                                    if cover.rect.collidepoint(x, y):
                                        cover.kill()

                        # Delete cover on top of the tile
                        for cover in self.tile_collision_covers:
                            if cover.rect.collidepoint(x, y):
                                cover.kill()

                    # Creates the new tile
                    tile = Tile(self, x_grid * self.settings.TILE_SIZE, y_grid * self.settings.TILE_SIZE, self.tile)
                    self.tiles.add(tile)

                    # Save it
                    self.current_save[self.current_tileset].append({"tile_id": self.tile_id, "position": [tile.rect.x, tile.rect.y], "collidable": self.tilesets[self.current_tileset][self.tile_id]["collidable"]})

                    # Place the cover on top of collidable tiles
                    if self.tilesets[self.current_tileset][self.tile_id]["collidable"]:
                        cover = UIObject(self, tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height, color="green", srcalpha=50)
                        self.tile_collision_covers.add(cover)

                # If a tile to pain was not selected
                else:

                    # Destroy the clicked tiles on grid
                    for tile in self.tiles:
                        if tile.clicked(destroy=True):
                            for tileset in self.tilesets:
                                self.current_save[tileset] = [d for d in self.current_save[tileset] if d.get("position") != [x_grid * self.settings.TILE_SIZE, y_grid * self.settings.TILE_SIZE]]

                        # Destroy the cover on top of the tile
                        for cover in self.tile_collision_covers:
                            if cover.rect.collidepoint(x, y):
                                cover.kill()

    def _asset_clicked(self):
        """Handles the choosing a tile from the segmented button"""

        # Checks if any button of the segmented button was clicked, and get its id
        if self.seg_button:
            button_id = self.seg_button.clicked()
        else:
            button_id = None

        # Checks if any button was of the segmented was clicked
        if button_id is not None:

            # If the clicked tile is not the same from before
            if self.tile != self.seg_button.images[button_id]:

                # Sets the tile to the clicked tile and its id too
                self.tile = self.seg_button.images[button_id]
                self.tile_id = button_id

            # If it is the same from before
            else:

                # Sets tile to None
                self.tile = None

    def draw_lines(self):
        """Draw the grid lines"""

        width = self.screen.get_width()
        height = self.screen.get_height()

        for x in range(0 - self.settings.grid_size, width + self.settings.grid_size, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(x - self.screen_x, -self.settings.grid_size - self.screen_y), end_pos=(x - self.screen_x, height + self.settings.grid_size - self.screen_y), width=self.settings.grid_width)

        for y in range(0 - self.settings.grid_size, height + self.settings.grid_size, self.settings.TILE_SIZE):
            pygame.draw.line(self.screen, "black", start_pos=(-self.settings.grid_size - self.screen_x, y - self.screen_y), end_pos=(width + self.settings.grid_size - self.screen_x, y - self.screen_y), width=self.settings.grid_width)

    def change_tileset(self, direction=0):
        """Handles the tileset changing, when clicking the arrows"""

        # Get the tileset keys and store it
        tilesets = []

        for tileset in self.tilesets.keys():
            tilesets.append(tileset)

        # Try to change the tileset, if it goes wrong, make it go back to the starter one
        if isinstance(direction, Path):
            self.current_tileset = str(direction)
            try:
                self.current_save[self.current_tileset]
            except Exception as ex:
                self.current_save[self.current_tileset] = []
                print(ex)
        else:
            try:
                self.current_tileset = tilesets[tilesets.index(self.current_tileset) + direction]
            except IndexError:
                self.current_tileset = tilesets[0]

        # Destroy the old segmented button, and creates a new one on top of it
        if self.seg_button:
            self.seg_button.kill()

        seg_btn_images = [sprite["surface"] for sprite in self.tilesets[self.current_tileset]]

        self.seg_button = SegmentedButton(self, self.seg_button_x, 0, 5, images=seg_btn_images, vertical=True,
                                          lock_pos=True)
        self.seg_button.center_y().move_me(0, self.seg_button_y)

        self.seg_group_buttons.add(self.seg_button)

        # Make the covers if there wasn't one
        if not self.seg_button_covers:
            for button in self.seg_button.objects:
                cover = UIObject(self, button.rect.x, button.rect.y, button.rect.width, button.rect.height,
                                 color="green", lock_pos=True, srcalpha=50)
                cover.visible = False
                self.seg_button_covers.add(cover)
        else:
            # If there was, it "loads" from the tileset which ones were on
            for cover in self.seg_button_covers:
                cover.visible = False
            for count, tile in enumerate(self.tilesets[self.current_tileset]):
                if tile["collidable"]:
                    self.seg_button_covers.sprites()[count].visible = True

    def load_tileset(self, path=None):
        """Opens a window for the user to choose the tileset set, and change it"""

        # Opens the window to choose the tileset
        if path is None:
            tileset_path = FileUtils.choose_image()
        else:
            tileset_path = Path(path)

        # If there's a path...
        if tileset_path.name != "":

            # Gets its tiles
            self.tilesets[str(tileset_path)] = TileSetReader(self, tileset_path, 32, 32)

            # Change the seg_button to the new Tileset
            self.change_tileset(tileset_path)

    def load_map(self):
        with open(self.BASE_DIR / "last_save.json", "r") as file:
            path = file.readline()

            if path:
                with open(path, "r") as save_file:
                    self.current_save = json.load(save_file)

                    # Load Tileset
                    for tileset in self.current_save.keys():
                        self.load_tileset(tileset)

                        # Load Tiles
                        for tile in self.current_save[tileset]:
                            t = Tile(self, tile["position"][0], tile["position"][1],
                                     self.tilesets[tileset][tile["tile_id"]]["surface"])
                            self.tiles.add(t)

                            # Place cover on top, if tile is collidable
                            if tile["collidable"]:
                                cover = UIObject(self, t.rect.x, t.rect.y, t.rect.width, t.rect.height,
                                                 color="green", srcalpha=50)
                                self.tile_collision_covers.add(cover)


if __name__ == '__main__':
    le = LevelEditor()
    le.run()
