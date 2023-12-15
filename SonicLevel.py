import sys

import pygame

from Enemy_score import Enemy_score
from MainHero import MainHero
from Settings import *
from SonicBossFight import SonicBossFight
from Tiles import Tiles
from Enemy import Enemy
from Rings import Rings
from button import Button


class SonicLevel:
    def __init__(self):
        self.last_screen = None
        self.my_font = pygame.font.SysFont('Bauhaus 93', 30)
        self.background_image = pygame.transform.scale(pygame.image.load("data/background_greenhill.jpg"),
                                                       (SCREEN_WIDTH, SCREEN_HEIGHT))

        running_sonic_right_sprites = [
            pygame.image.load(f"data/Sonic Sprites/tile00{i // 5}.png")
            if i < 50 else
            pygame.image.load(f"data/Sonic Sprites/tile0{i // 5}.png")
            for i in range(8 * 5, 11 * 5)
        ]
        running_sonic_right_sphere_sprites = [
            pygame.image.load(f"data/Sonic Sprites/tile00{i // 3}.png")
            if i < 30 else
            pygame.image.load(f"data/Sonic Sprites/tile0{i // 3}.png")
            for i in range(32 * 3, 37 * 3)
        ]
        fast_running_sonic_sprites = [
            pygame.image.load(f"data/Sonic Sprites/tile00{i // 2}.png")
            if i < 20 else
            pygame.image.load(f"data/Sonic Sprites/tile0{i // 2}.png")
            for i in range(24 * 2, 28 * 2)
        ]
        super_fast_running_sonic_sprites = [
            pygame.image.load(f"data/Sonic Sprites/tile{i // 2}{i // 2}{i // 2}.png")
            for i in range(1 * 2, 5 * 2)
        ]
        self.rings_sprites_for_draw = [
            pygame.transform.scale(pygame.image.load(f'data/Rings spritez/Sprite-000{i}.png'), (20, 20))
            for i in range(1, 9)
        ]
        self.rings_sprites = [
            pygame.transform.scale(pygame.image.load(f'data/Rings spritez/Sprite-000{i}.png'), (100, 100))
            for i in range(1, 9)
        ]
        self.enemy_images = [
            pygame.transform.scale(pygame.image.load(f'data/ENEMY/BUG {i // 3}.2.png'), (1000, 1000))
            for i in range(3, 12)
        ]
        self.rings_sprites_count = 0

        self.rings_sprites = [
            pygame.transform.scale(pygame.image.load(f'data/Rings spritez/Sprite-000{i}.png'), (20, 20))
            for i in range(1, 9)
        ]
        self.death_sprites = [
            pygame.image.load(f"data/Sonic Sprites/tile0{i // 2}.png")
            for i in range(51 * 2, 53 * 2)
        ]

        self.rings_sprites_count = 0

        self.immune_timer = pygame.time.Clock()

        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_rings_sprites = pygame.sprite.Group()
        self.all_tiles_sprites = pygame.sprite.Group()
        self.all_enemy_sprites = pygame.sprite.Group()
        self.all_sprites_wo_mh = pygame.sprite.Group()
        self.all_spikes_sprites = pygame.sprite.Group()
        self.all_enemies_score = pygame.sprite.Group()
        with open("data/map.txt") as f:
            self.map = [i.split() for i in f.readlines()[::-1]]

        NUM_TALES_X = len(self.map[0])
        NUM_TALES_Y = len(self.map)

        TALE_WIDTH, TALE_HEIGHT = 8 * SCREEN_WIDTH / NUM_TALES_X, 2 * SCREEN_HEIGHT / NUM_TALES_Y

        for i in range(10):
            Tiles(SCREEN_WIDTH // 60 * 8 * (-NUM_TALES_X // 2 - 2), SCREEN_HEIGHT - (i + 1) * 300, 300, 300,
                  pygame.transform.rotate(pygame.image.load("data/GROUND/Floor.png"), 270),
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh)
        for i in range(10):
            Tiles(SCREEN_WIDTH // 60 * 8 * (NUM_TALES_X // 2), SCREEN_HEIGHT - (i + 1) * 300, 300, 300,
                  pygame.transform.rotate(pygame.image.load("data/GROUND/Floor.png"), 90),
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh)
        for i in range(-50, 51):
            Tiles(i * 300, SCREEN_HEIGHT, 300, SCREEN_HEIGHT // 3, pygame.image.load("data/GROUND/Floor.png"),
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh)
        for y in range(NUM_TALES_Y):
            for x in range(-NUM_TALES_X // 2, NUM_TALES_X // 2):
                char = self.map[y][x + NUM_TALES_X // 2]
                if char == "t":
                    Tiles(SCREEN_WIDTH // 60 * 8 * x, SCREEN_HEIGHT - (y + 1) * SCREEN_HEIGHT // 6, TALE_WIDTH,
                          TALE_HEIGHT // 10, pygame.image.load("data/GROUND/Platform.png"),
                          self.all_tiles_sprites,
                          self.all_sprites,
                          self.all_sprites_wo_mh)
                if char == "e":
                    Enemy(SCREEN_WIDTH // 60 * 8 * x, SCREEN_HEIGHT - (y + 1) * SCREEN_HEIGHT // 6,
                          self.enemy_images[0],
                          self.enemy_images,
                          self.enemy_images,
                          self.enemy_images[0],
                          self.all_enemy_sprites,
                          self.all_sprites,
                          self.all_sprites_wo_mh
                          )
                if char == "s":
                    Tiles(SCREEN_WIDTH // 60 * 8 * x, SCREEN_HEIGHT - y * SCREEN_HEIGHT // 6 - TALE_HEIGHT // 10,
                          TALE_WIDTH,
                          TALE_HEIGHT // 10, pygame.image.load("data/OBJECTS/SPIKES.png"),
                          self.all_spikes_sprites,
                          self.all_sprites,
                          self.all_sprites_wo_mh)

                if char == "f":
                    self.finish_tale = Tiles(SCREEN_WIDTH // 60 * 8 * x,
                                             SCREEN_HEIGHT - y * SCREEN_HEIGHT // 6 - TALE_HEIGHT // 2, TALE_WIDTH,
                                             TALE_HEIGHT // 2, pygame.image.load("data/eggman_signs/eggman_sign_1.png"),
                                             self.all_sprites,
                                             self.all_sprites_wo_mh,
                                             animation_list=list(map(lambda x: pygame.transform.scale(x, (TALE_WIDTH, TALE_HEIGHT // 2)), [pygame.image.load(f"data/eggman_signs/eggman_sign_{i // 3}.png") for i in range(3, 15)])))

                if char == "r":
                    for k in range(5):
                        Rings(SCREEN_WIDTH // 60 * 8 * x + 35 * k, SCREEN_HEIGHT - y * SCREEN_HEIGHT // 6 - 35, 35, 35,
                              self.rings_sprites,
                              self.all_sprites,
                              self.all_rings_sprites,
                              self.all_sprites_wo_mh)

        self.main_hero = MainHero(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            pygame.image.load(f"data/Sonic Sprites/tile001.png"),
            running_sonic_right_sprites,
            running_sonic_right_sphere_sprites,
            fast_running_sonic_sprites,
            super_fast_running_sonic_sprites,
            pygame.image.load(f"data/Sonic Sprites/tile051.png"),
            self.all_sprites
        )
        self.background_image_x, self.background_image_y = SCREEN_WIDTH, 0
        self.background_image_slow = 4
        self.background_image_speed_x = 0.6

        self.background_music = pygame.mixer.Sound('data/MUSIC/Bg_Music.mp3')

        # self.play_music()
        self.game_loop()

    def play_music(self) -> None:
        self.background_music.set_volume(0.1)
        self.background_music.play(-1)

    def game_loop(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            running = self.movement_of_main_character() * running
            self.background_image_movement()
            self.all_sprites.update(self.all_tiles_sprites)
            self.draw()
            pygame.display.flip()
        self.background_music.stop()

    def end_screen(self, win):
        dct_win_phrases = {
            True: "победа",
            False: "поражение"
        }
        running = True
        while running:

            bg = pygame.transform.scale(pygame.image.load("data/background_greenhill.jpg"),
                                        (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(bg, (0, 0))
            text_surface = pygame.font.Font("data/menu_objects/menu_font.ttf", 50).render(
                f'{dct_win_phrases[win]}',
                True, (255, 255, 255))
            screen.blit(text_surface, (400, 100))

            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            RETRY = Button(image=pygame.image.load("data/menu_objects/character_rect.png"),
                           pos=(SCREEN_WIDTH // 1.2, 650),
                           text_input="ЗАНОВО", font=self.get_font(50), base_color="White",
                           hovering_color="Orange")

            RETRY.changeColor(pygame.mouse.get_pos())
            RETRY.update(screen)

            RETURN_TO_MAIN_MENU = Button(image=pygame.image.load("data/menu_objects/character_rect.png"),
                                         pos=(SCREEN_WIDTH // 1.2, 750),
                                         text_input="В МЕНЮ", font=self.get_font(50), base_color="White",
                                         hovering_color="Orange")

            RETURN_TO_MAIN_MENU.changeColor(pygame.mouse.get_pos())
            RETURN_TO_MAIN_MENU.update(screen)

            text_surface = pygame.font.Font("data/menu_objects/menu_font.ttf", 50).render(
                f'ОЧКИ: {self.main_hero.score}',
                True, (0, 0, 0))
            screen.blit(text_surface, (20, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETRY.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        SonicLevel()
                    if RETURN_TO_MAIN_MENU.checkForInput(PLAY_MOUSE_POS):
                        running = False
            pygame.display.update()

    def get_font(self, size):
        return pygame.font.Font("data/menu_objects/menu_font.ttf", size)

    def draw_lines(self) -> None:
        pygame.draw.rect(screen, "black", (100, 479, 10, 10))
        pygame.draw.rect(screen, "black", (self.main_hero.x + 5,
                                           self.main_hero.y - self.main_hero.speed_y / FPS,
                                           self.main_hero.width - 5,
                                           self.main_hero.height + self.main_hero.speed_y / FPS))
        pygame.draw.rect(screen, "red", (self.main_hero.x + 5,
                                         self.main_hero.y,
                                         self.main_hero.width - 5,
                                         self.main_hero.height + self.main_hero.speed_y / FPS)
                         )

    def draw_num_of_rings(self) -> None:
        self.rings_sprites_count = (self.rings_sprites_count + 1) % 48
        screen.blit(self.rings_sprites_for_draw[self.rings_sprites_count // 6], (5, 5))
        text_surface = self.my_font.render(f'X{self.main_hero.get_number_of_rings()}', True, (255, 255, 255))
        screen.blit(text_surface, (20, 0))

    def draw_score(self):
        text_surface = self.my_font.render(f'score: {self.main_hero.get_score()}', True, (255, 255, 255))
        screen.blit(text_surface, (20, 40))

    def movement_of_main_character(self) -> bool:
        running = True
        keys = pygame.key.get_pressed()
        if self.main_hero.is_alive() * (keys[pygame.K_SPACE] and not self.main_hero.get_is_jumping()):
            self.main_hero.play_sound_start_jump()
            self.main_hero.start_jump(self.all_tiles_sprites)
        if self.main_hero.is_alive() * (not ((keys[pygame.K_LEFT] or keys[button_settings["left"]]) and (
                keys[pygame.K_RIGHT] or keys[button_settings["right"]]))):
            if keys[pygame.K_LEFT] or keys[button_settings["left"]]:
                output_code, movement_sprites_speed = self.main_hero.move_left(self.all_tiles_sprites)
                if output_code in [STOPPED_BY_RIGHT_INVISIBLE_WALL, STOPPED_BY_LEFT_INVISIBLE_WALL]:
                    for tile in self.all_sprites_wo_mh:
                        tile.move_x(movement_sprites_speed, self.main_hero, self.all_tiles_sprites)
            else:
                self.main_hero.set_moving_left(False)

            if keys[pygame.K_RIGHT] or keys[button_settings["right"]]:
                output_code, movement_sprites_speed = self.main_hero.move_right(self.all_tiles_sprites)
                if output_code in [STOPPED_BY_RIGHT_INVISIBLE_WALL, STOPPED_BY_LEFT_INVISIBLE_WALL]:
                    for tile in self.all_sprites_wo_mh:
                        tile.move_x(-movement_sprites_speed, self.main_hero, self.all_tiles_sprites)
            else:
                self.main_hero.set_moving_right(False)
        elif self.main_hero.is_alive():
            self.main_hero.set_moving_right(True)
            self.main_hero.set_moving_left(True)

        if self.main_hero.get_is_jumping() * self.main_hero.is_alive():
            jump_speed_tiles = self.main_hero.jump(self.all_tiles_sprites)
            for tile in self.all_sprites_wo_mh:
                tile.move_y(jump_speed_tiles, self.main_hero, self.all_tiles_sprites)

        output_code_x, movement_sprites_speed_x, output_code_y, movement_sprites_speed_y = \
            self.main_hero.movement_by_inertia(self.all_tiles_sprites)
        if exit_codes["sonic_movement_x"][output_code_x] in [STOPPED_BY_RIGHT_INVISIBLE_WALL,
                                                             STOPPED_BY_LEFT_INVISIBLE_WALL] * self.main_hero.is_alive():
            for tile in self.all_sprites_wo_mh:
                tile.move_x(-movement_sprites_speed_x, self.main_hero, self.all_tiles_sprites)
        if exit_codes["sonic_movement_y"][output_code_y] in [STOPPED_BY_TOP_INVISIBLE_WALL,
                                                             STOPPED_BY_BOT_INVISIBLE_WALL] * self.main_hero.is_alive():
            for tile in self.all_sprites_wo_mh:
                tile.move_y(movement_sprites_speed_y, self.main_hero, self.all_tiles_sprites)
        if pygame.sprite.spritecollideany(self.main_hero, self.all_spikes_sprites):
            self.main_hero.get_damage()
        if pygame.sprite.spritecollideany(self.main_hero, self.all_rings_sprites):
            rings = pygame.sprite.spritecollideany(self.main_hero, self.all_rings_sprites)
            self.main_hero.add_rings()
            rings.kill()
        if pygame.sprite.spritecollideany(self.main_hero, self.all_enemy_sprites):
            enemies = pygame.sprite.spritecollideany(self.main_hero, self.all_enemy_sprites)
            if self.main_hero.collide_enemy(enemies):
                Enemy_score(self.main_hero.get_add_score(), self.my_font,
                            pygame.Rect(enemies.rect.x, enemies.rect.y, 100, 100), self.all_sprites)
                self.main_hero.start_jump(self.all_tiles_sprites)
        if self.check_exit():
            self.last_screen = screen.copy()
            running = False
            self.next_level()
            self.main_hero.animation_next_level()

        if not self.main_hero.is_alive():
            self.last_screen = screen.copy()
            running = False
            self.play_mh_death()
            self.main_hero.dead_jump()

        for i in self.all_enemy_sprites:
            if i.is_alive():
                i.check(self.all_tiles_sprites)
                if i.get_is_jumping() or i.get_is_falling():
                    i.jump(self.all_tiles_sprites)
                i.moveself_x(self.all_tiles_sprites)
            else:
                i.dead_jump()

        return running

    def play_mh_death(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    self.quit()
            self.clock.tick(FPS)
            running = self.main_hero.dead_jump()

            self.last_screen.blit(self.background_image, (self.background_image_x - SCREEN_WIDTH, 0))
            self.last_screen.blit(self.background_image, (self.background_image_x, 0))

            self.all_sprites.draw(self.last_screen)
            screen.blit(self.last_screen, (0, 0))

            pygame.display.update()

        self.end_screen(False)

    def background_image_movement(self) -> None:
        if self.main_hero.get_additional_speed() > 0:
            if (self.background_image_x - self.background_image_speed_x) > 0:
                self.background_image_x -= (self.background_image_speed_x * self.main_hero.get_additional_speed() / (
                        FPS * self.background_image_slow))
            else:
                self.background_image_x = SCREEN_WIDTH
        elif self.main_hero.get_additional_speed() < 0:
            if (self.background_image_x + self.background_image_speed_x) < SCREEN_WIDTH:
                self.background_image_x += (
                        self.background_image_speed_x * -self.main_hero.get_additional_speed() / (
                        FPS * self.background_image_slow) * self.background_image_x + self.background_image_speed_x > 0)
            else:
                self.background_image_x = 0

    def draw(self) -> None:
        screen.blit(self.background_image, (self.background_image_x - SCREEN_WIDTH, 0))
        screen.blit(self.background_image, (self.background_image_x, 0))

        self.draw_num_of_rings()
        self.draw_score()
        # self.draw_lines()
        self.all_sprites.draw(screen)

    def next_level(self):
        self.last_animation()
        # self.all_sprites.empty()
        SonicBossFight(self.main_hero.get_number_of_rings(), self.main_hero.get_score())

    def quit(self):
        pygame.quit()
        sys.exit()

    def check_exit(self):
        return self.main_hero.rect.colliderect(self.finish_tale)

    def last_animation(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    self.quit()

            running = self.main_hero.animation_next_level()

            self.main_hero.update()
            self.finish_tale.animation_finish_tale()

            screen.blit(self.background_image, (self.background_image_x - SCREEN_WIDTH, 0))
            screen.blit(self.background_image, (self.background_image_x, 0))

            self.all_sprites.draw(screen)

            pygame.display.update()
