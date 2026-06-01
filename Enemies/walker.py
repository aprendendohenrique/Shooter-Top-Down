import math

import pygame

from Enemies.enemy import Enemy


class Walker(Enemy):
    """The first enemy"""

    def __init__(self, st_game, x, y):
        super().__init__(st_game, x, y)

    def update(self):

        distance_x = self.player.rect.centerx - self.rect.centerx
        distance_y = self.player.rect.centery - self.rect.centery

        angle = math.atan2(distance_y, distance_x)

        if not self.rect.colliderect(self.player.rect):
            self.x_rect += math.cos(angle) * self.speed
            self.y_rect += math.sin(angle) * self.speed
        elif pygame.time.get_ticks() - self.last_hit >= self.enemy_attack_speed:
            self.last_hit = pygame.time.get_ticks()
            self.player.get_hit(self.damage)

        self.rect.x = self.x_rect
        self.rect.y = self.y_rect

        if self.got_hit and pygame.time.get_ticks() - self.got_hit_time >= self.hit_animation_time:
            self.got_hit = False
            self.current_color = self.color