import sys
import random

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

        # Game Over
        self.is_game_over = True
        self.game_over_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.game_over_surface.fill("white")
        self.game_over_surface.set_alpha(150)
        self.play_button_surface = pygame.Surface((200, 50))
        self.play_button_surface.fill((10, 80, 0))
        self.play_button_rect = self.play_button_surface.get_rect()
        self.play_button_rect.center = self.game_over_surface.get_rect().center
        self.play_font = pygame.font.SysFont(None, 48)
        self.play_text = self.play_font.render("Play", True, "white")
        self.play_text_rect = self.play_text.get_rect()
        self.play_text_rect.center = self.play_button_rect.center

        # Objects
        self.player = Player(self)
        self.weapon = Weapon(self, self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Shoot
        self.last_time_shot = pygame.time.get_ticks()
        self.is_shooting = False

        # Font of the mouse position
        self.font = pygame.font.SysFont(None, 48)

        # Spawn System
        self.enemies_to_spawn = 1
        self.max_enemies = 8
        self.enemies_spawned = 0
        self.x_spawn_positions = [0, self.screen_rect.width]
        self.enemies_classes = [Walker, Runner, Shooter]
        self._spawn()



    def run_game(self):
        while True:
            # Check key events
            self._check_events()

            if not self.is_game_over:

                # Objects
                self.player.update()
                self.weapon.update()
                self.bullets.update()
                self.enemies.update()

                # Run the player's shooting
                self._shoot()

                # Mouse position Text
                self.text_surface = self.font.render(f"{pygame.mouse.get_pos()}", True, "white")

            # Update the screen
            self._update_screen()

            # FPS
            self.clock.tick(60)

    def _update_screen(self):
        # Background color
        self.screen.fill(self.settings.background_color)

        if not self.is_game_over:
            # Objects
            self.player.drawme()
            self.weapon.drawme()
            for bullet in self.bullets:
                bullet.drawme()
            for enemy in self.enemies:
                enemy.drawme()

            # Text of the mouse position
            self.screen.blit(self.text_surface, (0, 465))
        else:
            # Game Over Screen
            self.screen.blit(self.game_over_surface, (0, 0))
            self.screen.blit(self.play_button_surface, self.play_button_rect)
            self.screen.blit(self.play_text, self.play_text_rect)

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
                self.weapon.is_shooting = True

                # Game Over
                if self.is_game_over and self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.is_game_over = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.weapon.is_shooting = False

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
        elif event.key == pygame.K_SPACE:
            self.player.dashing = True

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
        # Checking collisions between bullets and enemys
        enemy_collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, False, False, pygame.sprite.collide_circle)
        for bullet, enemies_hit in enemy_collisions.items():
            if bullet.is_player:
                bullet.kill()
                for enemy in enemies_hit:
                    enemy.get_hit(bullet.bullet_damage)
                    if enemy.health <= 0:
                        enemy.kill()
                        self.enemies_spawned -= 1
                        if self.enemies_spawned <= 0:
                            self._spawn()
        player_collisions = pygame.sprite.spritecollide(self.player, self.bullets, False)
        for bullet in player_collisions:
            if not bullet.is_player:
                bullet.kill()
                self.player.get_hit(bullet.bullet_damage)

    def _spawn(self):
        for _ in range(self.enemies_to_spawn):
            enemy_class = random.choice(self.enemies_classes)
            enemy = enemy_class(self)
            x = random.choice(self.x_spawn_positions)
            y = random.randint(0, self.screen_rect.height)
            enemy.reposition_me((x, y))
            self.enemies.add(enemy)
        self.enemies_spawned = len(self.enemies)
        if self.enemies_to_spawn < self.max_enemies:
            self.enemies_to_spawn += 1

    def game_over(self):
        self.is_game_over = True
        self.enemies.empty()
        self.bullets.empty()
        self.settings.player_health = self.settings.player_max_health
        self.player.reposition_me(self.screen_rect.center)
        self.enemies_to_spawn = 1
        self.enemies_spawned = 0
        self._spawn()



st_game = ShooterTopdown()
st_game.run_game()