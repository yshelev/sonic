import pygame


class Tiles(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, *sprite_group):
        super().__init__(*sprite_group)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def move_x(self, speed: float) -> None:
        self.rect = self.rect.move(speed, 0)