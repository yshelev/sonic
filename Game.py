import pygame

from MainHero import MainHero
from Tiles import Tiles
from Enemy import Enemy
from Ring import Ring
from Settings import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("[ezrf")

        self.background_image = pygame.transform.scale(pygame.image.load("data/background_greenhill.jpg"),
                                                       (SCREEN_WIDTH, SCREEN_HEIGHT))
        running_sonick_right_sprites = [
            pygame.image.load(f"data/Sonic Sprites/tile00{i // 2}.png")
            if i < 20 else
            pygame.image.load(f"data/Sonic Sprites/tile0{i // 2}.png")
            for i in range(8 * 2, 11 * 2)
        ]
        running_sonick_right_sphere_sprites = [
            pygame.image.load(f"data/Sonic Sprites/tile00{i // 2}.png")
            if i < 10 else
            pygame.image.load(f"data/Sonic Sprites/tile0{i // 2}.png")
            for i in range(32 * 2, 37 * 2)
        ]

        self.rings_sprites = [
            pygame.transform.scale(pygame.image.load(f'data/Rings spritez/Sprite-000{i}.png'), (20, 20))
            for i in range(1, 9)
        ]
        self.rings_sprites_count = 0

        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_tiles_sprites = pygame.sprite.Group()
        Tiles(100, 100, 100, 100, pygame.image.load("data/background_greenhill.jpg"), self.all_tiles_sprites,
              self.all_sprites)
        self.main_hero = MainHero(
            100,
            100,
            pygame.image.load(f"data/Sonic Sprites/tile001.png"),
            running_sonick_right_sprites,
            running_sonick_right_sphere_sprites,
            self.all_sprites
        )
        self.background_image_x, self.background_image_y = SCREEN_WIDTH, 0
        self.background_image_speed_x = 0.01
        # self.play_music()
        self.game_loop()

    def play_music(self) -> None:
        bg_music = pygame.mixer.Sound('data/Bg_Music.mp3')
        bg_music.set_volume(0.1)
        bg_music.play(-1)

    def game_loop(self) -> None:
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not self.main_hero.get_is_jumping():
                self.main_hero.start_jump()
            if not ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d])):
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.main_hero.move_left()
                else:
                    self.main_hero.set_moving_left(False)

                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.main_hero.move_right()
                else:
                    self.main_hero.set_moving_right(False)
            else:
                self.main_hero.set_moving_right(True)
                self.main_hero.set_moving_left(True)

            if self.main_hero.get_is_jumping():
                self.main_hero.jump()

            screen.blit(self.background_image, (self.background_image_x - SCREEN_WIDTH, 0))
            screen.blit(self.background_image, (self.background_image_x, 0))
            # screen.blit(self.rings_sprites[0], (100, 100))
            if self.main_hero.get_additional_speed() > 0:
                if (self.background_image_x - self.background_image_speed_x) > 0:
                    self.background_image_x -= self.background_image_speed_x * self.main_hero.get_additional_speed()
                else:
                    self.background_image_x = SCREEN_WIDTH
            elif self.main_hero.get_additional_speed() < 0:
                if (self.background_image_x + self.background_image_speed_x) < SCREEN_WIDTH:
                    if self.background_image_x + self.background_image_speed_x > 0:
                        self.background_image_x += self.background_image_speed_x * -self.main_hero.get_additional_speed()
                else:
                    self.background_image_x = 0

            self.all_sprites.update()
            self.draw_num_of_rings()
            self.all_sprites.draw(screen)
            pygame.display.flip()

        self.quit()

    def draw_num_of_rings(self) -> None:
        self.rings_sprites_count += 1
        screen.blit(self.rings_sprites[self.rings_sprites_count // 6 % 8], (5, 5))
        my_font = pygame.font.SysFont('Bauhaus 93', 30)
        text_surface = my_font.render(f'X{self.main_hero.get_number_of_rings()}', True, (255, 255, 255))
        screen.blit(text_surface, (20, 0))

    def quit(self) -> None:
        pygame.quit()
