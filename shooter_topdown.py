import sys

import pygame

from settings import Settings
from player import Player
from weapon import Weapon
from bullet import Bullet


class ShooterTopdown:
    """The main class that control and run the game"""

    def __init__(self):
        pygame.init()

        # Main variables
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.settings.screen_resolution)
        self.screen_rect = self.screen.get_rect()

        # Objects
        self.player = Player(self)
        self.weapon = Weapon(self, self.player)
        self.bullets = pygame.sprite.Group()

        # Font the mouse position text
        self.font = pygame.font.SysFont(None, 48)

    def run_game(self):
        while True:
            # Check key events
            self._check_events()

            # Player update
            self.player.update()
            self.weapon.update()
            self.bullets.update()

            # Text of the mouse position
            self.text_surface = self.font.render(f"{pygame.mouse.get_pos()}", True, "white")

            # Update everything to the screen
            self._update_screen()

            # FPS
            self.clock.tick(60)

    def _update_screen(self):
        # Background color
        self.screen.fill(self.settings.background_color)

        # Player and weapon on the screen
        self.player.drawme()
        self.weapon.drawme()
        for bullet in self.bullets:
            bullet.drawme()

        # Text of the mouse position
        self.screen.blit(self.text_surface, (0, 465))

        # Flips/Update de screen
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._key_down_event(event)
            elif event.type == pygame.KEYUP:
                self._key_up_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(self)
                self.bullets.add(bullet)

    def _key_down_event(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_s:
            self.player.moving_down = True
        elif event.key == pygame.K_w:
            self.player.moving_up = True
        elif event.key == pygame.K_d:
            self.player.moving_right = True
        elif event.key == pygame.K_a:
            self.player.moving_left = True

    def _key_up_event(self, event):
        if event.key == pygame.K_s:
            self.player.moving_down = False
        elif event.key == pygame.K_w:
            self.player.moving_up = False
        elif event.key == pygame.K_d:
            self.player.moving_right = False
        elif event.key == pygame.K_a:
            self.player.moving_left = False

st_game = ShooterTopdown()
st_game.run_game()