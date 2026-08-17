import pygame


class Button:

    def __init__(self, le_editor, x, y, width, height, color=(0, 0, 0), image=None, command=None, id=None):
        """Base class for all buttons"""

        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect
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

    def draw_me(self):
        if self.image:
            self.screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)


class SegmentedButton:

    def __init__(self, le_editor, x, y, spacing, color=(0, 0, 0), images=None):
        """Class that creates many buttons that only one can be selected."""

        self.le_editor = le_editor
        self.screen = le_editor.screen
        self.screen_rect = le_editor.screen_rect

        self.images = images

        self.buttons = []
        self.x = x
        self.width = images[0].get_width()
        self.height = images[0].get_height()

        for count, image in enumerate(self.images):
            button = Button(self.le_editor, self.x, y, self.width, self.height, image=image, id=count)
            self.buttons.append(button)

            self.x += self.width + spacing

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