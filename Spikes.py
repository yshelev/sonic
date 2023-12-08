from MainHero import MainHero
from Settings import *
from Tiles import Tiles


class Spikes(Tiles):
    def __init__(self, x, y, width, height, image, *sprite_group):
        super().__init__(x, y, width, height, image, *sprite_group)

    def move_x(self, speed: float, mh: MainHero, tiles) -> None:
        self.rect = self.rect.move(speed / FPS, 0)

    def move_y(self, speed: float, mh: MainHero, tiles) -> None:
        self.rect = self.rect.move(0, -speed / FPS)
