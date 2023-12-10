from Settings import *


class Enemy_score(pygame.sprite.Sprite):
    def __init__(self, score, font, rect, *groups):
        super().__init__(*groups)
        self.score = score
        self.image = font.render(f"{score}", True, (255, 255, 255))
        self.rect = rect
        self.speed_y = -600
        self.additional_speed_y = 10


    def update(self, tiles):
        self.speed_y = min(0, self.additional_speed_y + self.speed_y)
        self.rect = self.rect.move(0, self.speed_y / FPS)
        if self.speed_y == 0:
            self.kill()
