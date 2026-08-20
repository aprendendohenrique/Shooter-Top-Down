import pygame
from le_objects import UIObject


class Button(UIObject):

    def __init__(self, le_editor, x, y, width, height, color=(0, 0, 0), image=None, command=None, id=None):
        """Base class for all buttons"""
        super().__init__(le_editor, x, y, width, height)

        self.command = command
        self.id = id

        self.color = color

        self.image = image

        self.rect = pygame.Rect(x, y, width, height)

    def clicked(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if callable(self.command):
                self.command()
            return self
        return None

    def draw_me(self, surface=None):
        if self.image:
            self.screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)


class SegmentedButton(UIObject):

    def __init__(self, le_editor, x, y, spacing, color=(0, 0, 0), images=None):
        """Class that creates many buttons that only one can be selected."""
        super().__init__(le_editor, x, y)

        self.images = images

        self.buttons = []
        self.x = x
        self.tile_width = images[0].get_width()
        self.tile_height = images[0].get_height()

        for count, image in enumerate(self.images):
            button = Button(self.le_editor, self.x, y, self.tile_width, self.tile_height, image=image, id=count)
            self.buttons.append(button)

            self.x += self.tile_width + spacing

    def clicked(self):
        for button in self.buttons:
            clk = button.clicked()
            if clk:
                print(clk.id)
                return clk.id
        return None

    def draw_me(self):
        for button in self.buttons:
            button.draw_me()
