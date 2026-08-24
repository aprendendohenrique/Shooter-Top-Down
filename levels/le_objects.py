import pygame

class UIObject:

    def __init__(self, le_editor, x, y, width=0, height=0):
        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect

        self.rect = pygame.Rect(x, y, width, height)

    def center(self):
        self.rect.x = (self.screen.get_width() / 2) - self.rect.width / 2
        self.rect.y = (self.screen.get_height() / 2) - self.rect.height / 2
        return self

    def down(self):
        self.rect.y = self.screen.get_height() - self.rect.height
        return self

    def up(self):
        self.rect.y = 0
        return self

    def left(self):
        self.rect.x = 0
        return self

    def right(self):
        self.rect.x = self.screen.get_width()
        return self