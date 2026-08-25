import pygame

class UIObject:

    def __init__(self, le_editor, x, y, width=0, height=0):
        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect

        self.rect = pygame.Rect(x, y, width, height)

    def center(self):
        try:
            ...
            # make the centering
            x = (self.objects[-1].rect.x - self.objects[0].rect.x) / 2
            print(x)

            for obj in self.objects:
                obj.rect.x = (self.screen.get_width() / 2) - x
                obj.rect.y = (self.screen.get_height() / 2) - obj.rect.height / 2
                x -= self.spacing
                print(x)
        except AttributeError:
            self.rect.x = (self.screen.get_width() / 2) - self.rect.width / 2
            self.rect.y = (self.screen.get_height() / 2) - self.rect.height / 2
        else:
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