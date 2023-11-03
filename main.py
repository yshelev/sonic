import pygame

pygame.init()

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Character(pygame.sprite.Sprite):
    PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60

    def __init__(self, x, y, image, group_all_sprite):
        super().__init__(group_all_sprite)
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image), (PLAYER_WIDTH, PLAYER_HEIGHT))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def update(self, *args, **kwargs):
        self.draw()


class MainHero(Character, pygame.sprite.Sprite):
    def __init__(self, x, y, image, group_all_sprite):
        super().__init__(x, y, image, group_all_sprite)

    def update(self, *args, **kwargs):
        self.draw()


class Enemy(Character):
    def __init__(self, x, y, image, group_all_sprite):
        super().__init__(x, y, image, group_all_sprite)


pygame.display.set_caption("иуиу сониИИК")

background_image = pygame.image.load("data/background_greenhill.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

main_hero = MainHero(100, 100, "data/sonic.png", all_sprites)

running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    pygame.display.flip()

    all_sprites.update()

pygame.quit()
