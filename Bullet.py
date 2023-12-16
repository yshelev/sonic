import random

import pygame

from Settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, finish_x, finish_y, image, type, *sprite_group, **kwargs):
        super().__init__(*sprite_group)
        self.additional_speed = 600 * type
        self.start_x = x
        self.start_y = y
        self.width, self.height = 30, 30
        self.finish_x = finish_x
        self.finish_y = finish_y
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed_x = (self.finish_x - self.start_x) // 100
        self.speed_y = (self.finish_y - self.start_y) // 100
        print(self.speed_y, self.speed_x)

    def move_self(self):
        self.speed_x += self.additional_speed / FPS if self.speed_x > 0 else -self.additional_speed / FPS if self.speed_x < 0 else 0
        self.speed_y += self.additional_speed / FPS if self.speed_y > 0 else -self.additional_speed / FPS if self.speed_y < 0 else 0

        self.x += self.speed_x / FPS
        self.y += self.speed_y / FPS
        if not(0 <= self.x <= SCREEN_WIDTH and 0 <= self.y <= SCREEN_HEIGHT) or (self.speed_x == 0 and self.speed_y == 0):
            self.kill()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, *args, **kwargs):
        self.move_self()



