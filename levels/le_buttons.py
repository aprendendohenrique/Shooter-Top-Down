import pygame


class Button:

    def __init__(self, le_editor, x, y, width, height, color=(0, 0, 0), image=None, command=None):
        """Base class for all buttons"""

        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect
        self.command = command

        self.color = color

        self.image = image

        self.rect = pygame.Rect(x, y, width, height)

    def clicked(self):
        if callable(self.command):
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                self.command()

    def draw_me(self):
        if self.image:
            self.screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)


class SegmentedButton:

    def __init__(self):
        """Class that creates many buttons that only one can be selected."""
        ...