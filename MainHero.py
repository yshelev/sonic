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
        self.stop_boost = 900
        self.can_kill = False
        self.number_of_rings = 50

    def move_left(self) -> (int, float):
        """
        вернет 0 если соник двигается внутри квадрата
        вернет 1 если соник уперся в обычную стенку
        вернет 2 если соник уперся в невидимую стенку
        """
        can_move_left, can_move_right = self.can_move_x()
        can_move_invisible_left, can_move_invisible_right = self.can_move_invisible_wall_x()
        exit_code = 0
        self.moving_left = True
        self.additional_speed = self.additional_speed - self.boost / FPS \
            if self.additional_speed < 0 else self.additional_speed - self.stop_boost / FPS

        if not can_move_invisible_left:
            exit_code = exit_codes["sonic_movement"].index(STOPPED_BY_LEFT_INVISIBLE_WALL)
        if not can_move_invisible_right:
            exit_code = exit_codes["sonic_movement"].index(STOPPED_BY_RIGHT_INVISIBLE_WALL)
        if (can_move_right + can_move_left) < 2:
            exit_code = exit_codes["sonic_movement"].index(STOPPED_BY_WALL_OUTSIDE)
        if can_move_left:
            if can_move_right:
                print(exit_code)

                if exit_codes["sonic_movement"][exit_code] == OK:
                    self.x -= (self.speed_x - self.additional_speed) / FPS
            else:
                self.x = SCREEN_WIDTH - self.width - 10
                self.additional_speed = 0
        else:
            self.x = 0
            self.additional_speed = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return exit_codes["sonic_movement"][exit_code], (self.speed_x - self.additional_speed) / FPS

    def move_right(self) -> (int, float):
        """
        вернет 0 если соник двигается внутри квадрата
        вернет 1 если соник уперся в обычную стенку
        вернет 2 если соник уперся в невидимую стенку
        """
        can_move_left, can_move_right = self.can_move_x()
        can_move_invisible_left, can_move_invisible_right = self.can_move_invisible_wall_x()
        exit_code = 0
        self.moving_right = True
        self.additional_speed = self.additional_speed + self.boost / FPS \
            if self.additional_speed > 0 else self.additional_speed + self.stop_boost / FPS

        if not can_move_invisible_left:
            exit_code = exit_codes["sonic_movement"].index(STOPPED_BY_LEFT_INVISIBLE_WALL)
        if not can_move_invisible_right:
            exit_code = exit_codes["sonic_movement"].index(STOPPED_BY_RIGHT_INVISIBLE_WALL)

        if (can_move_right + can_move_left) < 2:
            exit_code = exit_codes["sonic_movement"].index(STOPPED_BY_WALL_OUTSIDE)

        if can_move_right:
            if can_move_left:
                print(exit_code)
                if exit_codes["sonic_movement"][exit_code] == OK:
                    self.x += (self.speed_x + self.additional_speed) / FPS
            else:
                self.x = 10
                self.additional_speed = 0
        else:
            self.x = SCREEN_WIDTH - self.width
            self.additional_speed = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return exit_codes["sonic_movement"][exit_code], (self.speed_x + self.additional_speed) / FPS

    def update(self, *args, **kwargs) -> None:

        self.update_counters()
        self.drawing()

    def movement_by_inertia(self) -> None:
        can_move_left, can_move_right = self.can_move_x()
        can_move_invisible_left, can_move_invisible_right = self.can_move_invisible_wall_x()
        if not (self.moving_right or self.moving_left) or (self.moving_right and self.moving_left):
            if can_move_right and self.additional_speed > 0:
                if can_move_invisible_right:
                    self.x += self.additional_speed / FPS
            elif can_move_left and self.additional_speed < 0:
                if can_move_invisible_left:
                    self.x += self.additional_speed / FPS
            else:
                self.additional_speed = 0
            if self.additional_speed > 0:
                self.additional_speed = \
                    0 if self.additional_speed - self.stop_boost / FPS <= 0 else self.additional_speed - self.stop_boost / FPS
            elif self.additional_speed < 0:
                self.additional_speed = \
                    0 if self.additional_speed + self.stop_boost / FPS >= 0 else self.additional_speed + self.stop_boost / FPS
            if not self.is_jumping and abs(self.additional_speed) / FPS < 5:
                self.image = self.start_image
                self.cur_fast_frame = 0
            if not self.is_jumping:
                if self.additional_speed < 0:
                    self.image = self.fast_left_frames[self.cur_fast_frame]
                elif self.additional_speed > 0:
                    self.image = self.fast_left_frames[self.cur_fast_frame]

    def drawing(self) -> None:
        if self.is_jumping:
            if self.moving_left:
                self.image = self.left_jump_frames[self.cur_frame_jump]
            else:
                self.image = self.right_jump_frames[self.cur_frame_jump]
        else:
            self.cur_frame_jump = 0
            if self.moving_right and self.moving_left:
                self.image = self.start_image
            elif self.moving_left:
                if abs(self.additional_speed) / FPS > 7.5:
                    self.image = self.fast_left_frames[self.cur_fast_frame]
                    self.can_kill = True
                else:
                    self.image = self.left_frames[self.cur_frame]
                    self.start_image = self.start_image_left
                    self.can_kill = False
            elif self.moving_right:
                if abs(self.additional_speed) / FPS > 7.5:
                    self.image = self.fast_right_frames[self.cur_fast_frame]
                    self.can_kill = True
                else:
                    self.image = self.right_frames[self.cur_frame]
                    self.start_image = self.start_image_right
                    self.can_kill = False
            else:
                self.image = self.start_image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_counters(self) -> None:
        self.cur_frame = (self.cur_frame + 1) % len(self.left_frames)
        if abs(self.additional_speed) > 7.5:
            self.cur_fast_frame = (self.cur_fast_frame + 1) % len(self.fast_left_frames)
        if self.is_jumping:
            self.cur_frame_jump = min(self.cur_frame_jump + 1, len(self.left_jump_frames) - 1)

    def can_move_invisible_wall_x(self) -> (bool, bool):
        return (
            not pygame.rect.Rect(self.rect.x + (self.speed_x + self.additional_speed) / FPS,
                                 self.rect.y, self.rect.w, self.rect.h).colliderect(pygame.Rect(
                LEFT_INVISIBLE_LINE[0][0],
                LEFT_INVISIBLE_LINE[0][1],
                LEFT_INVISIBLE_LINE[0][0] - LEFT_INVISIBLE_LINE[1][0] + 5,
                LEFT_INVISIBLE_LINE[1][1] - LEFT_INVISIBLE_LINE[0][1])),
            not pygame.rect.Rect(self.rect.x + (self.speed_x + self.additional_speed) / FPS,
                                 self.rect.y, self.rect.w, self.rect.h).colliderect(pygame.Rect(
                RIGHT_INVISIBLE_LINE[0][0],
                RIGHT_INVISIBLE_LINE[0][1],
                RIGHT_INVISIBLE_LINE[0][0] - RIGHT_INVISIBLE_LINE[1][0] + 5,
                RIGHT_INVISIBLE_LINE[1][1] - RIGHT_INVISIBLE_LINE[0][1]))
        )

    def set_is_jumping(
            self,
            is_jumping: bool
    ) -> None:
        self.is_jumping = is_jumping

    def get_additional_speed(self) -> int:
        return self.additional_speed

    def get_number_of_rings(self) -> int:
        return self.number_of_rings

    def reset_speed(self) -> None:
        self.speed_x = 0
        self.additional_speed = 0