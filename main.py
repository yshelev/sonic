import pygame

from MainHero import MainHero
from Enemy import Enemy
from Settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# bg_music = pygame.mixer.Sound('data/Bg_Music.mp3')
# bg_music.play(-1)
# bg_music.set_volume(0.1)


# класс персонаж - Character - наследуется от класса спрайт для того, чтобы его можно было
# присоединить к группе спрайтов и работать уже с этой группе, а не с каждым элеметом группы
# по отдельности


pygame.display.set_caption("иуиу сониИИК")

background_image = pygame.transform.scale(pygame.image.load("data/background_greenhill.jpg"),
                                          (SCREEN_WIDTH, SCREEN_HEIGHT))

running_sonick_right = [
    pygame.image.load(f"data/Sonic Sprites/tile00{i}.png")
    if i < 10 else
    pygame.image.load(f"data/Sonic Sprites/tile0{i}.png")
    for i in range(8, 14)
]
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

main_hero = MainHero(100, 100, pygame.image.load(f"data/Sonic Sprites/tile001.png"), running_sonick_right, all_sprites)

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
    else:
        main_hero.set_moving_left(False)

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        main_hero.move_right()
    else:
        main_hero.set_moving_right(False)

    if main_hero.get_is_jumping():
        main_hero.jump()

    screen.blit(background_image, (0, 0))

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
