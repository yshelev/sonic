import sys

import cv2

from MainHero import MainHero
from Tiles import Tiles
from Enemy import Enemy
from Rings import Rings
from Spikes import Spikes
from Plane_Level import *
from Settings import *
from button import Button


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("[ezrf")
        self.my_font = pygame.font.SysFont('Bauhaus 93', 30)
        self.background_image = pygame.transform.scale(pygame.image.load("data/background_greenhill.jpg"),
                                                       (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.background_image_level2 = pygame.transform.scale(pygame.image.load("data/background_sky.png"),
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
        self.rings_sprites_for_draw = [
            pygame.transform.scale(pygame.image.load(f'data/Rings spritez/Sprite-000{i}.png'), (20, 20))
            for i in range(1, 9)
        ]
        self.rings_sprites = [
            pygame.transform.scale(pygame.image.load(f'data/Rings spritez/Sprite-000{i}.png'), (100, 100))
            for i in range(1, 9)
        ]
        self.enemy_images = [pygame.transform.scale(pygame.image.load(f'data/ENEMY/BUG {i // 3}.2.png'), (1000, 1000))
                             for i in range(3, 12)
                             ]
        self.rings_sprites_count = 0

        self.plane_sprites = [pygame.image.load(f"data/Plane Sprites/plane_image{i}.png") for i in range(1, 5)]
        self.fly_sprites = [pygame.image.load(f"data/Plane Sprites/FLY_BUG{i}.png") for i in range(1, 5)]
        self.cloud_sprites = [pygame.image.load(f"data/Plane Sprites/Sprite-{i}.png") for i in range(1, 8)]
        self.rings_sprites = [
            pygame.transform.scale(pygame.image.load(f'data/Rings spritez/Sprite-000{i}.png'), (20, 20))
            for i in range(1, 9)
        ]
        self.upgrade_image = pygame.image.load(f"data/Plane Sprites/health.png")
        self.rings_sprites_count = 0

        self.last_enemy = 0
        self.last_shot = 0
        self.last_ring = 0
        self.last_cloud = 0
        self.ring_sound = pygame.mixer.Sound('data/sounds/level 2/ring_sound.mp3')
        self.boom_sound = pygame.mixer.Sound('data/sounds/level 2/boom.mp3')
        self.ot_vinta = pygame.mixer.Sound('data/MUSIC/ot_vinta.mp3')
        self.ring_sound.set_volume(0.1)
        self.boom_sound.set_volume(0.1)
        self.ot_vinta.set_volume(0.3)
        self.ot_vinta_len = 200
        self.timer = 0
        self.score = 0

        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites_level2 = pygame.sprite.Group()
        self.all_enemies_level2_sprites = pygame.sprite.Group()
        self.all_bullet_sprites = pygame.sprite.Group()
        self.all_rings_sprites = pygame.sprite.Group()
        self.all_tiles_sprites = pygame.sprite.Group()
        self.plane_characters = pygame.sprite.Group()
        self.plane_upgrade_sprites = pygame.sprite.Group()
        self.all_enemy_sprites = pygame.sprite.Group()
        self.all_sprites_wo_mh = pygame.sprite.Group()
        self.all_spikes_sprites = pygame.sprite.Group()
        for i in range(-50, 51):
            Tiles(i * 300, SCREEN_HEIGHT - 100, 300, SCREEN_HEIGHT // 3, pygame.image.load("data/GROUND/Floor.png"),
                  self.all_tiles_sprites,
                  self.all_sprites,
                  self.all_sprites_wo_mh)
            if i % 10 == 0:
                Tiles(i * 300, SCREEN_HEIGHT - 400, 100, 50, pygame.image.load("data/GROUND/Platform.png "),
                      self.all_tiles_sprites,
                      self.all_sprites,
                      self.all_sprites_wo_mh)
            if i % 20 == 0:
                Rings(i * 300 + 150, SCREEN_HEIGHT - 200, 100, 100, self.rings_sprites,
                      self.all_rings_sprites,
                      self.all_sprites,
                      self.all_sprites_wo_mh)
            if i == 0:
                Enemy(i * 300 + 150, SCREEN_HEIGHT - 200, self.enemy_images[0], self.enemy_images, self.enemy_images,
                      self.all_enemy_sprites,
                      self.all_sprites,
                      self.all_sprites_wo_mh)

        self.plane_character = Plane_Character(SCREEN_WIDTH // 2,
                                               SCREEN_HEIGHT // 2,
                                               self.plane_sprites,
                                               self.all_sprites_level2, self.plane_characters)

        self.fire_rate = 250
        self.damage = 10
        self.bullet_width = 15
        self.bullet_height = 15
        self.bullet_speed = self.plane_character.speed_x * 1.2
        self.bullet_image = 1
        self.bullet_spread = 30

        self.main_hero = MainHero(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            pygame.image.load(f"data/Sonic Sprites/tile001.png"),
            running_sonic_right_sprites,
            running_sonic_right_sphere_sprites,
            fast_running_sonic_sprites,
            self.all_sprites
        )
        self.background_image_x, self.background_image_y = SCREEN_WIDTH, 0
        self.background_image_slow = 4
        self.background_image_speed_x = 0.6
        self.start_video_loop()


    def get_font(self, size):
        return pygame.font.Font("data/menu_objects/minecraft.ttf", size)

    def play(self):
        while True:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            screen.blit(self.background_image, (0, 0))

            PLAY_TEXT = self.get_font(60).render("Выберите персонажа", True, "#b68f40")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(600, 120))
            screen.blit(PLAY_TEXT, PLAY_RECT)

            PLAY_SONIC = Button(image=pygame.image.load("data/menu_objects/options_rect.png"), pos=(600, 320),
                                text_input="Соник", font=self.get_font(70), base_color="White", hovering_color="Blue")

            PLAY_SONIC.changeColor(PLAY_MOUSE_POS)
            PLAY_SONIC.update(screen)

            PLAY_TAILS = Button(image=pygame.image.load("data/menu_objects/options_rect.png"), pos=(600, 500),
                                text_input="Тейлз", font=self.get_font(70), base_color="White", hovering_color="Orange")

            PLAY_TAILS.changeColor(PLAY_MOUSE_POS)
            PLAY_TAILS.update(screen)

            PLAY_BACK = Button(image=pygame.image.load("data/menu_objects/back_rect.png"), pos=(600, 700),
                               text_input="Назад", font=self.get_font(40), base_color="White", hovering_color="Green")

            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        self.main_menu()
                    if PLAY_SONIC.checkForInput(PLAY_MOUSE_POS):
                        self.game_loop(True)
                    if PLAY_TAILS.checkForInput(PLAY_MOUSE_POS):
                        self.game_loop_level2()

            pygame.display.update()

    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            screen.blit(self.background_image, (0, 0))

            PLAY_TEXT = self.get_font(60).render("Настройки", True, "#b68f40")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(600, 120))
            screen.blit(PLAY_TEXT, PLAY_RECT)

            OPTIONS_BACK = Button(image=pygame.image.load("data/menu_objects/back_rect.png"), pos=(600, 700),
                                  text_input="Назад", font=self.get_font(40), base_color="White",
                                  hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def main_menu(self):
        while True:
            screen.blit(self.background_image, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("Меню", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(600, 120))

            PLAY_BUTTON = Button(image=pygame.image.load("data/menu_objects/play_rect.png"), pos=(600, 270),
                                 text_input="Играть", font=self.get_font(70), base_color="#d7fcd4",
                                 hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("data/menu_objects/options_rect.png"), pos=(600, 420),
                                    text_input="Настройки", font=self.get_font(70), base_color="#d7fcd4",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("data/menu_objects/quit_rect.png"), pos=(600, 570),
                                 text_input="Выход", font=self.get_font(70), base_color="#d7fcd4",
                                 hovering_color="White")

            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def game_loop_level2(self):
        self.ot_vinta.play(-1)
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if self.plane_character.rings <= 0 or self.ot_vinta_len - self.timer == 0:
                running = False
            self.spawner()
            self.plane_actions()
            self.collide_enemy()
            self.draw_level2()
            self.check()
            self.all_sprites_level2.update()

            pygame.display.flip()

    def plane_actions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.plane_character.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.plane_character.move_down()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.plane_character.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.plane_character.move_right()
        if keys[pygame.K_SPACE]:
            self.shooting()

    def shooting(self):
        if pygame.time.get_ticks() - self.last_shot >= self.fire_rate:
            Plane_Bullet(self.plane_character.x + self.plane_character.width,
                         self.plane_character.y + self.plane_character.height / 2 + 5,
                         random.randint(-self.bullet_spread, self.bullet_spread),
                         self.damage,
                         self.bullet_width,
                         self.bullet_height,
                         self.bullet_speed,
                         pygame.image.load(f'data/Plane Sprites/bullshit_{self.bullet_image}.png'),
                         self.all_sprites_level2, self.all_bullet_sprites)
            self.last_shot = pygame.time.get_ticks()
    def start_video_loop(self) -> None:
        # video = cv2.VideoCapture("data/VIDEO/INTRO.mp4")
        # success, video_image = video.read()
        # fps = video.get(cv2.CAP_PROP_FPS)
        #
        # window = pygame.display.set_mode(video_image.shape[1::-1])
        # clock = pygame.time.Clock()
        flag = True
        # pygame.mixer.init()
        # pygame.mixer.music.load('data/MUSIC/INTRO_MUSIC.mp3')
        # pygame.mixer.music.play(-1)
        #
        # run = success
        # while run:
        #     clock.tick(fps)
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             run = False
        #             flag = False
        #
        #     success, video_image = video.read()
        #     if success:
        #         video_surf = pygame.image.frombuffer(
        #             video_image.tobytes(),
        #             video_image.shape[1::-1],
        #             "background_imageR"
        #         )
        #     else:
        #         run = False
        #     window.blit(video_surf, (0, 0))
        #     pygame.display.flip()
        #
        # pygame.mixer.music.stop()
        self.main_menu()
        # self.play_music()

    def play_music(self) -> None:
        background_music = pygame.mixer.Sound('data/MUSIC/background_image_Music.mp3')
        background_music.set_volume(0.1)
        background_music.play(-1)

    def game_loop(self, flag: bool) -> None:
        running = flag
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            running = self.movement_of_main_character() * running
            self.background_image_movement()
            self.all_sprites.update(self.all_tiles_sprites)
            self.draw()
            pygame.display.flip()

        self.quit()

    def draw_lines(self) -> None:
        pygame.draw.rect(screen, "black", (100, 479, 10, 10))
        pygame.draw.rect(screen, "black", (self.main_hero.x,
                                           self.main_hero.y - self.main_hero.speed_y / FPS,
                                           self.main_hero.width,
                                           self.main_hero.height + self.main_hero.speed_y / FPS))
        pygame.draw.rect(screen, "red", (self.main_hero.x,
                                         self.main_hero.y,
                                         self.main_hero.width,
                                         self.main_hero.height + self.main_hero.speed_y / FPS)
                         )

    def draw_num_of_rings(self) -> None:
        self.rings_sprites_count = (self.rings_sprites_count + 1) % 48
        screen.blit(self.rings_sprites_for_draw[self.rings_sprites_count // 6], (5, 5))
        text_surface = self.my_font.render(f'X{self.main_hero.get_number_of_rings()}', True, (255, 255, 255))
        screen.blit(text_surface, (20, 0))

    def quit(self) -> None:
        pygame.quit()

    def movement_of_main_character(self) -> bool:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.main_hero.get_is_jumping():
            self.main_hero.start_jump(self.all_tiles_sprites)
        if not ((keys[pygame.K_LEFT] or keys[button_settings["left"]]) and (keys[pygame.K_RIGHT] or keys[button_settings["right"]])):
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
        else:
            self.main_hero.set_moving_right(True)
            self.main_hero.set_moving_left(True)

        if self.main_hero.get_is_jumping():
            jump_speed_tiles = self.main_hero.jump(self.all_tiles_sprites)
            for tile in self.all_sprites_wo_mh:
                tile.move_y(jump_speed_tiles, self.main_hero, self.all_tiles_sprites)

        output_code_x, movement_sprites_speed_x, output_code_y, movement_sprites_speed_y =\
            self.main_hero.movement_by_inertia(self.all_tiles_sprites)
        if exit_codes["sonic_movement_x"][output_code_x] in [STOPPED_BY_RIGHT_INVISIBLE_WALL,
                                                             STOPPED_BY_LEFT_INVISIBLE_WALL]:
            for tile in self.all_sprites_wo_mh:
                tile.move_x(-movement_sprites_speed_x, self.main_hero, self.all_tiles_sprites)
        if exit_codes["sonic_movement_y"][output_code_y] in [STOPPED_BY_TOP_INVISIBLE_WALL,
                                                             STOPPED_BY_BOT_INVISIBLE_WALL]:
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
            self.main_hero.collide_enemy(enemies)
        running = True
        if not self.main_hero.is_alive():
            running = False
        for i in self.all_enemy_sprites:
            i.check(self.all_tiles_sprites)
            if i.get_is_jumping():
                i.jump(self.all_tiles_sprites)
            i.moveself_x(self.all_tiles_sprites)

        return running

    def background_image_movement(self) -> None:
        if self.main_hero.get_additional_speed() > 0:
            if (self.background_image_x - self.background_image_speed_x) > 0:
                self.background_image_x -= (self.background_image_speed_x * self.main_hero.get_additional_speed() / (
                            FPS * self.background_image_slow))
            else:
                self.background_image_x = SCREEN_WIDTH
        elif self.main_hero.get_additional_speed() < 0:
            if (self.background_image_x + self.background_image_speed_x) < SCREEN_WIDTH:
                if self.background_image_x + self.background_image_speed_x > 0:
                    self.background_image_x += (
                            self.background_image_speed_x * -self.main_hero.get_additional_speed() / (
                                FPS * self.background_image_slow))
            else:
                self.background_image_x = 0

    def draw(self) -> None:
        screen.blit(self.background_image, (self.background_image_x - SCREEN_WIDTH, 0))
        screen.blit(self.background_image, (self.background_image_x, 0))

        self.draw_num_of_rings()
        # self.draw_lines()
        self.all_sprites.draw(screen)

    def draw_timer_and_score(self):
        self.timer = pygame.time.get_ticks() // 1000
        self.minutes = (self.ot_vinta_len - self.timer) // 60
        self.seconds = self.ot_vinta_len - self.minutes * 60 - self.timer
        self.seconds = self.seconds if self.seconds >= 10 else '0' + str(self.seconds)

        text_surface = self.my_font.render(
            f'{self.minutes}:{self.seconds}',
            True, (255, 255, 255))
        screen.blit(text_surface, (SCREEN_WIDTH / 2, 10))
        text_surface = self.my_font.render(
            f'score: {self.score}',
            True, (255, 255, 255))
        screen.blit(text_surface, (30, 50))

    def draw_rings_level2(self):
        self.rings_sprites_count += 1
        screen.blit(pygame.transform.scale(self.rings_sprites[self.rings_sprites_count // 2 % 8], (32, 32)), (5, 5))
        text_surface = self.my_font.render(f'X{self.plane_character.rings}', True, (255, 255, 255))
        screen.blit(text_surface, (40, 10))

    def draw_level2(self):
        if self.background_image_x >= 0:
            self.background_image_x -= 3
        else:
            self.background_image_x = SCREEN_WIDTH
        screen.blit(self.background_image_level2, (self.background_image_x - SCREEN_WIDTH, 0))
        screen.blit(self.background_image_level2, (self.background_image_x, 0))
        self.all_sprites_level2.draw(screen)
        self.draw_rings_level2()
        self.draw_timer_and_score()

    def spawner(self):
        if pygame.time.get_ticks() - self.last_enemy >= 500:
            Plane_Enemy(self.fly_sprites, self.all_sprites_level2, self.all_enemies_level2_sprites)
            self.last_enemy = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_ring >= 3000:
            self.j = random.randint(0, SCREEN_HEIGHT - 64)
            [Plane_Rings(i * 70, self.j, self.rings_sprites, self.all_sprites_level2, self.all_rings_sprites) for i in
             range(random.randint(3, 7))]
            self.last_ring = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_cloud >= 5000:
            Plane_Cloud(self.cloud_sprites, self.all_sprites_level2, self.all_enemies_level2_sprites)
            self.last_cloud = pygame.time.get_ticks()
        if self.ot_vinta_len - self.timer == 195 and not self.plane_upgrade_sprites:
            Plane_Upgrates(1, self.upgrade_image, self.all_sprites_level2,
                           self.plane_upgrade_sprites)
        if self.ot_vinta_len - self.timer == 150 and not self.plane_upgrade_sprites:
            Plane_Upgrates(2, self.upgrade_image, self.all_sprites_level2,
                           self.plane_upgrade_sprites)

    def check(self):
        for enemy in self.all_enemies_level2_sprites:
            if enemy.health <= 0 or enemy.x + enemy.width < 0:
                if enemy.health <= 0:
                    self.score += 200
                    self.boom_sound.play()
                enemy.kill()
        for bullet in self.all_bullet_sprites:
            if bullet.x > SCREEN_WIDTH + bullet.width:
                bullet.kill()
            if pygame.sprite.spritecollideany(bullet, self.all_enemies_level2_sprites):
                enemy = pygame.sprite.spritecollideany(bullet, self.all_enemies_level2_sprites)
                bullet.kill()
                enemy.health -= bullet.damage
        for ring in self.all_rings_sprites:
            if ring.x + ring.width < 0:
                ring.kill()
            if pygame.sprite.spritecollideany(ring, self.plane_characters):
                self.ring_sound.play()
                self.score += 100
                self.plane_character.rings += 1
                ring.kill()
        for upgrade in self.plane_upgrade_sprites:
            if upgrade.x + upgrade.width < 0:
                upgrade.kill()
            if pygame.sprite.spritecollideany(upgrade, self.plane_characters):
                if upgrade.type == 1:
                    self.score += 200
                    self.ring_sound.play()
                    self.bullet_speed = self.plane_character.speed_x * 1.5
                    self.fire_rate = 100
                    self.bullet_width = 20
                    self.bullet_height = 20
                    self.bullet_image = 2
                    upgrade.kill()
                else:
                    self.score += 200
                    self.ring_sound.play()
                    self.bullet_speed = self.plane_character.speed_x * 1.4
                    self.fire_rate = 50
                    self.bullet_width = 10
                    self.bullet_height = 10
                    self.bullet_image = 1
                    self.damage = 4
                    self.bullet_spread = 100
                    upgrade.kill()

    def collide_enemy(self):
        if pygame.sprite.spritecollideany(self.plane_character, self.all_enemies_level2_sprites):
            enemy = pygame.sprite.spritecollideany(self.plane_character, self.all_enemies_level2_sprites)
            if enemy.__class__.__name__ == "Plane_Enemy":
                self.score -= 50
                self.boom_sound.play()
                enemy.kill()
                self.plane_character.rings -= 6
            else:
                self.plane_character.rings = self.plane_character.rings // 2 + 1
