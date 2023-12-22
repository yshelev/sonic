import pygame

from Settings import SCREEN_WIDTH


class My_group(pygame.sprite.AbstractGroup):
    def __init__(self):
        super().__init__()

    def draw(self, surface, bgsurf=None, special_flags=0):
        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    [sprite for sprite in sprites if
                     0 < sprite.rect.x + sprite.rect.width and sprite.rect.x < SCREEN_WIDTH],
                    surface.blits(
                        (spr.image, spr.rect, None, special_flags) for spr in sprites if
                        0 < spr.rect.x + spr.rect.width and spr.rect.x < SCREEN_WIDTH
                    ),
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(
                    spr.image, spr.rect, None, special_flags
                )
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
