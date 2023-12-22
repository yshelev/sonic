import pygame.sprite

from Settings import *


class FireBall(pygame.sprite.Sprite):
    def __init__(self, x, y, image, typ, *groups):
        super().__init__(*groups)
        self.speed = 600

        self.movement_dict = {
            "r": (self.speed / FPS, 0),
            "l": (-self.speed / FPS, 0),
            "t": (0, self.speed / FPS),
            "b": (0, -self.speed / FPS),
        }
        self.rect = pygame.Rect(x, y, 20, 20)
        self.image = image
        self.typ = typ

    def moveself(self):
        self.rect = self.rect.move(self.movement_dict[self.typ])

    def update(self, *args, **kwargs):
        if self.rect.x < 0 or self.rect.y < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT:
            self.kill()
        self.moveself()
