import pygame

from Character import Character


class Enemy(Character):
    def __init__(
        self,
        x: int,
        y: int,
        start_image: pygame.image,
        images: list[pygame.image],
        group_all_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(x, y, start_image, images, group_all_sprite)

