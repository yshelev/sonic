from Settings import *
from Tiles import Tiles


class Enemy_score(pygame.sprite.Sprite):
    def __init__(self, score, font, rect, *groups):
        super().__init__(*groups)
        self.score = score
        self.image = font.render(f"{score}", True, (255, 255, 255))
        self.rect = rect
        self.speed_y = -600
        self.additional_speed_y = 1200

    def update(self, tiles):
        self.speed_y += self.additional_speed_y / FPS
        self.rect = self.rect.move(0, -self.speed_y / FPS)
        if self.rect.y <= 0:
            self.kill()


