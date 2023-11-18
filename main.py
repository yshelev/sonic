import pygame

from MainHero import MainHero
from Enemy import Enemy
from Ring import Ring
from Settings import *


def play_music():
    bg_music = pygame.mixer.Sound('data/Bg_Music.mp3')
    bg_music.set_volume(0.1)
    bg_music.play(-1)


def draw_num_of_rings():
    global rings_sprites_count
    rings_sprites_count += 1
    screen.blit(rings_sprites[rings_sprites_count // 6 % 8], (5, 5))
    my_font = pygame.font.SysFont('Bauhaus 93', 30)
    text_surface = my_font.render("X" + str(main_hero.get_number_of_rings()), True, (255, 255, 255))
    screen.blit(text_surface, (20, 0))


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("[ezrf")

background_image = pygame.transform.scale(pygame.image.load("data/background_greenhill.jpg"),
                                          (SCREEN_WIDTH * 2, SCREEN_HEIGHT))

# running_sonick_right = [
#     pygame.image.load(f"data/Sonic Sprites/tile00{i}.png")
#     if i < 10 else
#     pygame.image.load(f"data/Sonic Sprites/tile0{i}.png")
#     for i in range(24, 28)
# ]
running_sonick_right_sprites = [
    pygame.image.load(f"data/Sonic Sprites/tile00{i}.png")
    if i < 10 else
    pygame.image.load(f"data/Sonic Sprites/tile0{i}.png")
    for i in range(8, 14)
]
running_sonick_right_sphere_sprites = [
    pygame.image.load(f"data/Sonic Sprites/tile00{i}.png")
    if i < 10 else
    pygame.image.load(f"data/Sonic Sprites/tile0{i}.png")
    for i in range(32, 37)
]

rings_sprites = [
    pygame.transform.scale(pygame.image.load(f'data/Rings spritez/Sprite-000{i}.png'), (20, 20))
    for i in range(1, 9)
]
rings_sprites_count = 0

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

main_hero = MainHero(
    100,
    100,
    pygame.image.load(f"data/Sonic Sprites/tile001.png"),
    running_sonick_right_sprites,
    running_sonick_right_sphere_sprites,
    all_sprites
)

# play_music()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not main_hero.get_is_jumping() and main_hero.get_can_jump():
        main_hero.start_jump()
    if not ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d])):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            main_hero.move_left()
        else:
            main_hero.set_moving_left(False)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            main_hero.move_right()
        else:
            main_hero.set_moving_right(False)
    else:
        main_hero.set_moving_right(True)
        main_hero.set_moving_left(True)

    if main_hero.get_is_jumping():
        main_hero.jump()

    screen.blit(background_image, (0, 0, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))
    # screen.blit(rings_sprites[0], (100, 100))

    all_sprites.update()
    draw_num_of_rings()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
