from MainHero import MainHero
from Settings import *


class Tiles(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, *sprite_group, **kwargs):
        super().__init__(*sprite_group)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.counter = 0
        self.animation_speed = 0.1
        if len(kwargs):
            self.animation_images = kwargs["animation_list"]

    def move_x(self, speed: float, mh: MainHero, tiles) -> None:
        self.rect = self.rect.move(speed / FPS, 0)

    def can_move_x(self, speed: float, mh: MainHero, tiles) -> (bool, bool):
        return not self.rect.move(-speed / FPS, 0).colliderect(mh.rect), not self.rect.move(speed / FPS, 0).colliderect(mh.rect)

    def move_y(self, speed: float, mh: MainHero, tiles) -> None:
        self.rect = self.rect.move(0, -speed / FPS)

    def can_move_y(self, speed: float, mh: MainHero, tiles) -> (bool, bool):
        return not self.rect.move(0, speed / FPS).colliderect(mh.rect), not self.rect.move(0, speed / FPS).colliderect(mh.rect)

    def animation_finish_tale(self):
        print(self.counter)
        if self.counter >= 0:
            self.counter += self.animation_speed
        if self.counter > 12 - 0.1 - self.animation_speed:
            self.counter = -12
        self.image = self.animation_images[int(self.counter)]

