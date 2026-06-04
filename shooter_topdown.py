import sys

import pygame

from settings import Settings
from player import Player
from weapon import Weapon
from bullet import Bullet
from Enemies.walker import Walker
from Enemies.runner import Runner
from Enemies.shooter import Shooter


class ShooterTopdown:
    """The main class that control and run the game"""

    def __init__(self):
        """Start the game's variables"""

        pygame.init()

        # Base
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.settings.screen_resolution)
        self.screen_rect = self.screen.get_rect()

        # Objects
        self.player = Player(self)
        self.weapon = Weapon(self, self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # walker = Walker(self, 50, 150)
        # runner = Runner(self, 840, 150)
        shooter = Shooter(self, 0, self.screen_rect.centery)
        # self.enemies.add(walker)
        # self.enemies.add(runner)
        self.enemies.add(shooter)

        # Shoot
        self.last_time_shot = pygame.time.get_ticks()
        self.is_shooting = False

        # Font of the mouse position
        self.font = pygame.font.SysFont(None, 48)

    def run_game(self):
        while True:
            # Check key events
            self._check_events()

            # Run the player's shooting
            self._shoot()

            # Objects
            self.player.update()
            self.weapon.update()
            self.bullets.update()
            self.enemies.update()

            # Text of the mouse position
            self.text_surface = self.font.render(f"{pygame.mouse.get_pos()}", True, "white")

            # Update the screen
            self._update_screen()

            # FPS
            self.clock.tick(60)

    def _update_screen(self):
        # Background color
        self.screen.fill(self.settings.background_color)

        # Objects
        self.player.drawme()
        self.weapon.drawme()
        for bullet in self.bullets:
            bullet.drawme()
        for enemy in self.enemies:
            enemy.drawme()

        # Text of the mouse position
        self.screen.blit(self.text_surface, (0, 465))

        # Flips/Update the screen
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
                self.is_shooting = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.is_shooting = False

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

    def _shoot(self):
        if self.is_shooting:
            if pygame.time.get_ticks() - self.last_time_shot  >= self.settings.firerate:
                bullet = Bullet(self, self.player, self.weapon.angle, self.settings.player_damage)
                self.bullets.add(bullet)
                self.last_time_shot = pygame.time.get_ticks()

        # Checking collisions between bullets and enemys
        enemy_collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False, pygame.sprite.collide_circle)
        for bullet, enemies_hit in enemy_collisions.items():
            for enemy in enemies_hit:
                enemy.get_hit(bullet.bullet_damage)
                if enemy.health <= 0:
                    enemy.kill()
        player_collisions = pygame.sprite.spritecollide(self.player, self.bullets, True)
        for bullet in player_collisions:
            self.player.get_hit(bullet.bullet_damage)

st_game = ShooterTopdown()
st_game.run_game()