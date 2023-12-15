import sys

import pygame.event

from Eggman import Eggman
from MainHero import MainHero
from Settings import *
from Tiles import Tiles


class SonicBossFight:
    def __init__(self, score, rings):
        self.score = score
        self.rings = rings

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

        self.all_tiles_sprites = pygame.sprite.Group()
        self.rlbt_tiles_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites_wo_mh = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.tile_image_width = pygame.transform.scale(pygame.image.load("data/GROUND/Platform.png"),
                                                       (SCREEN_WIDTH // 4, 300))

        for i in range(-1, 5):
            Tiles(i * SCREEN_WIDTH // 4, -SCREEN_HEIGHT // 2, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2,
                  self.tile_image_width,
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh,
                  self.rlbt_tiles_sprites)
            Tiles(i * SCREEN_WIDTH // 4, SCREEN_HEIGHT - 5, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2,
                  self.tile_image_width,
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh,
                  self.rlbt_tiles_sprites)
            Tiles(SCREEN_WIDTH - 5, i * SCREEN_HEIGHT // 4, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4,
                  self.tile_image_width,
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh,
                  self.rlbt_tiles_sprites)
            Tiles(-SCREEN_WIDTH // 3, i * SCREEN_HEIGHT // 4, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4,
                  self.tile_image_width,
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh,
                  self.rlbt_tiles_sprites)

        self.main_hero = MainHero(
            0,
            SCREEN_HEIGHT - 105,
            pygame.image.load(f"data/Sonic Sprites/tile001.png"),
            running_sonic_right_sprites,
            running_sonic_right_sphere_sprites,
            fast_running_sonic_sprites,
            super_fast_running_sonic_sprites,
            pygame.image.load(f"data/Sonic Sprites/tile051.png"),
            self.all_sprites
        )

        self.eggman = Eggman(SCREEN_WIDTH // 3 * 2, SCREEN_HEIGHT - 105, 100, 100,
                             self.all_sprites,
                             self.all_sprites_wo_mh)

        self.sonic_in_animation()

    def sonic_in_animation(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

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
                    self.quit()

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
                    self.quit()

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
                    self.quit()

            print(f"{self.eggman.y = }")
            screen.blit(self.background_image, (0, 0))
            running = self.eggman.fall_on_robot_animation()
            self.all_sprites.draw(screen)
            pygame.display.update()
        self.eggman.reset_counter()
        self.eggman.turn_game_mod()
        self.game_loop()

    def game_loop(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            running = self.movement_of_main_character() * running
            screen.blit(self.background_image, (0, 0))
            self.all_sprites.update()
            self.all_sprites.draw(screen)
            pygame.display.update()

    def movement_of_main_character(self) -> bool:
        running = True
        keys = pygame.key.get_pressed()
        if self.main_hero.is_alive() * (keys[pygame.K_SPACE] and not self.main_hero.get_is_jumping()):
            self.main_hero.play_sound_start_jump()
            self.main_hero.start_jump(self.all_tiles_sprites)
        if self.main_hero.is_alive() * (not ((keys[pygame.K_LEFT] or keys[button_settings["left"]]) and (
                keys[pygame.K_RIGHT] or keys[button_settings["right"]]))):
            if keys[pygame.K_LEFT] or keys[button_settings["left"]]:
                self.main_hero.move_left_level_boss(self.all_tiles_sprites)
            else:
                self.main_hero.set_moving_left(False)
            if keys[pygame.K_RIGHT] or keys[button_settings["right"]]:
                self.main_hero.move_right_level_boss(self.all_tiles_sprites)
            else:
                self.main_hero.set_moving_right(False)
        elif self.main_hero.is_alive():
            self.main_hero.set_moving_right(True)
            self.main_hero.set_moving_left(True)

        if self.main_hero.get_is_jumping() * self.main_hero.is_alive():
            self.main_hero.jump_level_boss(self.all_tiles_sprites)
        self.main_hero.movement_by_inertia(self.all_tiles_sprites)
        return running

    def quit(self):
        pygame.quit()
        sys.exit()
