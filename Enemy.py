import random

import pygame

from Character import Character
from MainHero import MainHero
from Settings import *


class Enemy(Character):
    def __init__(
            self,
            x: int,
            y: int,
            start_image: pygame.image,
            images: list[pygame.image],
            jump_images: list[pygame.image],
            *sprite_group: pygame.sprite.Group
    ) -> None:
        super().__init__(x, y, start_image, images, jump_images, *sprite_group)
        self.movement_cooldown = random.randint(100, 1000)
        self.jump_cooldown = random.randint(100, 1000)
        self.movement_counter = 0
        self.jump_counter = 0
        self.speed_x = 180 * random.choice([-1, 1])

    def move_x(self, speed: float, mh: MainHero) -> None:
        self.x += speed / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_y(self, speed: float, mh: MainHero) -> None:
        self.y -= speed / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def start_jump(self, tiles_sprites) -> None:
        super().start_jump(tiles_sprites)

    def jump(self, tiles_sprites):
        super().jump(tiles_sprites)

    def update(self, *args, **kwargs) -> None:
        super().update()
        self.jump_counter += 1
        self.movement_counter += 1
        if self.jump_counter > self.jump_cooldown:
            self.start_jump(args[0])
            self.jump_cooldown = random.randint(1000, 1500)
            self.jump_counter = 0
        if self.movement_counter > self.movement_cooldown:
            self.speed_x *= -1
            self.movement_cooldown = random.randint(1000, 1500)
            self.movement_counter = 0

    def moveself_x(self, tiles_sprite):
        self.move_right(tiles_sprite) if self.speed_x > 0 else self.move_left(tiles_sprite)

