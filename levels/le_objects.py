from pygame.sprite import Sprite
import pygame

class UIObject(Sprite):

    def __init__(self, le_editor, x=0, y=0, width=0, height=0, color=None, image=None, lock_pos=False, scale=1, srcalpha=255):
        """Dad class used in every UI Object"""

        super().__init__()

        """Base Variables"""

        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect
        self.settings = le_editor.settings

        """Other Variables"""

        self.lock_pos = lock_pos
        self.visible = True
        self.rect = pygame.Rect(x, y, width, height)
        self.srcalpha = srcalpha

        # Makes a surface if only the color was passed
        if color and image is None:
            self.image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
            self.image.fill(color)
            self.image.set_alpha(self.srcalpha)
        else:
            self.image = image

        if self.image:
            if scale != 1:
                self.image = pygame.transform.scale_by(self.image, scale)
            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()

    def draw_me(self):
        if self.visible and self.image:

            # If lock_pos is true the object follow the camera object, if false, it doesn't
            if self.lock_pos:
                self.screen.blit(self.image, self.rect)
            else:
                self.screen.blit(self.image, self.rect.move(-self.le_editor.screen_x, -self.le_editor.screen_y))

    def move_me(self, x ,y):
        try:
            for obj in self.objects:
                obj.rect.x += x
                obj.rect.y += y
        except AttributeError:
            self.rect.x += x
            self.rect.y += y
        finally:
            return(self)

    def center(self):
        try:
            if self.vertical:
                fixed_y = ((self.objects[-1].rect.y + self.objects[-1].rect.height) - self.objects[0].rect.y) / 2
                y = 0

                for obj in self.objects:
                    obj.rect.y = (self.screen.get_height() / 2) - fixed_y
                    obj.rect.y += y
                    obj.rect.x = (self.screen.get_width() / 2) - obj.rect.width / 2

                    y += self.spacing
            else:
                fixed_x = ((self.objects[-1].rect.x + self.objects[-1].rect.width) - self.objects[0].rect.x) / 2
                x = 0

                for obj in self.objects:
                    obj.rect.x = (self.screen.get_width() / 2) - fixed_x
                    obj.rect.x += x
                    obj.rect.y = (self.screen.get_height() / 2) - obj.rect.height / 2

                    x += self.spacing
        except AttributeError:
            self.rect.x = (self.screen.get_width() / 2) - self.rect.width / 2
            self.rect.y = (self.screen.get_height() / 2) - self.rect.height / 2
        finally:
            return self

    def center_x(self):
        try:
            if self.vertical:
                for obj in self.objects:
                    obj.rect.x = (self.screen.get_width() / 2) - obj.rect.width / 2
            else:
                fixed_x = ((self.objects[-1].rect.x + self.objects[-1].rect.width) - self.objects[0].rect.x) / 2
                x = 0

                for obj in self.objects:
                    obj.rect.x = (self.screen.get_width() / 2) - fixed_x
                    obj.rect.x += x

                    x += self.spacing
        except AttributeError:
            self.rect.x = (self.screen.get_width() / 2) - self.rect.width / 2
        finally:
            return self

    def center_y(self):
        try:
            if self.vertical:
                fixed_y = ((self.objects[-1].rect.y + self.objects[-1].rect.height) - self.objects[0].rect.y) / 2
                y = 0

                for obj in self.objects:
                    obj.rect.y = (self.screen.get_height() / 2) - fixed_y
                    obj.rect.y += y

                    y += self.spacing
            else:
                for obj in self.objects:
                    obj.rect.y = (self.screen.get_height() / 2) - obj.rect.height / 2
        except AttributeError:
            self.rect.y = (self.screen.get_height() / 2) - self.rect.height / 2
        finally:
            return self

    def down(self):
        try:
            if self.vertical:
                size = (self.objects[-1].rect.y + self.objects[-1].rect.height) - self.objects[0].rect.y
                y = 0

                for obj in self.objects:
                    obj.rect.y = self.screen.get_height() - size + y
                    y += self.spacing
            else:
                for obj in self.objects:
                    obj.rect.y = self.screen.get_height() - obj.rect.height
        except AttributeError:
            self.rect.y = self.screen.get_height() - self.rect.height
        finally:
            return self

    def up(self):
        try:
            if self.vertical:
                y = 0

                for obj in self.objects:
                    obj.rect.y = y
                    y += self.spacing
            else:
                for obj in self.objects:
                    obj.rect.y = 0
        except AttributeError:
            self.rect.y = 0
        finally:
            return self

    def left(self):
        try:
            if self.vertical:
                for obj in self.objects:
                    obj.rect.x = 0
            else:
                x = 0

                for obj in self.objects:
                    obj.rect.x = x
                    x += self.spacing
        except AttributeError:
            self.rect.x = 0
        finally:
            return self

    def right(self):
        try:
            if self.vertical:
                for obj in self.objects:
                    obj.rect.x = self.screen.get_width() - obj.rect.width
            else:
                size = (self.objects[-1].rect.x + self.objects[-1].rect.width) - self.objects[0].rect.x
                x = 0

                for obj in self.objects:
                    obj.rect.x = self.screen.get_width() - size + x
                    x += self.spacing
        except AttributeError:
            self.rect.x = self.screen.get_width() - self.rect.width
        finally:
            return self
        

