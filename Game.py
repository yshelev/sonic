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
        self.rings_sprites = [
            pygame.transform.scale(pygame.image.load(f'data/Rings spritez/Sprite-000{i}.png'), (20, 20))
            for i in range(1, 9)
        ]
        self.rings_sprites_count = 0

        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_tiles_sprites = pygame.sprite.Group()
        Tiles(800, SCREEN_HEIGHT // 2, 300, 100, pygame.image.load("data/GROUND/Platform.png"), self.all_tiles_sprites,
              self.all_sprites)
        Tiles(100, SCREEN_HEIGHT // 2, 300, 100, pygame.image.load("data/GROUND/Platform.png"), self.all_tiles_sprites,
              self.all_sprites)
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
        self.background_image_speed_x = 0.6
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

            self.movement_of_main_character()
            self.background_image_movement()
            self.all_sprites.update()
            self.draw()
            pygame.display.flip()

        self.quit()

    def draw_lines(self):
        pygame.draw.line(screen, "green", LEFT_INVISIBLE_LINE[0], LEFT_INVISIBLE_LINE[1], 10)
        pygame.draw.line(screen, "green", RIGHT_INVISIBLE_LINE[0], RIGHT_INVISIBLE_LINE[1], 10)
        pygame.draw.line(screen, "green", TOP_INVISIBLE_LINE[0], TOP_INVISIBLE_LINE[1], 10)
        pygame.draw.line(screen, "green", BOTTOM_INVISIBLE_LINE[0], BOTTOM_INVISIBLE_LINE[1], 10)
        pygame.draw.rect(screen, "black", (self.main_hero.rect.x - (self.main_hero.speed_x - self.main_hero.additional_speed) / FPS, self.main_hero.rect.y, self.main_hero.width + (self.main_hero.speed_x - self.main_hero.additional_speed) / FPS, self.main_hero.rect.height))
        # pygame.draw.rect(screen, "red", (self.main_hero.rect.x, self.main_hero.rect.y, self.main_hero.width + (self.main_hero.speed_x + self.main_hero.additional_speed) / FPS, self.main_hero.rect.height))


    def draw_num_of_rings(self) -> None:
        self.rings_sprites_count += 1
        screen.blit(self.rings_sprites[self.rings_sprites_count // 6 % 8], (5, 5))
        text_surface = self.my_font.render(f'X{self.main_hero.get_number_of_rings()}', True, (255, 255, 255))
        screen.blit(text_surface, (20, 0))

    def quit(self) -> None:
        pygame.quit()

    def movement_of_main_character(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.main_hero.get_is_jumping():
            self.main_hero.start_jump()
        if not ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d])):
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                output_code, movement_sprites_speed = self.main_hero.move_left(self.all_tiles_sprites)
                if output_code == OK:
                    pass
                elif output_code in [STOPPED_BY_RIGHT_INVISIBLE_WALL, STOPPED_BY_LEFT_INVISIBLE_WALL]:
                    for tile in self.all_tiles_sprites:
                        tile.move_x(movement_sprites_speed, self.main_hero)
            else:
                self.main_hero.set_moving_left(False)

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                output_code, movement_sprites_speed = self.main_hero.move_right(self.all_tiles_sprites)
                if output_code in [STOPPED_BY_RIGHT_INVISIBLE_WALL, STOPPED_BY_LEFT_INVISIBLE_WALL]:
                    for tile in self.all_tiles_sprites:
                        tile.move_x(-movement_sprites_speed, self.main_hero)
            else:
                self.main_hero.set_moving_right(False)
        else:
            self.main_hero.set_moving_right(True)
            self.main_hero.set_moving_left(True)

        if self.main_hero.get_is_jumping():
            self.main_hero.jump()

        output_code, movement_sprites_speed = self.main_hero.movement_by_inertia(self.all_tiles_sprites)
        if exit_codes["sonic_movement"][output_code] in [STOPPED_BY_RIGHT_INVISIBLE_WALL,
                                                         STOPPED_BY_LEFT_INVISIBLE_WALL]:
            if self.main_hero.get_additional_speed() > 0:
                for tile in self.all_tiles_sprites:
                    tile.move_x(-movement_sprites_speed, self.main_hero)
            else:
                for tile in self.all_tiles_sprites:
                    tile.move_x(-movement_sprites_speed, self.main_hero)

    def background_image_movement(self):
        if self.main_hero.get_additional_speed() > 0:
            if (self.background_image_x - self.background_image_speed_x) > 0:
                self.background_image_x -= (self.background_image_speed_x * self.main_hero.get_additional_speed() / FPS)
            else:
                self.background_image_x = SCREEN_WIDTH
        elif self.main_hero.get_additional_speed() < 0:
            if (self.background_image_x + self.background_image_speed_x) < SCREEN_WIDTH:
                if self.background_image_x + self.background_image_speed_x > 0:
                    self.background_image_x += (
                            self.background_image_speed_x * -self.main_hero.get_additional_speed() / FPS)
            else:
                self.background_image_x = 0

    def draw(self):
        screen.blit(self.background_image, (self.background_image_x - SCREEN_WIDTH, 0))
        screen.blit(self.background_image, (self.background_image_x, 0))

        self.draw_num_of_rings()
        self.draw_lines()
        self.all_sprites.draw(screen)
