import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """Main class that manages the simple enemy."""
    
    def __init__(self, st_game, x, y):
        super().__init__()
        self.screen = st_game.screen
        self.player = st_game.player

        self.color = (255, 0, 0)
        self.health = 4
        self.damage = 1
        self.speed = 2
        self.vision_range = 500

        # 1000 = 1 second
        self.enemy_attack_speed = 1000
        self.last_hit = pygame.time.get_ticks()

        # Hit animation stuff
        self.hit_color = (255, 255, 255)
        self.current_color = self.color
        self.got_hit = False
        self.got_hit_time = pygame.time.get_ticks()
        self.hit_animation_time = 100

        self.rect = pygame.Rect(x, y, 50, 50)

        self.x_rect = float(self.rect.x)
        self.y_rect = float(self.rect.y)

    def drawme(self):
        pygame.draw.rect(self.screen, self.current_color, self.rect)

    def get_hit(self, damage):
        self.health -= damage
        self.current_color = self.hit_color
        self.got_hit = True
        self.got_hit_time = pygame.time.get_ticks()