import pygame


class Ring(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group_all_sprites) -> None:
        super().__init__(group_all_sprites)
        self.width, self.height = 50, 50
        self.x, self.y = x, y
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)



