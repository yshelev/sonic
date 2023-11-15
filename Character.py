import pygame
from Settings import SCREEN_HEIGHT, SCREEN_WIDTH, GRAVITY


class Character(pygame.sprite.Sprite):

    def __init__(self, x, y, start_image, images, jump_images, group_all_sprite):
        super().__init__(group_all_sprite)
        self.moving_left = False
        self.moving_right = False
        self.width, self.height = 500, 500
        self.right_frames = list(map(lambda image: pygame.transform.scale(image, (self.width, self.height)), images))

        self.left_frames = list(map(lambda image: pygame.transform.flip(image, True, False), self.right_frames))
        self.x = x
        self.y = y

        self.start_image_right = pygame.transform.scale(start_image, (self.width, self.height))
        self.start_image_left = pygame.transform.flip(self.start_image_right, True, False)
        self.start_image = self.start_image_right
        self.image = self.start_image
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed_x = 3
        self.speed_y = -10
        self.is_jumping = False
        self.cur_frame = 0

        self.right_jump_frames = list(map(
            lambda image: pygame.transform.scale(image, (self.width, self.height)), jump_images
        ))
        self.left_jump_frames = list(map(
            lambda image: pygame.transform.flip(image, True, False), self.right_jump_frames
        ))
        self.cur_frame_jump = 0

    def update(self, *args, **kwargs):
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
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_left(self):
        self.moving_left = True
        if self.x - self.speed_x >= 0:
            self.x -= self.speed_x
        else:
            self.x = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_right(self):
        self.moving_right = True
        if self.x + self.width + self.speed_x <= SCREEN_WIDTH:
            self.x += self.speed_x
        else:
            self.x = SCREEN_WIDTH - self.width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        self.speed_y += GRAVITY
        if self.speed_y + self.y + self.height < SCREEN_HEIGHT:
            if self.y + self.speed_y > 0:
                self.y += self.speed_y
            else:
                self.y = 0
        else:
            self.y = SCREEN_HEIGHT - self.height
            self.is_jumping = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_is_jumping(self):
        return self.is_jumping

    def set_is_jumping(self, is_jumping):
        self.is_jumping = is_jumping

    def set_speed_y(self, speed_y):
        self.speed_y = speed_y

    def set_moving_left(self, moving_left):
        self.moving_left = moving_left

    def set_moving_right(self, moving_right):
        self.moving_right = moving_right
# ы
