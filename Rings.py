import pygame

from MainHero import MainHero
from Settings import *
from Tiles import Tiles


class Rings(Tiles):
    def __init__(self, x, y, width, height, images, *sprite_group):
        super().__init__(x, y, width, height, images[0], *sprite_group)

        self.counter = 0
        self.images = list(map(lambda image: pygame.transform.scale(image, (width, height)), images))

    def update(self, *args, **kwargs):
        self.counter = (self.counter + 1) % 48
        self.image = self.images[self.counter // 6 % 8]



