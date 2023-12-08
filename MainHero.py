from typing import Tuple, Type

from Character import Character
from Settings import *
import pygame


class MainHero(Character):
    def __init__(
            self,
            x: int,
            y: int,
            start_image: pygame.image,
            images: list[pygame.image],
            jump_images: list[pygame.image],
            fast_images: list[pygame.image],
            group_all_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(x, y, start_image, images, jump_images, group_all_sprite)
        self.fast_right_frames = list(map(lambda image: pygame.transform.scale(image, (self.width, self.height)),
                                          fast_images))

        self.fast_left_frames = list(map(lambda image: pygame.transform.flip(image, True, False),
                                         self.fast_right_frames))
        self.cur_fast_frame = 0
        self.additional_speed = 0
        self.boost = 300
        self.stop_boost = self.boost * 3
        self.number_of_rings = 50
        self.is_falling = False
        self.jump_sound = pygame.mixer.Sound('data/sounds/sonic/jump.mp3')
        self.enemy_death_sound = pygame.mixer.Sound('data/sounds/sonic/ring_collect.mp3')

    def move_left(self, tiles) -> (int, float):
        can_move_left, can_move_right, _ = self.can_move_x(tiles)
        can_move_invisible_left, can_move_invisible_right = self.can_move_invisible_wall_x()
        self.moving_left = True
        self.additional_speed -= self.boost / FPS

        move_code = self.get_move_x_code(can_move_left, can_move_right, can_move_invisible_left, can_move_invisible_right)

        ec = exit_codes["sonic_movement_x"][move_code]
        direction = self.move_direction()[0]
        if ec == OK:
            self.x -= (self.speed_x - self.additional_speed) / FPS
        elif ec != STOPPED_BY_LEFT_INVISIBLE_WALL:
            self.x -= (self.speed_x - self.additional_speed) / FPS * can_move_left * (direction in [STAY, LEFT])
        if ec == STOPPED_BY_LEFT_WALL_OUTSIDE:
            self.additional_speed = 0
        if direction == RIGHT:
            self.additional_speed = max(self.additional_speed - self.stop_boost / FPS, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return exit_codes["sonic_movement_x"][move_code], self.speed_x - self.additional_speed

    def move_right(self, tiles: pygame.sprite.Group) -> (int, float):
        """
        """
        can_move_left, can_move_right, point_x = self.can_move_x(tiles)
        can_move_invisible_left, can_move_invisible_right = self.can_move_invisible_wall_x()
        self.moving_right = True
        self.additional_speed += self.boost / FPS

        move_code = self.get_move_x_code(can_move_left, can_move_right, can_move_invisible_left, can_move_invisible_right)

        ec = exit_codes["sonic_movement_x"][move_code]
        direction = self.move_direction()[0]
        if ec == OK:
            self.x += (self.speed_x + self.additional_speed) / FPS
        elif ec != STOPPED_BY_RIGHT_INVISIBLE_WALL:
            self.x += (self.speed_x + self.additional_speed) / FPS * can_move_right * (direction in [RIGHT, STAY])
        if ec == STOPPED_BY_RIGHT_WALL_OUTSIDE:
            self.additional_speed = 0
        if direction == LEFT:
            self.additional_speed = min(self.additional_speed + self.stop_boost / FPS, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return exit_codes["sonic_movement_x"][move_code], self.speed_x + self.additional_speed

    def movement_by_inertia(self, tiles) -> (int, float):
        """
        инерция(тормозит быстро)
        """
        can_move_bottom, can_move_top, point_y = self.can_move_y(tiles)
        can_move_left, can_move_right, point_x = self.can_move_x(tiles)
        can_move_invisible_left, can_move_invisible_right = self.can_move_invisible_wall_x()
        can_move_invisible_bottom, can_move_invisible_top = self.can_move_invisible_wall_y()
        direction_x = self.move_direction()[0]

        if not (self.moving_right or self.moving_left) or (self.moving_right and self.moving_left):
            move_code_x = self.get_move_x_code(can_move_left, can_move_right, can_move_invisible_left,
                                               can_move_invisible_right)

            if can_move_right and self.additional_speed > 0:
                if can_move_invisible_right:
                    self.x += self.additional_speed / FPS
            elif can_move_left and self.additional_speed < 0:
                if can_move_invisible_left:
                    self.x += self.additional_speed / FPS
            else:
                self.additional_speed = 0
            if direction_x == RIGHT:
                self.additional_speed = max(self.additional_speed - self.stop_boost / FPS, 0)
            elif direction_x == LEFT:
                self.additional_speed = min(self.additional_speed + self.stop_boost / FPS, 0)
            if not self.is_jumping and abs(self.additional_speed) / FPS < 5:
                self.image = self.start_image
                self.cur_fast_frame = 0
            if not self.is_jumping:
                if direction_x == LEFT:
                    self.image = self.fast_left_frames[self.cur_fast_frame]
                elif direction_x == RIGHT:
                    self.image = self.fast_left_frames[self.cur_fast_frame]
        else:
            move_code_x = exit_codes["sonic_movement_x"].index(MOVING)

        move_code_y = self.get_move_y_code(can_move_top, can_move_bottom, can_move_invisible_top, can_move_invisible_bottom)

        mc = exit_codes["sonic_movement_y"][move_code_y]

        if mc != STOPPED_BY_BOT_WALL_OUTSIDE:
            self.jump(tiles)

        return move_code_x, self.additional_speed, move_code_y, self.speed_y if not self.is_jumping else 0

    def start_jump(self, tiles_sprites) -> None:
        super().start_jump(tiles_sprites)
        self.play_sound_start_jump()

    def play_sound_start_jump(self) -> None:
        self.jump_sound.set_volume(0.1)
        self.jump_sound.play(-1)


    def jump(self, tiles_sprites: pygame.sprite.Group) -> int:
        self.is_jumping = True
        self.speed_y += GRAVITY / FPS
        can_move_bottom, can_move_top, point_y = self.can_move_y(tiles_sprites)
        can_invisible_move_bottom, can_invisible_move_top = self.can_move_invisible_wall_y()
        output = 0
        direction = self.move_direction()[1]
        if direction in [BOT, STAY]:
            if can_move_bottom:
                if (can_invisible_move_top * (direction in [TOP, STAY]) + can_invisible_move_bottom * (
                        direction in [BOT, STAY])) >= 1:
                    self.y += self.speed_y / FPS
                else:
                    output = self.speed_y
            else:
                self.y = point_y[0] if point_y else self.y
                self.speed_y = 0
                self.is_jumping = False
                self.is_falling = False
        else:
            if (can_invisible_move_top * (direction in [TOP, STAY]) + can_invisible_move_bottom * (
                    direction in [BOT, STAY])) >= 1:
                self.y += self.speed_y / FPS
            else:
                output = self.speed_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return output

    def drawing(self) -> None:
        if self.is_jumping:
            if self.moving_left:
                self.image = self.left_jump_frames[self.cur_frame_jump]
            else:
                self.image = self.right_jump_frames[self.cur_frame_jump]
        elif not self.is_falling:
            if self.speed_y == 0:
                self.cur_frame_jump = 0
            if self.moving_right and self.moving_left:
                self.image = self.start_image
            elif self.moving_left:
                if abs(self.additional_speed) / FPS > 7.5:
                    self.image = self.fast_left_frames[self.cur_fast_frame]
                else:
                    self.image = self.left_frames[self.cur_frame]
                    self.start_image = self.start_image_left
            elif self.moving_right:
                if abs(self.additional_speed) / FPS > 7.5:
                    if abs(self.additional_speed) / FPS == 20:
                        self.image = self.super_fast_right_frames
                    else:
                        self.image = self.fast_right_frames[self.cur_fast_frame]
                else:
                    self.image = self.right_frames[self.cur_frame]
                    self.start_image = self.start_image_right
            else:
                self.image = self.start_image
        else:
            self.image = self.start_image

    def update_counters(self) -> None:
        self.cur_frame = (self.cur_frame + 1) % len(self.left_frames)
        self.cur_fast_frame = (self.cur_fast_frame + 1 * (abs(self.additional_speed) > 7.5)) % len(
            self.fast_left_frames)
        if self.speed_y != 0:
            self.cur_frame_jump = min(self.cur_frame_jump + 1 * self.is_jumping, len(self.left_jump_frames) - 1)

    def can_move_y(self, tiles_sprites: pygame.sprite.Group) -> (bool, bool, list[int]):
        return not any(pygame.rect.Rect(
            self.x, self.y, self.width,
            self.height + (GRAVITY + self.speed_y) / FPS
        ).colliderect(i) for i in filter(lambda i: i.rect.y > self.rect.y, tiles_sprites)), not any(pygame.rect.Rect(
            self.x, self.y - (self.speed_y + GRAVITY) / FPS, self.width,
                    self.height + (self.speed_y + GRAVITY) / FPS
        ).colliderect(i) for i in filter(lambda i: i.rect.y < self.rect.y, tiles_sprites)), [i.rect.y - self.rect.w - 2 for
                                                                                             i
                                                                                             in filter(
                lambda i: i.rect.y > self.rect.y, tiles_sprites) if pygame.rect.Rect(
                self.x, self.y, self.width,
                self.height + (GRAVITY + self.speed_y) / FPS
            ).colliderect(i)]

    def can_move_invisible_wall_y(self) -> (bool, bool):
        return (not pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height + self.speed_y / FPS
        ).colliderect(pygame.Rect(
            BOTTOM_INVISIBLE_LINE[0][0],
            BOTTOM_INVISIBLE_LINE[0][1],
            BOTTOM_INVISIBLE_LINE[1][0] - BOTTOM_INVISIBLE_LINE[0][0],
            5
        )), not pygame.Rect(
            self.x,
            self.y - self.speed_y / FPS,
            self.width,
            self.height + self.speed_y / FPS
        ).colliderect(pygame.Rect(
            TOP_INVISIBLE_LINE[0][0],
            TOP_INVISIBLE_LINE[0][1],
            TOP_INVISIBLE_LINE[1][0] - TOP_INVISIBLE_LINE[0][0],
            5)))

    def can_move_invisible_wall_x(self) -> (bool, bool):
        return (
            not pygame.rect.Rect(self.rect.x - (self.speed_x - self.additional_speed) / FPS, self.rect.y,
                                 self.width + (self.speed_x - self.additional_speed) / FPS,
                                 self.rect.height).colliderect(pygame.Rect(
                LEFT_INVISIBLE_LINE[0][0],
                LEFT_INVISIBLE_LINE[0][1],
                5,
                LEFT_INVISIBLE_LINE[1][1] - LEFT_INVISIBLE_LINE[0][1])),
            not pygame.rect.Rect(self.rect.x, self.rect.y, self.width + (self.speed_x + self.additional_speed) / FPS,
                                 self.rect.height).colliderect(pygame.Rect(
                RIGHT_INVISIBLE_LINE[0][0],
                RIGHT_INVISIBLE_LINE[0][1],
                5,
                RIGHT_INVISIBLE_LINE[1][1] - RIGHT_INVISIBLE_LINE[0][1]))
        )

    def can_move_x(self, tiles_sprites: pygame.sprite.Group) -> (bool, bool, list):
        direction = self.move_direction()[0]
        return (not (any(
            pygame.rect.Rect(self.rect.x - (self.speed_x - self.additional_speed) / FPS,
                             self.rect.y,
                             self.width + (self.speed_x - self.additional_speed) / FPS,
                             self.rect.height).colliderect(i.rect) * (direction in [LEFT, STAY])
            for i in filter(lambda i: i.rect.x < self.rect.x, tiles_sprites))),
                not (any(
                    pygame.rect.Rect(self.rect.x + (self.speed_x + self.additional_speed) / FPS,
                                     self.rect.y,
                                     self.width,
                                     self.rect.height).colliderect(i.rect) * (direction in [RIGHT, STAY])
                    for i in filter(lambda i: i.rect.x > self.rect.x, tiles_sprites))),
                [min(i.rect.x - self.rect.w - 1,
                     RIGHT_INVISIBLE_LINE[0][0] - 1) if i.rect.x + i.rect.w > self.rect.x else max(
                    i.rect.x + i.rect.w + 1,
                    LEFT_INVISIBLE_LINE[0][0] + 1) if self.rect.x + self.rect.w > i.rect.x else None for i in
                 tiles_sprites if
                 pygame.rect.Rect(self.rect.x, self.rect.y,
                                  self.width + (self.speed_x + self.additional_speed) / FPS,
                                  self.rect.height).colliderect(i.rect) or
                 pygame.rect.Rect(self.rect.x - (self.speed_x - self.additional_speed) / FPS, self.rect.y,
                                  self.width + (self.speed_x - self.additional_speed) / FPS,
                                  self.rect.height).colliderect(i.rect)
                 ])

    def move_direction(self) -> (str, str):
        return (LEFT if self.additional_speed < 0 else RIGHT if self.additional_speed > 0 else STAY,
                TOP if self.speed_y < 0 else BOT if self.speed_y > 0 else STAY)

    def set_is_jumping(
            self,
            is_jumping: bool
    ) -> None:
        self.is_jumping = is_jumping

    def get_additional_speed(self) -> int:
        return self.additional_speed

    def get_number_of_rings(self) -> int:
        return self.number_of_rings

    def set_y(self, y):
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def reset_speed(self) -> None:
        self.additional_speed = 0

    def update(self, *args, **kwargs) -> None:
        self.update_counters()
        self.drawing()
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def get_move_x_code(self,
                        ml: bool,
                        mr: bool,
                        iml: bool,
                        imr: bool
                        ) -> int:
        if not mr:
            move_code = exit_codes["sonic_movement_x"].index(STOPPED_BY_RIGHT_WALL_OUTSIDE)
        elif not ml:
            move_code = exit_codes["sonic_movement_x"].index(STOPPED_BY_LEFT_WALL_OUTSIDE)
        elif not iml:
            move_code = exit_codes["sonic_movement_x"].index(STOPPED_BY_LEFT_INVISIBLE_WALL)
        elif not imr:
            move_code = exit_codes["sonic_movement_x"].index(STOPPED_BY_RIGHT_INVISIBLE_WALL)
        else:
            move_code = exit_codes["sonic_movement_x"].index(OK)
        return move_code

    def get_move_y_code(self,
                        mt: bool,
                        mb: bool,
                        imt: bool,
                        imb: bool
                        ) -> int:
        if not mt:
            move_code = exit_codes["sonic_movement_y"].index(STOPPED_BY_TOP_WALL_OUTSIDE)
        elif not mb:
            move_code = exit_codes["sonic_movement_y"].index(STOPPED_BY_BOT_WALL_OUTSIDE)
        elif not imt:
            move_code = exit_codes["sonic_movement_y"].index(STOPPED_BY_TOP_INVISIBLE_WALL)
        elif not imb:
            move_code = exit_codes["sonic_movement_y"].index(STOPPED_BY_BOT_INVISIBLE_WALL)
        else:
            move_code = exit_codes["sonic_movement_y"].index(OK)
        return move_code

    def get_damage(self):
        self.number_of_rings -= 10
        if self.number_of_rings <= 0:
            self.kill()

    def add_rings(self):
        self.play_collect_ring()
        self.number_of_rings += 1

    def is_alive(self):
        return self.number_of_rings > 0

    def collide_enemy(self, enemies):
        if self.speed_y > 0:
            enemies.kill()
            return True
        else:
            self.get_damage()
            return False

    def play_collect_ring(self) -> None:
        self.enemy_death_sound.set_volume(0.1)
        self.enemy_death_sound.play(-1)