class Tile(UIObject):
    
    def __init__(self, le_editor, x, y, image, fill=False, directions=None):
        super().__init__(le_editor, x, y, image=image)

        # If fill is true and the tile is on top of another tile or outside the grid, it destroys itself
        if fill:
            killed = False

            if x < -self.settings.grid_size or y < -self.settings.grid_size or x > self.settings.grid_size + le_editor.screen_rect.width or y > self.settings.grid_size + le_editor.screen_rect.height:
                killed = True
                self.kill()

            for tile in le_editor.tiles:
                if self.rect.colliderect(tile.rect):
                    killed = True
                    self.kill()
                    break

            if not killed:
                if directions is not None:
                    if directions[0] == -1 or directions[0] == 0:
                        if (x - self.settings.TILE_SIZE, y) not in le_editor.fill_visited:
                            le_editor.fill_visited.append((x - self.settings.TILE_SIZE, y))
                            left_tile = Tile(le_editor, x - self.settings.TILE_SIZE, y, image, True, directions=(-1, 0))
                            le_editor.tiles.add(left_tile)
                    if directions[0] == 1 or directions[0] == 0:
                        if (x + self.settings.TILE_SIZE, y) not in le_editor.fill_visited:
                            le_editor.fill_visited.append((x + self.settings.TILE_SIZE, y))
                            right_tile = Tile(le_editor, x + self.settings.TILE_SIZE, y, image, True, directions=(1, 0))
                            le_editor.tiles.add(right_tile)
                    if directions[1] == 1 or directions[1] == 0:
                        if (x , y + self.settings.TILE_SIZE) not in le_editor.fill_visited:
                            le_editor.fill_visited.append((x, y + self.settings.TILE_SIZE))
                            top_tile = Tile(le_editor, x , y + self.settings.TILE_SIZE, image, True, directions=(0, 1))
                            le_editor.tiles.add(top_tile)
                    if directions[1] == -1 or directions[1] == 0:
                        if (x, y - self.settings.TILE_SIZE) not in le_editor.fill_visited:
                            le_editor.fill_visited.append((x, y - self.settings.TILE_SIZE))
                            bottom_tile = Tile(le_editor, x, y - self.settings.TILE_SIZE, image, True, directions=(0, -1))
                            le_editor.tiles.add(bottom_tile)
                else:
                    left_tile = Tile(le_editor, x - self.settings.TILE_SIZE, y, image, True, directions=(-1, 0))
                    right_tile = Tile(le_editor, x + self.settings.TILE_SIZE, y, image, True, directions=(1, 0))
                    top_tile = Tile(le_editor, x, y + self.settings.TILE_SIZE, image, True, directions=(0, 1))
                    bottom_tile = Tile(le_editor, x, y - self.settings.TILE_SIZE, image, True, directions=(0, -1))
                    le_editor.tiles.add(left_tile, right_tile, top_tile, bottom_tile)

    def clicked(self, destroy=False):
        x, y = pygame.mouse.get_pos()
        x, y = x + self.le_editor.screen_x, y + self.le_editor.screen_y
        if self.rect.collidepoint(x, y):
            self.kill()
            return self
        return None


class CameraObject(UIObject):
    
    def __init__(self, le_editor, x, y, width=0, height=0):
        super().__init__(le_editor, x, y, width, height)

    def move_me(self, x, y):
        self.rect.x += x
        self.rect.y += y

        if (self.rect.x + self.rect.width + self.screen_rect.width // 2) > (self.screen_rect.width + self.settings.grid_size):
            self.rect.x = (self.screen_rect.width + self.settings.grid_size) - self.rect.width - self.screen_rect.width // 2
        elif self.rect.x - self.screen_rect.width // 2 < -self.settings.grid_size:
            self.rect.x = -self.settings.grid_size + self.screen_rect.width // 2

        if (self.rect.y + self.rect.height + self.screen_rect.height // 2) > (self.screen_rect.height + self.settings.grid_size):
            self.rect.y = (self.screen_rect.height + self.settings.grid_size) - self.rect.height - self.screen_rect.height // 2
        elif self.rect.y - self.screen_rect.height // 2 < -self.settings.grid_size:
            self.rect.y = -self.settings.grid_size + self.screen_rect.height // 2

        return self