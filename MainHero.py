from Character import Character
from Settings import *
import pygame


class MainHero(Character):
    def __init__(self, x, y, start_image, images, jump_images, group_all_sprite):
        super().__init__(x, y, start_image, images, jump_images, group_all_sprite)
        self.additional_speed = 0
        self.boost = 0.1
        self.can_kill = False
        self.can_jump = True
        self.jump_cooldown = 300
        self.jump_cooldown_count = 0
        self.number_of_rings = 100

    def move_left(self):
        self.moving_left = True
        self.additional_speed -= self.boost
        if self.x - self.speed_x + self.additional_speed >= 0:
            self.x -= self.speed_x - self.additional_speed
        else:
            self.x = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_right(self):
        self.moving_right = True
        self.additional_speed += self.boost
        if self.x + self.width + self.speed_x <= SCREEN_WIDTH:
            self.x += (self.speed_x + self.additional_speed)
        else:
            self.x = SCREEN_WIDTH - self.width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, *args, **kwargs):
        self.cur_frame = (self.cur_frame + 1) % len(self.left_frames)
        self.cur_frame_jump = min(self.cur_frame_jump + 1, len(self.left_jump_frames) - 1)
        if not self.can_jump:
            self.jump_cooldown_count = (self.jump_cooldown_count + 1) % self.jump_cooldown
            if self.jump_cooldown_count == 0:
                self.can_jump = True

        if self.is_jumping:
            if self.moving_left:
                self.image = self.left_jump_frames[self.cur_frame_jump]
            else:
                self.image = self.right_jump_frames[self.cur_frame_jump]
        else:
            if self.moving_right and self.moving_left:
                self.image = self.start_image
            elif self.moving_left:
                if abs(self.additional_speed) > 5:
                    self.image = self.left_jump_frames[self.cur_frame_jump]
                    self.can_kill = True
                else:
                    self.image = self.left_frames[self.cur_frame]
                    self.start_image = self.start_image_left
                    self.can_kill = False
            elif self.moving_right:
                if abs(self.additional_speed) > 5:
                    self.image = self.right_jump_frames[self.cur_frame_jump]
                    self.can_kill = True
                else:
                    self.image = self.right_frames[self.cur_frame]
                    self.start_image = self.start_image_right
                    self.can_kill = False
            else:
                self.image = self.start_image
            if abs(self.additional_speed) < 5:
                self.cur_frame_jump = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if not (self.moving_right or self.moving_left) or (self.moving_right and self.moving_left):
            self.x += self.additional_speed
            if self.additional_speed > 0:
                self.additional_speed = \
                    0 if self.additional_speed - self.boost <= 0 else self.additional_speed - self.boost
            elif self.additional_speed < 0:
                self.additional_speed = \
                    0 if self.additional_speed + self.boost >= 0 else self.additional_speed + self.boost
            if not self.is_jumping:
                self.image = self.start_image

    def set_is_jumping(self, is_jumping):
        self.is_jumping = is_jumping
        self.can_jump = False

    def get_can_jump(self):
        return self.can_jump

    def get_number_of_rings(self):
        return self.number_of_rings
