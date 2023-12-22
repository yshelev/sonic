import sys

import pygame.event

from Eggman import Eggman
from MainHero import MainHero
import Settings
from Settings import *
from Tiles import Tiles
from button import Button


class SonicBossFight:
    def __init__(self, score, rings):
        self.score = score
        self.rings = rings

        self.my_font = pygame.font.SysFont('Bauhaus 93', 30)

        self.rings_sprites_count = 0

        self.background_image = pygame.transform.scale(pygame.image.load("data/backgrounds/background_greenhill.jpg"),
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

        self.all_tiles_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites_wo_mh = pygame.sprite.Group()
        self.all_bullets_sprites = pygame.sprite.Group()
        self.all_spikes_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.tile_image_width = pygame.transform.scale(pygame.image.load("data/GROUND/Platform.png"),
                                                       (SCREEN_WIDTH // 4, 300))

        with open("data/txts/boss_map.txt") as f:
            self.map = [i.split() for i in f.readlines()[::-1]]

        NUM_TALES_X = len(self.map[0])
        NUM_TALES_Y = len(self.map)

        TALE_WIDTH, TALE_HEIGHT = SCREEN_WIDTH / NUM_TALES_X, SCREEN_HEIGHT / NUM_TALES_Y

        for i in range(-1, 5):
            Tiles(i * SCREEN_WIDTH // 4, -SCREEN_HEIGHT // 2 + 5, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2,
                  self.tile_image_width,
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh)
            Tiles(i * SCREEN_WIDTH // 4, SCREEN_HEIGHT - 5, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2,
                  self.tile_image_width,
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh, )
            Tiles(SCREEN_WIDTH - 5, i * SCREEN_HEIGHT // 4, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4,
                  self.tile_image_width,
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh, )
            Tiles(-SCREEN_WIDTH // 3 + 5, i * SCREEN_HEIGHT // 4, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4,
                  self.tile_image_width,
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh, )

        for y in range(NUM_TALES_Y):
            for x in range(NUM_TALES_X):
                char = self.map[y][x]
                if char == "t":
                    Tiles(TALE_WIDTH * x, SCREEN_HEIGHT - (y + 1) * SCREEN_HEIGHT // 6, TALE_WIDTH,
                          TALE_HEIGHT // 10, pygame.image.load("data/GROUND/Platform.png"),
                          self.all_tiles_sprites,
                          self.all_sprites,
                          self.all_sprites_wo_mh)

                if char == "s":
                    Tiles(TALE_WIDTH * x, SCREEN_HEIGHT - y * SCREEN_HEIGHT // 6 - TALE_HEIGHT // 10,
                          TALE_WIDTH,
                          TALE_HEIGHT // 10, pygame.image.load("data/OBJECTS/SPIKES.png"),
                          self.all_spikes_sprites,
                          self.all_sprites,
                          self.all_sprites_wo_mh)



        self.main_hero = MainHero(
            0,
            SCREEN_HEIGHT - 105,
            pygame.image.load(f"data/Sonic Sprites/tile001.png"),
            running_sonic_right_sprites,
            running_sonic_right_sphere_sprites,
            fast_running_sonic_sprites,
            super_fast_running_sonic_sprites,
            pygame.image.load(f"data/Sonic Sprites/tile051.png"),
            self.rings,
            self.score,
            self.all_sprites
        )


        self.eggman = Eggman(SCREEN_WIDTH // 3 * 2, SCREEN_HEIGHT - 105, 100, 100,
                             self.all_sprites,
                             self.all_sprites_wo_mh)

        self.background_music = pygame.mixer.Sound('data/MUSIC/Bg_Music.mp3')

        self.sonic_in_animation()

    def play_music(self) -> None:
        self.background_music.set_volume(Settings.sound)
        self.background_music.play(-1)

    def stop_music(self) -> None:
        self.background_music.stop()

    def sonic_in_animation(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            screen.blit(self.background_image, (0, 0))
            running = self.main_hero.animation_boss_fight_in()
            self.main_hero.update()
            self.all_sprites.draw(screen)
            pygame.display.update()
        self.eggman_is_angry()

    def eggman_is_angry(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            screen.blit(self.background_image, (0, 0))
            running = self.eggman.man_jump_animation()
            self.all_sprites.draw(screen)
            pygame.display.update()
        self.eggman.reset_counter()
        self.eggman_is_running()

    def eggman_is_running(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            screen.blit(self.background_image, (0, 0))
            running = self.eggman.man_run_out()
            self.all_sprites.draw(screen)
            pygame.display.update()
        pygame.time.wait(2000)
        self.eggman.reset_counter()
        self.eggman_on_robot_animation()

    def eggman_on_robot_animation(self):
        self.eggman.turn_robot()
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            screen.blit(self.background_image, (0, 0))
            running = self.eggman.fall_on_robot_animation()
            self.all_sprites.draw(screen)
            pygame.display.update()
        self.eggman.reset_counter()
        self.eggman.turn_game_mod()
        self.play_music()
        self.game_loop()

    def game_loop(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            running = self.movement(running)
            self.update()

            screen.blit(self.background_image, (0, 0))
            self.draw()

            pygame.display.update()

    def prepare_eggman_death(self):
        self.all_bullets_sprites.empty()
        self.main_hero.start_boss_jump(self.all_tiles_sprites)
        self.main_hero.set_moving_left(False)
        self.main_hero.set_moving_right(False)
        self.all_sprites.add(self.eggman)

    def play_eggman_death(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            screen.blit(self.background_image, (0, 0))
            self.main_hero.movement_by_inertia_boss_level(self.all_tiles_sprites)
            self.main_hero.update()
            running = self.eggman.last_move(self.main_hero.x > (self.eggman.x + self.eggman.width // 2))
            self.all_sprites.draw(screen)

            pygame.display.flip()

        self.end_screen(True)

    def movement_of_main_character(self) -> bool:
        running = True
        keys = pygame.key.get_pressed()
        if self.main_hero.is_alive() * ((keys[pygame.K_SPACE] or keys[
            dict_movement[Settings.dict_movement_pointer]["top"]]) and not self.main_hero.get_is_jumping()) == 1:
            self.main_hero.play_sound_start_jump()
            self.main_hero.start_boss_jump(self.all_tiles_sprites)
        if self.main_hero.is_alive() * (not (keys[dict_movement[Settings.dict_movement_pointer]["left"]] and keys[
            dict_movement[Settings.dict_movement_pointer]["right"]])):
            if keys[dict_movement[Settings.dict_movement_pointer]["left"]]:
                self.main_hero.move_left_level_boss(self.all_tiles_sprites)
            else:
                self.main_hero.set_moving_left(False)
            if keys[dict_movement[Settings.dict_movement_pointer]["right"]]:
                self.main_hero.move_right_level_boss(self.all_tiles_sprites)
            else:
                self.main_hero.set_moving_right(False)
        elif self.main_hero.is_alive():
            self.main_hero.set_moving_right(True)
            self.main_hero.set_moving_left(True)
        if not self.main_hero.is_alive():
            self.last_screen = screen.copy()
            running = False
            self.play_mh_death()
            self.main_hero.dead_jump()

        if self.main_hero.get_is_jumping() * self.main_hero.is_alive():
            self.main_hero.jump_level_boss(self.all_tiles_sprites)
        if self.main_hero.rect.colliderect(self.eggman.rect):
            if self.eggman.collide_sonic(self.main_hero) * self.main_hero.available():
                self.main_hero.start_boss_jump_bounce(self.all_tiles_sprites)
        if not self.eggman.is_alive():
            self.last_screen = screen.copy()
            running = False
            self.eggman.reset_counter()
            self.eggman.eggman_death()
            self.prepare_eggman_death()
            self.play_eggman_death()

        self.main_hero.movement_by_inertia_boss_level(self.all_tiles_sprites)

        return running

    def quit(self):
        pygame.quit()
        sys.exit()

    def play_mh_death(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    quit()
            self.clock.tick(FPS)
            running = self.main_hero.dead_jump()

            self.last_screen.blit(self.background_image, (0, 0))

            self.all_sprites.draw(self.last_screen)
            screen.blit(self.last_screen, (0, 0))

            pygame.display.update()
        self.end_screen(False)

    def draw(self) -> None:

        self.draw_num_of_rings()
        self.draw_score()
        self.draw_lines()
        self.all_sprites.draw(screen)

    def get_font(self, size):
        return pygame.font.Font("data/menu_objects/menu_font.ttf", size)

    def draw_score(self):
        text_surface = self.my_font.render(f'score: {self.main_hero.get_score()}', True, (255, 255, 255))
        screen.blit(text_surface, (20, 40))

    def draw_lines(self) -> None:
        pygame.draw.rect(screen, (0, 0, 0), (
            SCREEN_WIDTH // 8 - 5, SCREEN_HEIGHT // 8 - 5, SCREEN_WIDTH - SCREEN_WIDTH // 4 + 10,
            SCREEN_HEIGHT // 8 + 10),
                         5)
        pygame.draw.rect(screen, (255, 0, 0), (
            SCREEN_WIDTH // 8, SCREEN_HEIGHT // 8,
            (SCREEN_WIDTH - SCREEN_WIDTH // 4) * int(self.eggman.hp) // int(self.eggman.max_hp),
            SCREEN_HEIGHT // 8))

    def draw_num_of_rings(self) -> None:
        self.rings_sprites_count = (self.rings_sprites_count + 1) % 48
        screen.blit(self.rings_sprites_for_draw[self.rings_sprites_count // 6], (5, 5))
        text_surface = self.my_font.render(f'X{self.main_hero.get_number_of_rings()}', True, (255, 255, 255))
        screen.blit(text_surface, (20, 0))

    def update(self):
        if self.eggman.can_shoot():
            self.eggman.shoot(self.all_sprites, self.all_bullets_sprites)

        if bullets := pygame.sprite.spritecollideany(self.main_hero, self.all_bullets_sprites):
            if self.main_hero.get_damage():
                bullets.kill()

        for bullet in self.all_bullets_sprites:
            bullet.move_self()
        self.main_hero.update()
        self.eggman.update(self.main_hero.x < self.eggman.x)

    def movement(self, running):
        running = self.movement_of_main_character() * running
        self.eggman.eggman_movement(self.main_hero)
        return running

    def end_screen(self, win):
        self.stop_music()
        if win:
            Settings.max_score = max(Settings.max_score_sonic, self.main_hero.get_score())
        dct_win_phrases = {
            True: "победа",
            False: "поражение"
        }
        running = True
        while running:

            bg = pygame.transform.scale(pygame.image.load(
                f"{"data/backgrounds/sonic_win_background.jpg" if win else "data/backgrounds/sonic_lose_background.jpg"}"),
                                        (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(bg, (0, 0))
            text_surface = pygame.font.Font("data/menu_objects/menu_font.ttf", 50).render(
                f'{dct_win_phrases[win]}. {"Новый рекорд!" if (win * (Settings.max_score_sonic == self.main_hero.get_score())) else "все по старому.."}',
                True, (0, 0, 0))
            screen.blit(text_surface, (75, 30) if not win else (10, 0))

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
            screen.blit(text_surface, (100, 125) if not win else (50, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETRY.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        SonicBossFight(self.score, self.rings)
                        del self
                    if RETURN_TO_MAIN_MENU.checkForInput(PLAY_MOUSE_POS):
                        running = False
            pygame.display.update()
