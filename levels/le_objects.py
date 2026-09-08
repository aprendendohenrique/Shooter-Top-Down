from pygame.sprite import Sprite
import pygame

class UIObject(Sprite):

    def __init__(self, le_editor, x, y, width=0, height=0, color=None, image=None, lock_pos=False):
        super().__init__()
        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect

        self.lock_pos = lock_pos
        self.color = color
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)

        if self.image:
            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()

    def draw_me(self):
        if self.image:
            if self.lock_pos:
                self.screen.blit(self.image, self.rect)
            else:
                self.screen.blit(self.image, self.rect.move(-self.le_editor.screen_x, -self.le_editor.screen_y))
        elif self.color:
            if self.lock_pos:
                pygame.draw.rect(self.screen, self.color, self.rect)
            else:
                pygame.draw.rect(self.screen, self.color,
                                 self.rect.move(-self.le_editor.screen_x, -self.le_editor.screen_y))

    def move_me(self, x ,y):
        self.rect.x += x
        self.rect.y += y
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
    
    def __init__(self, le_editor, x, y, image):
        super().__init__(le_editor, x, y)
        self.le_editor = le_editor
        self.image = image
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()

    def draw_me(self):
        self.screen.blit(self.image, self.rect.move(-self.le_editor.screen_x, -self.le_editor.screen_y))

    def clicked(self, destroy=False):
        x, y = pygame.mouse.get_pos()
        x, y = x + self.le_editor.screen_x, y + self.le_editor.screen_y
        if self.rect.collidepoint(x, y):
            self.kill()