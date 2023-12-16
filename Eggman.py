import random
import math
import pygame

from Bullet import Bullet
from MainHero import MainHero
from Settings import *


class Eggman(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, *sprite_group):
        super().__init__(*sprite_group)

        self.shot_cooldown = 0
        self.x = x
        self.y = y
        self.alive = False

        self.bullet_sprite = pygame.transform.scale(pygame.image.load("data/Plane Sprites/bullshit_2.png"), (30, 30))

        self.current_stage = 0
        self.counter = 0
        self.fly_counter = 0

        self.stages = {
            "run",
            "robot"
        }

        self.robot_width = width * 1.5
        self.start_robot_height = height * 2
        self.robot_height = height * 1.5
        self.man_width = width
        self.man_height = height

        self.width, self.height = self.man_width, self.man_height

        self.speed_y_multiplier = 10
        self.speed_y = 300
        self.speed_x_multiplier = 10
        self.speed_x = 300

        self.hp = 1000

        self.types = {
            "robot_dies": list(map(lambda x: pygame.transform.scale(x, (self.robot_width, self.start_robot_height)),
                                   [pygame.image.load(f"data/eggman/robot/eggman_robot_dies_{i // 3}.png") for
                                    i in range(3, 9)])),
            "robot_shoot_right": list(map(lambda x: pygame.transform.scale(x, (self.robot_width, self.start_robot_height)),
                                   [pygame.image.load(f"data/eggman/robot/eggman_robot_hit_{2}.png")
                                    ])),
            "robot_shoot_left": list(map(lambda x: pygame.transform.flip(x, True, False), list(map(lambda x: pygame.transform.scale(x, (self.robot_width, self.robot_height)),
                                   [pygame.image.load(f"data/eggman/robot/eggman_robot_hit_{2}.png")
                                    ])))),
            "robot_fly_right": list(
                map(lambda x: pygame.transform.scale(x, (self.robot_width, self.start_robot_height)),
                    [pygame.image.load(f"data/eggman/robot/eggman_robot_fly_{i // 3}.png") for
                     i in range(3, 9)])),
            "robot_fly_left": list(map(lambda x: pygame.transform.flip(x, True, False),
                                       list(map(lambda x: pygame.transform.scale(x, (
                                           self.robot_width, self.start_robot_height)),
                                                [pygame.image.load(f"data/eggman/robot/eggman_robot_fly_{i // 3}.png")
                                                 for
                                                 i in range(3, 9)])))),

            "robot_animation": list(map(lambda x: pygame.transform.flip(x, True, False),
                                        list(map(lambda x: pygame.transform.scale(x, (
                                            self.robot_width, self.start_robot_height)),
                                                 [pygame.image.load(
                                                     f"data/eggman/robot/eggman_robot_transform_{i // 3}.png") for
                                                     i in range(3, 15)])))),
            "man_run": list(map(lambda x: pygame.transform.scale(x, (self.man_width, self.man_height)),
                                [pygame.image.load(f"data/eggman/run/eggman_run_{i // 3}.png") for i in range(3, 15)])),
            "man_jump": list(map(lambda x: pygame.transform.scale(x, (self.man_width, self.man_height)),
                                 [pygame.image.load(f"data/eggman/eggman_zloy/eggman_jump_{i // 3}.png") for i in
                                  range(3, 12)][::-1]))
        }

        self.image = self.start_image = self.types["man_jump"][0]

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def eggman_movement(self, sonic: MainHero):
        self.x += (sonic.rect.x - self.rect.x) / self.speed_x_multiplier / FPS
        self.y += (sonic.rect.y - self.rect.y) / self.speed_y_multiplier / FPS

        self.speed_x_multiplier = max(self.speed_x_multiplier - 0.01, 5)

        self.speed_y_multiplier = max(self.speed_y_multiplier - 0.01, 5)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def turn_game_mod(self):
        self.width = self.robot_width
        self.height = self.robot_height

        self.current_stage = 1

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def turn_robot(self):
        self.width = self.robot_width
        self.height = self.start_robot_height
        self.x = SCREEN_WIDTH - self.width * 2
        self.y = -self.height
        self.current_stage = 1

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def man_run_out(self):
        self.man_run_animation()
        self.x += self.speed_x / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return self.x <= SCREEN_WIDTH

    def fall_on_robot_animation(self):
        self.image = self.types["robot_animation"][0]
        output = True
        if self.y + self.height + self.speed_y / FPS < SCREEN_HEIGHT:
            self.y += self.speed_y / FPS
        else:
            self.y = SCREEN_HEIGHT - self.height - 5
            output = self.turn_into_flying_robot_animation()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        return output

    def flying_animation(self):
        self.fly_counter = (self.fly_counter + 0.5) % len(self.types["robot_fly"])
        self.image = self.types["robot_fly"][int(self.counter) % len(self.types["robot_animation"])]

    def man_run_animation(self):
        self.counter += 0.5
        self.image = self.types["man_run"][int(self.counter) % len(self.types["man_run"])]
        return True

    def man_jump_animation(self):
        self.counter += 0.5
        self.image = self.types["man_jump"][int(self.counter) % len(self.types["man_jump"])]
        return self.counter <= 52

    def turn_into_flying_robot_animation(self):
        self.counter += 0.5
        self.image = self.types["robot_animation"][int(self.counter) % len(self.types["robot_animation"])]
        return self.counter <= 10

    def reset_counter(self):
        self.counter = 0

    def update(self, *args, **kwargs):
        self.shot_cooldown -= 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fly_counter = (self.fly_counter + 0.1) % len(self.types["robot_fly_left"])
        self.image = self.types["robot_fly_left" if args[0] else "robot_fly_right"][int(self.fly_counter)] if self.shot_cooldown > 20 else self.types["robot_shoot_left" if args[0] else "robot_shoot_right"][0]

    def shoot(self, *groups):
        self.shot_cooldown = 600
        start_x, start_y = self.x + self.width // 2, self.y + self.height // 2
        shoot_length = SCREEN_WIDTH
        for i in range(8):
            pygame.draw.line(screen, (0, 0, 0), (start_x, start_y), (start_x + shoot_length * math.cos(i * math.pi / 4), start_y + shoot_length * math.sin(i * math.pi / 4)), 20)
            Bullet(start_x, start_y, start_x + shoot_length * math.cos(i * math.pi / 4), start_y + shoot_length * math.sin(i * math.pi / 4), self.bullet_sprite, 1, *groups)

    def collide_sonic(self, sonic: MainHero):
        if self.y < sonic.y:
            sonic.get_damage()
            return False
        else:
            self.get_damage(sonic.speed_y)
            return True

    def get_damage(self, sonic_speed_y):
        self.hp -= abs(int(sonic_speed_y)) / FPS
        if self.hp < 0:
            self.alive = False
            self.kill()

    def can_shoot(self):
        return self.shot_cooldown <= 0
