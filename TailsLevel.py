import random
import sys
import pygame

from Plane_Level import *
from Settings import *
from button import *
from Menu import *


class TailsLevel:
    def __init__(self):

        self.my_font = pygame.font.SysFont('Bauhaus 93', 30)
        self.background_image = pygame.transform.scale(pygame.image.load("data/background_greenhill.jpg"),
                                                       (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.background_image_level2 = pygame.transform.scale(pygame.image.load("data/background_sky.png"),
                                                              (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.enemy_images = [pygame.transform.scale(pygame.image.load(f'data/ENEMY/BUG {i // 3}.2.png'), (1000, 1000))
                             for i in range(3, 12)
                             ]
        self.rings_sprites_count = 0

        self.plane_sprites = [pygame.image.load(f"data/Plane Sprites/plane_image{i}.png") for i in range(1, 5)]
        self.fly_sprites = [pygame.image.load(f"data/Plane Sprites/FLY_BUG{i}.png") for i in range(1, 5)]
        self.cloud_sprites = [pygame.image.load(f"data/Plane Sprites/Sprite-{i}.png") for i in range(1, 8)]
        self.sad_cloud_sprites = [pygame.image.load(f"data/Plane Sprites/Cloud({i}).png") for i in range(1, 7)]
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
        self.zap_sound = pygame.mixer.Sound('data/sounds/level 2/zap.wav')
        self.bonus_sound = pygame.mixer.Sound('data/sounds/level 2/bonus.wav')
        self.ot_vinta = pygame.mixer.Sound('data/MUSIC/ot_vinta.mp3')
        self.ring_sound.set_volume(0.1)
        self.boom_sound.set_volume(0.1)
        self.zap_sound.set_volume(0.1)
        self.bonus_sound.set_volume(0.1)
        self.ot_vinta.set_volume(0.3)
        self.ot_vinta_len = 200
        self.start_time = 0
        self.current_time = 0
        self.timer = 0
        self.score = 0
        self.win = False

        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites_level2 = pygame.sprite.Group()
        self.all_enemies_level2_sprites = pygame.sprite.Group()
        self.all_bullet_sprites = pygame.sprite.Group()
        self.all_rings_sprites = pygame.sprite.Group()
        self.plane_characters = pygame.sprite.Group()
        self.plane_upgrade_sprites = pygame.sprite.Group()
        self.all_enemy_sprites = pygame.sprite.Group()

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

        self.background_image_x = 0

        self.output = self.game_loop()

    def game_loop(self):
        self.ot_vinta.play(-1)
        self.start_time = pygame.time.get_ticks()
        flag = True
        running = True
        while running:
            self.current_time = pygame.time.get_ticks()
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    flag = False
                    running = False
                    self.quit()
            if self.plane_character.rings <= 0 or self.ot_vinta_len - self.timer == 0:
                if self.ot_vinta_len - self.timer == 0:
                    self.win = True
                running = False
                self.ot_vinta.stop()
                self.end_screen()
            self.spawner()
            self.plane_actions()
            self.collide_enemy()
            self.draw_level2()
            self.check()
            self.all_sprites_level2.update()

            pygame.display.flip()
        return flag

    def end_screen(self):
        running = True
        while running:
            if self.win == True:
                bg = pygame.transform.scale(pygame.image.load("data/tails_winner.jpg"),
                                                       (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(bg, (1, 1))
                text_surface = pygame.font.Font("data/menu_objects/menu_font.ttf", 50).render(
                    f'ХОРОШ',
                    True, (255, 255, 255))
                screen.blit(text_surface, (400, 100))
            else:
                bg = pygame.transform.scale(pygame.image.load("data/tails_loser.jpg"),
                                            (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(bg, (1, 1))

            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            RETRY = Button(image=pygame.image.load("data/menu_objects/character_rect.png"),
                           pos=(SCREEN_WIDTH // 1.2, 650),
                           text_input="ЗАНОВО", font=self.get_font(50), base_color="White", hovering_color="Orange")

            RETRY.changeColor(pygame.mouse.get_pos())
            RETRY.update(screen)

            RETURN_TO_MAIN_MENU = Button(image=pygame.image.load("data/menu_objects/character_rect.png"),
                                         pos=(SCREEN_WIDTH // 1.2, 750),
                                         text_input="В МЕНЮ", font=self.get_font(50), base_color="White",
                                         hovering_color="Orange")

            RETURN_TO_MAIN_MENU.changeColor(pygame.mouse.get_pos())
            RETURN_TO_MAIN_MENU.update(screen)

            text_surface = pygame.font.Font("data/menu_objects/menu_font.ttf", 50).render(
                f'ОЧКИ: {self.score}',
                True, (0, 0, 0))
            screen.blit(text_surface, (20, 100))





            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETRY.checkForInput(PLAY_MOUSE_POS):
                        running = False
                        TailsLevel()
                    if RETURN_TO_MAIN_MENU.checkForInput(PLAY_MOUSE_POS):
                        running = False
            pygame.display.update()

    def get_font(self, size):
        return pygame.font.Font("data/menu_objects/menu_font.ttf", size)

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

    def play_music(self) -> None:
        background_music = pygame.mixer.Sound('data/MUSIC/background_image_Music.mp3')
        background_music.set_volume(0.1)
        background_music.play(-1)

    def draw_timer_and_score(self):
        self.timer = (self.current_time - self.start_time) // 1000
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
            [Plane_Rings(i * 70, self.j, self.rings_sprites, self.all_sprites_level2, self.all_rings_sprites) for i
             in
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
                    self.bonus_sound.play()
                    self.bullet_speed = self.plane_character.speed_x * 1.5
                    self.fire_rate = 100
                    self.bullet_width = 20
                    self.bullet_height = 20
                    self.bullet_image = 2
                    upgrade.kill()
                else:
                    self.score += 200
                    self.bonus_sound.play()
                    self.bullet_speed = self.plane_character.speed_x * 1.4
                    self.fire_rate = 50
                    self.bullet_width = 10
                    self.bullet_height = 10
                    self.bullet_image = 1
                    self.damage = 6
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
                if enemy.damage:
                    self.plane_character.rings -= enemy.damage
                    self.score -= 50
                    self.zap_sound.play()
                    enemy.damage = 0
                    enemy.images = list(
                        map(lambda image: pygame.transform.scale(image, (enemy.width, enemy.height)),
                            self.sad_cloud_sprites))

    def quit(self):
        pygame.quit()
        sys.exit()

    def get_output(self) -> bool:
        return self.output
