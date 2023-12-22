import pygame
from Settings import *


class Character(pygame.sprite.Sprite):

    def __init__(
            self,
            x: int,
            y: int,
            start_image: pygame.image,
            images: list[pygame.image],
            jump_images: list[pygame.image],
            dead_image: pygame.image,
            *group_all_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(*group_all_sprite)
        self.moving_left = False
        self.moving_right = False
        self.width, self.height = 100, 100
        self.dead_image = pygame.transform.scale(dead_image, (self.width, self.height))

        self.right_frames = list(map(lambda image: pygame.transform.scale(image, (self.width, self.height)), images))

        self.left_frames = list(map(lambda image: pygame.transform.flip(image, True, False), self.right_frames))
        self.x = x
        self.y = y

        self.start_image_right = pygame.transform.scale(start_image, (self.width, self.height))
        self.start_image_left = pygame.transform.flip(self.start_image_right, True, False)
        self.start_image = self.start_image_right
        self.image = self.start_image
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed_x = 6
        self.speed_y = 0
        self.is_jumping = False
        self.cur_frame = 0

        self.right_jump_frames = list(map(
            lambda image: pygame.transform.scale(image, (self.width, self.height)), jump_images
        ))
        self.left_jump_frames = list(map(
            lambda image: pygame.transform.flip(image, True, False), self.right_jump_frames
        ))
        self.cur_frame_jump = 0
        self.is_falling = False

    def update(self, *args, **kwargs) -> None:
        self.cur_frame = (self.cur_frame + 1) % len(self.left_frames)
        if self.is_jumping:
            self.cur_frame_jump = min(self.cur_frame_jump + 1, len(self.left_jump_frames) - 1)
            if self.moving_left:
                self.image = self.left_jump_frames[self.cur_frame_jump]
            else:
                self.image = self.right_jump_frames[self.cur_frame_jump]
        else:
            if self.moving_right and self.moving_left:
                self.image = self.start_image
            elif self.moving_left:
                self.image = self.left_frames[self.cur_frame]
                self.start_image = self.start_image_left
            elif self.moving_right:
                self.image = self.right_frames[self.cur_frame]
                self.start_image = self.start_image_right
            else:
                self.image = self.start_image
            self.cur_frame_jump = 0

    def move_left(self, tiles) -> None:
        self.moving_left = True
        self.moving_right = False
        can_move_right, can_move_left = self.can_move_x(tiles)
        if can_move_left * can_move_right == 1:
            self.x += self.speed_x / FPS
        else:
            self.start_jump(tiles)
            self.moving_left = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_right(self, tiles) -> None:
        self.moving_right = True
        self.moving_left = False
        can_move_left, can_move_right = self.can_move_x(tiles)
        if can_move_right * can_move_left == 1:
            self.x += self.speed_x / FPS
        else:
            self.start_jump(tiles)
            self.moving_right = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def start_jump(self, tiles_sprites) -> None:
        self.speed_y = -600
        self.is_jumping = True
        self.jump(tiles_sprites)

    def jump(self, tiles_sprites) -> None:
        can_move_top, can_move_bottom, ys = self.can_move_y(tiles_sprites)
        self.speed_y += GRAVITY / FPS
        if can_move_bottom:
            if can_move_top:
                self.y += (self.speed_y / FPS)
        else:
            self.is_jumping = False
            self.is_falling = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def start_dead_jump(self) -> None:
        self.speed_y = -400
        self.dead_jump()

    def dead_jump(self) -> bool:
        self.speed_y += GRAVITY / FPS
        self.y += self.speed_y / FPS
        self.image = self.dead_image
        if self.y > SCREEN_HEIGHT:
            super().kill()
            return False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return True

    def kill(self):
        self.alive = False
        self.start_dead_jump()

    def get_is_jumping(self) -> bool:
        return self.is_jumping

    def set_is_jumping(self, is_jumping: bool) -> None:
        self.is_jumping = is_jumping

    def set_speed_y(self, speed_y: float) -> None:
        self.speed_y = speed_y

    def set_moving_left(self, moving_left) -> None:
        self.moving_left = moving_left

    def get_moving_left(self) -> bool:
        return self.moving_left

    def get_moving_right(self) -> bool:
        return self.moving_right

    def set_moving_right(self, moving_right: bool) -> None:
        self.moving_right = moving_right

    def can_move_x(self, tiles_sprites) -> (bool, bool):
        return (not (any(self.rect.move(-self.speed_x / FPS, 0).colliderect(i) for i in tiles_sprites)),
                not (any(self.rect.move(self.speed_x / FPS, 0).colliderect(i) for i in tiles_sprites)))

    def can_move_y(self, tiles_sprites) -> (bool, bool):
        return (not (any(self.rect.move(0, self.speed_y / FPS).colliderect(i) for i in tiles_sprites)),
                not (any(self.rect.move(0, self.speed_y / FPS).colliderect(i) for i in tiles_sprites)))
