import pygame
class Tiles(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, image, *sprite_group):
        super().__init__(*sprite_group)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)


