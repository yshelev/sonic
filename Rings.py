import pygame

from MainHero import MainHero
from Settings import *
from Tiles import Tiles


class Rings(Tiles):
    def __init__(self, x, y, width, height, images, *sprite_group):
        super().__init__(x, y, width, height, images[0], *sprite_group)

        self.counter = 0
        self.images = images

    def update(self, *args, **kwargs):
        self.counter = (self.counter + 1) % 48
        self.image = self.images[self.counter // 6 % 8]

    def move_x(self, speed: float, mh: MainHero) -> None:

        self.rect = self.rect.move(speed / FPS, 0)


    def move_y(self, speed: float, mh: MainHero) -> None:
        self.rect = self.rect.move(0, -speed / FPS)

