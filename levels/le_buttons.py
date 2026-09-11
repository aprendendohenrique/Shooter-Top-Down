import pygame
from le_objects import UIObject


class Button(UIObject):

    def __init__(self, le_editor, x, y, width, height, color=(0, 0, 0), image=None, scale=1, command=None, id=None, lock_pos=False):
        """Base class for all buttons"""
        super().__init__(le_editor, x, y, width, height, lock_pos=lock_pos)

        self.command = command
        self.id = id

        self.color = color

        self.image = image
        if scale != 1:
            self.image = pygame.transform.scale_by(self.image, scale)

        self.rect = pygame.Rect(x, y, width, height)

    def clicked(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if callable(self.command):
                self.command()
            return self
        return None

    def draw_me(self, surface=None):
        if surface:
            if self.image:
                surface.blit(self.image, self.rect)
            else:
                pygame.draw.rect(surface, self.color, self.rect)
        else:
            if self.image:
                self.screen.blit(self.image, self.rect)
            else:
                pygame.draw.rect(self.screen, self.color, self.rect)


class SegmentedButton(UIObject):

    def __init__(self, le_editor, x, y, spacing, color=(0, 0, 0), images=None, vertical=False, lock_pos=False):
        """Class that creates many buttons that only one can be selected."""
        super().__init__(le_editor, x, y, lock_pos=lock_pos)

        self.images = images
        self.vertical = vertical

        self.objects = []
        self.x = x
        self.y = y
        self.tile_width = images[0].get_width()
        self.tile_height = images[0].get_height()
        self.spacing = self.tile_width + spacing

        if vertical:
            for count, image in enumerate(self.images):
                button = Button(self.le_editor, x, self.y, self.tile_width, self.tile_height, image=image, id=count)
                self.objects.append(button)

                self.y += self.spacing
        else:
            for count, image in enumerate(self.images):
                button = Button(self.le_editor, self.x, y, self.tile_width, self.tile_height, image=image, id=count)
                self.objects.append(button)

                self.x += self.spacing

    def clicked(self):
        for button in self.objects:
            clk = button.clicked()
            if clk:
                return clk.id
        return None

    def draw_me(self):
        for button in self.objects:
            button.draw_me()
        x = (self.objects[-1].rect.x - self.objects[0].rect.x) / 2