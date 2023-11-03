import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# bg_music = pygame.mixer.Sound('data/Bg_Music.mp3')
# bg_music.play(-1)
# bg_music.set_volume(0.1)


# класс персонаж - Character - наследуется от класса спрайт для того, чтобы его можно было
# присоединить к группе спрайтов и работать уже с этой группе, а не с каждым элеметом группы
# по отдельности
class Character(pygame.sprite.Sprite):

    def __init__(self, x, y, image, group_all_sprite):
        super().__init__(group_all_sprite)
        self.width, self.height = 40, 60
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image), (self.width, self.height))
        self.rect = (x, y, x + self.width, y + self.height)
        self.speed_x = 50
        self.speed_y = -10
        self.image_right_move = self.image
        self.is_jumping = False
        self.image_left_move = pygame.transform.flip(self.image, True, False)

    def update(self, *args, **kwargs):
        self.rect = (self.x, self.y, self.x + self.width, self.y + self.height)

    def move_left(self):
        self.image = self.image_left_move
        if self.x - self.speed_x >= 0:
            self.x -= self.speed_x
        else:
            self.x = 0

    def move_right(self):
        self.image = self.image_right_move
        if self.x + self.width + self.speed_x <= SCREEN_WIDTH:
            self.x += self.speed_x
        else:
            self.x = SCREEN_WIDTH - self.width

    def jump(self):
        self.speed_y += GRAVITY
        if self.speed_y + self.y + self.height < SCREEN_HEIGHT:
            if self.y + self.speed_y > 0:
                self.y += self.speed_y
            else:
                self.y = 0
        else:
            self.y = SCREEN_HEIGHT - self.height

    def get_is_jumping(self):
        return self.is_jumping

    def set_is_jumping(self, is_jumping):
        self.is_jumping = is_jumping

    def set_speed_y(self, speed_y):
        self.speed_y = speed_y


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
    if keys[pygame.K_SPACE] and not main_hero.get_is_jumping():
        main_hero.set_speed_y(-10)
        main_hero.set_is_jumping(True)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        main_hero.move_left()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        main_hero.move_right()

    if main_hero.get_is_jumping():
        main_hero.jump()

    screen.blit(background_image, (0, 0))

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
