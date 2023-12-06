import random

import pygame

from Character import Character
from MainHero import MainHero
from Settings import *
from Tiles import Tiles


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

    def move_x(self, speed: float, mh: MainHero, tiles) -> None:
        if self.can_move_x(tiles):
            self.x += speed / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_y(self, speed: float, mh: MainHero, tiles) -> None:
        if self.can_move_y(tiles):
            self.y -= speed / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def check(self, tiles):
        tiles_stacked = self.stack(tiles)
        if tiles_stacked:
            tile: Tiles = tiles_stacked[0]
            top_indent = tile.rect.y - self.rect.y - self.rect.h
            bot_indent = tile.rect.y + tile.rect.h - self.rect.y
            self.y += top_indent if abs(top_indent) < bot_indent else bot_indent
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def stack(self, tiles):
        return [i for i in tiles if i.rect.colliderect(self.rect)]

    def start_jump(self, tiles_sprites) -> None:
        super().start_jump(tiles_sprites)

    def jump(self, tiles_sprites):
        super().jump(tiles_sprites)

    def update(self, *args, **kwargs) -> None:
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
        super().update()

    def moveself_x(self, tiles_sprite):
        self.move_right(tiles_sprite) if self.speed_x > 0 else self.move_left(tiles_sprite) if self.speed_x < 0 else \
            None
