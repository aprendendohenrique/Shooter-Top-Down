from argparse import ArgumentError

import pygame

class UIObject:

    def __init__(self, le_editor, x, y, width=0, height=0):
        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect

        self.rect = pygame.Rect(x, y, width, height)

    def center(self):
        try:
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
        else:
            return self

    def center_x(self):
        try:
            fixed_x = ((self.objects[-1].rect.x + self.objects[-1].rect.width) - self.objects[0].rect.x) / 2
            x = 0

            for obj in self.objects:
                obj.rect.x = (self.screen.get_width() / 2) - fixed_x
                obj.rect.x += x

                x += self.spacing
        except AttributeError:
            self.rect.x = (self.screen.get_width() / 2) - self.rect.width / 2
        else:
            return self

    def center_y(self):
        try:
            for obj in self.objects:
                obj.rect.y = (self.screen.get_height() / 2) - obj.rect.height / 2
        except AttributeError:
            self.rect.y = (self.screen.get_height() / 2) - self.rect.height / 2
        else:
            return self

    def down(self):
        try:
            for obj in self.objects:
                obj.rect.y = self.screen.get_height() - obj.rect.height
        except AttributeError:
            self.rect.y = self.screen.get_height() - self.rect.height
        else:
            return self

    def up(self):
        try:
            for obj in self.objects:
                obj.rect.y = 0
        except AttributeError:
            self.rect.y = 0
        else:
            return self

    def left(self):
        try:
            x = 0

            for obj in self.objects:
                obj.rect.x = x
                x += self.spacing
        except AttributeError:
            self.rect.x = 0
        else:
            return self

    def right(self):
        try:
            size = (self.objects[-1].rect.x + self.objects[-1].rect.width) - self.objects[0].rect.x
            x = 0

            for obj in self.objects:
                obj.rect.x = self.screen.get_width() - size + x
                x += self.spacing
        except AttributeError:
            self.rect.x = self.screen.get_width() - self.rect.width
        else:
            return self