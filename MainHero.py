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

    def move_left(self, tiles) -> (int, float):
        """

        """
        can_move_left, can_move_right, point_x = self.can_move_x(tiles)
        can_move_invisible_left, can_move_invisible_right = self.can_move_invisible_wall_x()
        self.moving_left = True
        self.additional_speed -= self.boost / FPS
        self.rect = self.rect.move(self.x - int(point_x[0]) if point_x else 0, 0)
        move_code = self.get_move_code(can_move_left, can_move_right, can_move_invisible_left, can_move_invisible_right)

        ec = exit_codes["sonic_movement"][move_code]
        print(f"l{ec=}, ")

        if ec == OK:
            self.x -= (self.speed_x - self.additional_speed) / FPS
        elif ec != STOPPED_BY_LEFT_INVISIBLE_WALL:
            if can_move_left and self.move_direction() == LEFT:
                self.x -= (self.speed_x - self.additional_speed) / FPS * can_move_left * (self.move_direction() == LEFT)
        elif ec in [STOPPED_BY_RIGHT_WALL_OUTSIDE,
                    STOPPED_BY_LEFT_WALL_OUTSIDE]:
            self.x = point_x
            self.additional_speed = 0
        if self.move_direction() == RIGHT:
            self.additional_speed = max(self.additional_speed - self.stop_boost / FPS, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return exit_codes["sonic_movement"][move_code], self.speed_x - self.additional_speed

    def move_right(self, tiles: pygame.sprite.Group) -> (int, float):
        """

        """
        can_move_left, can_move_right, point_x = self.can_move_x(tiles)
        can_move_invisible_left, can_move_invisible_right = self.can_move_invisible_wall_x()
        self.moving_right = True
        self.additional_speed += self.boost / FPS

        move_code = self.get_move_code(can_move_left, can_move_right, can_move_invisible_left, can_move_invisible_right)

        ec = exit_codes["sonic_movement"][move_code]
        direction = self.move_direction()
        print(f"r{ec=}, ")
        if ec == OK:
            self.x += (self.speed_x + self.additional_speed) / FPS
        elif ec != STOPPED_BY_RIGHT_INVISIBLE_WALL:
            self.x += (self.speed_x + self.additional_speed) / FPS * can_move_right * (direction in [RIGHT, STAY])
        elif ec in [STOPPED_BY_RIGHT_WALL_OUTSIDE,
                    STOPPED_BY_LEFT_WALL_OUTSIDE]:
            self.x = point_x
            self.additional_speed = 0
        if self.move_direction() == LEFT:
            self.additional_speed = min(self.additional_speed + self.stop_boost / FPS, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return exit_codes["sonic_movement"][move_code], self.speed_x + self.additional_speed

    def movement_by_inertia(self, tiles) -> (int, float):
        """
        инерция(тормозит быстро)
        """
        can_move_left, can_move_right, point_x = self.can_move_x(tiles)
        can_move_invisible_left, can_move_invisible_right = self.can_move_invisible_wall_x()
        if not (self.moving_right or self.moving_left) or (self.moving_right and self.moving_left):
            move_code = self.get_move_code(can_move_left, can_move_right, can_move_invisible_left,
                                           can_move_invisible_right)
            direction = self.move_direction()

            if can_move_right and self.additional_speed > 0:
                if can_move_invisible_right:
                    self.x += self.additional_speed / FPS
            elif can_move_left and self.additional_speed < 0:
                if can_move_invisible_left:
                    self.x += self.additional_speed / FPS
            else:
                self.additional_speed = 0
            if direction == RIGHT:
                self.additional_speed = max(self.additional_speed - self.stop_boost / FPS, 0)
            elif direction == LEFT:
                self.additional_speed = min(self.additional_speed + self.stop_boost / FPS, 0)
            if not self.is_jumping and abs(self.additional_speed) / FPS < 5:
                self.image = self.start_image
                self.cur_fast_frame = 0
            if not self.is_jumping:
                if direction == LEFT:
                    self.image = self.fast_left_frames[self.cur_fast_frame]
                elif direction == RIGHT:
                    self.image = self.fast_left_frames[self.cur_fast_frame]
        else:
            move_code = exit_codes["sonic_movement"].index(MOVING)

        return move_code, self.additional_speed

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
                else:
                    self.image = self.left_frames[self.cur_frame]
                    self.start_image = self.start_image_left
            elif self.moving_right:
                if abs(self.additional_speed) / FPS > 7.5:
                    self.image = self.fast_right_frames[self.cur_fast_frame]
                else:
                    self.image = self.right_frames[self.cur_frame]
                    self.start_image = self.start_image_right
            else:
                self.image = self.start_image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update_counters(self) -> None:
        self.cur_frame = (self.cur_frame + 1) % len(self.left_frames)
        self.cur_fast_frame = (self.cur_fast_frame + 1 * (abs(self.additional_speed) > 7.5)) % len(
            self.fast_left_frames)
        self.cur_frame_jump = min(self.cur_frame_jump + 1 * self.is_jumping, len(self.left_jump_frames) - 1)

    def can_move_invisible_wall_x(self) -> (bool, bool):
        return (
            not pygame.rect.Rect(self.rect.x - (self.speed_x - self.additional_speed) / FPS, self.rect.y,
                                 self.width + (self.speed_x - self.additional_speed) / FPS,
                                 self.rect.height).colliderect(pygame.Rect(
                LEFT_INVISIBLE_LINE[0][0],
                LEFT_INVISIBLE_LINE[0][1],
                LEFT_INVISIBLE_LINE[0][0] - LEFT_INVISIBLE_LINE[1][0] + 5,
                LEFT_INVISIBLE_LINE[1][1] - LEFT_INVISIBLE_LINE[0][1])),
            not pygame.rect.Rect(self.rect.x, self.rect.y, self.width + (self.speed_x + self.additional_speed) / FPS,
                                 self.rect.height).colliderect(pygame.Rect(
                RIGHT_INVISIBLE_LINE[0][0],
                RIGHT_INVISIBLE_LINE[0][1],
                RIGHT_INVISIBLE_LINE[0][0] - RIGHT_INVISIBLE_LINE[1][0] + 5,
                RIGHT_INVISIBLE_LINE[1][1] - RIGHT_INVISIBLE_LINE[0][1]))
        )

    def can_move_x(self, tiles_sprites) -> (bool, bool):
        print(*[(i.rect.x, self.rect.x - (self.speed_x - self.additional_speed) / FPS, i.rect.w) for i in filter(lambda i: i.rect.x < self.rect.x, tiles_sprites)])
        return (not (any(
            pygame.rect.Rect(self.rect.x - (self.speed_x - self.additional_speed) / FPS,
                             self.rect.y,
                             self.width + (self.speed_x - self.additional_speed) / FPS,
                             self.rect.height).colliderect(i)
            for i in filter(lambda i: i.rect.x < self.rect.x, tiles_sprites))),
                not (any(
                    pygame.rect.Rect(self.rect.x,
                                     self.rect.y,
                                     self.width + (self.speed_x + self.additional_speed) / FPS,
                                     self.rect.height).colliderect(i)
                    for i in filter(lambda i: i.rect.x > self.rect.x, tiles_sprites))),
                [i.rect.x - self.rect.w if i.rect.x > self.rect.x else i.rect.x + i.rect.w for i in tiles_sprites if
                 pygame.rect.Rect(self.rect.x, self.rect.y,
                                  self.width + (self.speed_x + self.additional_speed) / FPS,
                                  self.rect.height).colliderect(i) or
                 pygame.rect.Rect(self.rect.x - (self.speed_x - self.additional_speed) / FPS, self.rect.y,
                                  self.width + (self.speed_x - self.additional_speed) / FPS,
                                  self.rect.height).colliderect(i)
                 ])

    def move_direction(self) -> str:
        return LEFT if self.additional_speed < 0 else RIGHT if self.additional_speed > 0 else STAY

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

    def update(self, *args, **kwargs) -> None:
        self.update_counters()
        self.drawing()

    def get_move_code(self,
                      ml: bool,
                      mr: bool,
                      iml: bool,
                      imr: bool) -> int:
        print(ml)
        if not mr:
            move_code = exit_codes["sonic_movement"].index(STOPPED_BY_RIGHT_WALL_OUTSIDE)
        elif not ml:
            move_code = exit_codes["sonic_movement"].index(STOPPED_BY_LEFT_WALL_OUTSIDE)
        elif not iml:
            move_code = exit_codes["sonic_movement"].index(STOPPED_BY_LEFT_INVISIBLE_WALL)
        elif not imr:
            move_code = exit_codes["sonic_movement"].index(STOPPED_BY_RIGHT_INVISIBLE_WALL)
        else:
            move_code = exit_codes["sonic_movement"].index(OK)
        return move_code
