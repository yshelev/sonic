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
        self.speed_x = 180 * random.randint(-1000, 1000) / 500.0
        self.enemy_death_sound = pygame.mixer.Sound('data/sounds/sonic/enemy_death.mp3')
        self.alive = True

    def move_x(self, speed: float, mh: MainHero, tiles) -> None:
        if self.can_move_x(tiles):
            self.x += speed / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_y(self, speed: float, mh: MainHero, tiles) -> None:
        if any(self.can_move_y(tiles)):
            self.y -= speed / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def start_jump(self, tiles_sprites) -> None:
        self.speed_y = -300
        self.is_jumping = True
        self.jump(tiles_sprites)

    def start_fall(self, tiles_sprites):
        self.speed_y = 0
        self.is_falling = True
        self.jump(tiles_sprites)

    def get_is_falling(self):
        return self.is_falling

    def check(self, tiles):
        tiles_stacked = self.stack(tiles)
        if tiles_stacked:
            tile: Tiles = tiles_stacked[0]
            top_indent = tile.rect.y - self.rect.y - self.rect.h
            bot_indent = tile.rect.y + tile.rect.h - self.rect.y
            self.y += top_indent if abs(top_indent) < bot_indent else bot_indent
            tile: Tiles = tiles_stacked[0]
            left_indent = tile.rect.x - self.rect.x - self.rect.w
            right_indent = tile.rect.x + tile.rect.w - self.rect.x
            self.x += -1 if abs(left_indent) < right_indent else 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def stack(self, tiles):
        return [i for i in tiles if i.rect.colliderect(self.rect)]

    def update(self, *args, **kwargs) -> None:
        self.jump_counter += 1
        self.movement_counter += 1
        if self.can_move_y(args[0]):
            self.is_falling = True
        if self.jump_counter > self.jump_cooldown:
            self.start_jump(args[0])
            self.jump_cooldown = random.randint(300, 900)
            self.jump_counter = 0
        if self.movement_counter > self.movement_cooldown:
            self.speed_x = 180 * random.randint(-1000, 1000) / 500.0
            self.movement_cooldown = random.randint(300, 900)
            self.movement_counter = 0

        super().update()

    def kill(self):
        self.play_enemy_death()
        super().kill()

    def is_alive(self):
        return self.alive

    def play_enemy_death(self) -> None:
        self.enemy_death_sound.set_volume(0.1)
        self.enemy_death_sound.play()

    def moveself_x(self, tiles_sprite):
        self.move_right(tiles_sprite) if self.speed_x > 0 else self.move_left(tiles_sprite) if self.speed_x < 0 else \
            None

    def can_move_y(self, tiles_sprites) -> (bool, bool):
        return (not (any(self.rect.move(0, (self.speed_y - 60) / FPS).colliderect(i) for i in tiles_sprites)),
                not (any(self.rect.move(0, (self.speed_y - 60) / FPS).colliderect(i) for i in tiles_sprites)),
                [i.rect.y - self.height - 1 for i in filter(lambda x: x.rect.y > self.rect.y, tiles_sprites) if (self.rect.move(0, (self.speed_y - 60) / FPS))])
