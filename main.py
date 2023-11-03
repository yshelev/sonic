import pygame

pygame.init()

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# класс персонаж - Character - наследуется от класса спрайт для того, чтобы его можно было
#
class Character(pygame.sprite.Sprite):

    def __init__(self, x, y, image, group_all_sprite):
        super().__init__(group_all_sprite)
        self.PLAYER_WIDTH, self.PLAYER_HEIGHT = 40, 60

        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = (x, y, x + self.PLAYER_WIDTH, y + self.PLAYER_HEIGHT)
        self.speed = 1

    def update(self, *args, **kwargs):
        self.rect = (self.x, self.y, self.x + self.PLAYER_WIDTH, self.y + self.PLAYER_HEIGHT)


    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed



class MainHero(Character):
    def __init__(self, x, y, image, group_all_sprite):
        super().__init__(x, y, image, group_all_sprite)


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

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        main_hero.move_left()

    screen.blit(background_image, (0, 0))

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
