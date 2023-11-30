from MainHero import MainHero
from Settings import *


class Tiles(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, *sprite_group):
        super().__init__(*sprite_group)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def move_x(self, speed: float, mh: MainHero) -> None:
        can_move_left, can_move_right = self.can_move_x(speed, mh)
        if can_move_right and can_move_left:
            self.rect = self.rect.move(speed / FPS, 0)

    def can_move_x(self, speed: float, mh: MainHero) -> (bool, bool):
        return not self.rect.move(-speed / FPS, 0).colliderect(mh.rect), not self.rect.move(speed / FPS, 0).colliderect(mh.rect)

