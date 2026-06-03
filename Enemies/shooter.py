import math

import pygame
from numpy.ma.core import angle

from Enemies.enemy import Enemy
from bullet import Bullet


class Shooter(Enemy):
    """Shooter Enemy"""

    def __init__(self, st_game, x, y):
        super().__init__(st_game, x, y)
        self.st_game = st_game
        self.color = (150, 0, 255)
        self.current_color = self.color
        self.health = 3

        self.vision_range = 700
        self.attack_range = 450
        self.current_angle = 0
        self.weapon_rotation_speed = 0.02
        self.weapon_rotation_offset = self.weapon_rotation_speed / 2

        # Weapon variables
        self.last_time_shot = pygame.time.get_ticks()
        self.firerate = 3000
        self.weapon_color = (255, 255, 255)
        self.weapon_width = 55
        self.weapon_height = 12
        self.weapon_distance = 40

        self.gun_surface = pygame.Surface((self.weapon_width, self.weapon_height), pygame.SRCALPHA)

    def update(self):

        distance_x = self.player.rect.centerx - self.rect.centerx
        distance_y = self.player.rect.centery - self.rect.centery

        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance < self.vision_range + self.player.rect.width:

            # weapon
            self.angle = math.atan2(distance_y, distance_x)

            if (self.current_angle == 0 or
                    self.angle - self.weapon_rotation_offset < self.current_angle < self.angle + self.weapon_rotation_offset):
                self.current_angle = self.angle
            elif self.current_angle < self.angle:
                self.current_angle += self.weapon_rotation_speed
            elif self.current_angle > self.angle:
                self.current_angle -= self.weapon_rotation_speed

            weapon_x = self.rect.centerx + math.cos(self.current_angle) * self.weapon_distance
            weapon_y = self.rect.centery + math.sin(self.current_angle) * self.weapon_distance

            current_angle = math.degrees(self.current_angle)

            self.rotated_surface = pygame.transform.rotate(self.gun_surface, -current_angle)
            self.rotated_rect = self.rotated_surface.get_rect(center=(weapon_x, weapon_y))

            if distance < self.attack_range + self.player.rect.width:
                if pygame.time.get_ticks() - self.last_time_shot >= self.firerate:
                    bullet = Bullet(self.st_game, self, self.current_angle, self.damage, 7,"red")
                    self.st_game.bullets.add(bullet)
                    self.last_time_shot = pygame.time.get_ticks()
            else:
                self.last_time_shot = pygame.time.get_ticks()

                # movement
                if not self.rect.colliderect(self.player.rect):
                    self.x_rect += math.cos(self.angle) * self.speed
                    self.y_rect += math.sin(self.angle) * self.speed
                elif pygame.time.get_ticks() - self.last_hit >= self.enemy_attack_speed:
                    self.last_hit = pygame.time.get_ticks()
                    self.player.get_hit(self.damage)

                self.rect.x = self.x_rect
                self.rect.y = self.y_rect


        if self.got_hit and pygame.time.get_ticks() - self.got_hit_time >= self.hit_animation_time:
            self.got_hit = False
            self.current_color = self.color

    def drawme(self):
        pygame.draw.rect(self.screen, self.current_color, self.rect)
        pygame.draw.rect(self.gun_surface, self.weapon_color, (0, 0, self.weapon_width, self.weapon_height))
        self.screen.blit(self.rotated_surface, self.rotated_rect)
