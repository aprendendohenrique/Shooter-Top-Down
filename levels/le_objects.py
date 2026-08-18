import pygame

class UIObject:

    def __init__(self, le_editor, x, y, width=0, height=0):
        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect

        self.rect = pygame.Rect(x, y, width, height)

    def center(self):
        # Trying to do the cetering any object thing
        self.rect.x = self.screen.get_width() / 2
        self.rect.y = self.screen.get_height() / 2