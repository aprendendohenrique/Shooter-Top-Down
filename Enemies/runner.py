import math

import pygame

from Enemies.enemy import Enemy


class Runner(Enemy):
    """The Second Enemy, Runner"""

    def __init__(self, st_game):
        """Start all the needed variables"""

        super().__init__(st_game)

        # Enemy
        self.color = (255, 0, 255)
        self.current_color = self.color
        self.speed = 4
        self.health = 2

    def update(self):
        """Update the enemy every tick"""
        # Make the enemy move
        distance_x = self.player.rect.centerx - self.rect.centerx
        distance_y = self.player.rect.centery - self.rect.centery

        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance < self.vision_range + self.player.rect.width:
            angle = math.atan2(distance_y, distance_x)

            if not self.rect.colliderect(self.player.rect):
                self.x_rect += math.cos(angle) * self.speed
                self.y_rect += math.sin(angle) * self.speed
            elif pygame.time.get_ticks() - self.last_hit >= self.enemy_attack_speed:
                self.last_hit = pygame.time.get_ticks()
                self.player.get_hit(self.damage)

            self.rect.x = self.x_rect
            self.rect.y = self.y_rect

        # Hit
        if self.got_hit and pygame.time.get_ticks() - self.got_hit_time >= self.hit_animation_time:
            self.got_hit = False
            self.current_color = self.color