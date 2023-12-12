import pygame, random
from Settings import *


class Plane_Character(pygame.sprite.Sprite):

    def __init__(
            self,
            x: int,
            y: int,
            images: list[pygame.image],
            *group_all_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(group_all_sprite)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.width, self.height = 256, 128-30
        self.x = x
        self.y = y
        self.images = images

        self.cur_frame = 0
        self.image = images[self.cur_frame]
        self.images = list(map(lambda image: pygame.transform.scale(image, (self.width, self.height+30)), self.images))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed_x = 500
        self.speed_y = 500
        self.rings = 14

    def move_right(self) -> (int, float):
        self.moving_right = True
        if self.x + (self.speed_x / FPS) + self.width <= SCREEN_WIDTH:
            self.x += self.speed_x / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_left(self) -> (int, float):
        self.moving_left = True
        if self.x - (self.speed_x / FPS) >= 0:
            self.x -= self.speed_x / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_up(self) -> (int, float):
        self.moving_up = True
        if self.y - (self.speed_y / FPS) >= 0:
            self.y -= self.speed_y / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_down(self) -> (int, float):
        self.moving_down = True
        if self.y + (self.speed_y / FPS) + self.height <= SCREEN_HEIGHT:
            self.y += self.speed_y / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def alive(self):
        return self.rings >= 0

    def update(self, *args, **kwargs) -> None:
        self.cur_frame += 1
        self.image = self.images[self.cur_frame // 2 % len(self.images)]


class Plane_Enemy(pygame.sprite.Sprite):

    def __init__(
            self,
            images: list[pygame.image],
            *group_all_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(*group_all_sprite)
        self.k = random.random()
        self.width, self.height = int(45 * (2 + self.k)), int(25 * (2 + self.k))
        self.x = SCREEN_WIDTH + random.randint(1000, 1200)
        self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        self.images = images

        self.cur_frame = 0
        self.images = list(map(lambda image: pygame.transform.scale(image, (self.width, self.height)), self.images))
        self.image = images[self.cur_frame]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed_x = random.randint(400, 600)
        self.speed_y = random.randint(-10, 10)
        self.health = 15 * (1 + 2 * self.k)

    def alive(self):
        return self.health > 0 and self.x + self.width > 0

    def update(self, *args, **kwargs):
        self.cur_frame += 1
        self.x -= self.speed_x / FPS
        self.y -= self.speed_y / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = self.images[self.cur_frame // 4 % len(self.images)]


class Plane_Bullet(pygame.sprite.Sprite):

    def __init__(
            self,
            x: int,
            y: int,
            speed_y,
            damage: int,
            width: int,
            height: int,
            speed: int,
            image: pygame.image,
            *group_all_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(*group_all_sprite)
        self.width, self.height = width, height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.image = image
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.speed_x = speed
        self.speed_y = speed_y
        self.damage = damage

    def update(self):
        self.x += self.speed_x / FPS
        self.y += self.speed_y / FPS
        screen.blit(self.image, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Plane_Rings(pygame.sprite.Sprite):

    def __init__(
            self,
            x: int,
            y: int,
            images: list[pygame.image],
            *group_all_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(*group_all_sprite)
        self.width, self.height = 64, 64
        self.x = SCREEN_WIDTH + x
        self.y = y
        self.images = images
        self.cur_frame = 0
        self.images = list(map(lambda image: pygame.transform.scale(image, (self.width, self.height)), self.images))
        self.image = images[self.cur_frame]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed_x = 400

    def update(self, *args, **kwargs):
        self.cur_frame += 1
        self.x -= self.speed_x / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = self.images[self.cur_frame // 4 % len(self.images)]


class Plane_Upgrates(pygame.sprite.Sprite):

    def __init__(
            self,
            type: int,
            image: pygame.image,
            *group_all_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(*group_all_sprite)
        self.width, self.height = 64, 64
        self.x = SCREEN_WIDTH + 200
        self.y = random.randint(int(0.25 * SCREEN_HEIGHT), int(0.75 * SCREEN_HEIGHT))
        self.cur_frame = 0
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed_x = 400
        self.type = type

    def update(self, *args, **kwargs):
        self.x -= self.speed_x / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Plane_Cloud(pygame.sprite.Sprite):

    def __init__(
            self,
            images: list[pygame.image],
            *group_all_sprite: pygame.sprite.Group
    ) -> None:
        super().__init__(*group_all_sprite)
        self.k = random.random()
        self.width, self.height = int(45 * (2 + self.k)), int(25 * (2 + self.k))
        self.x = SCREEN_WIDTH + random.randint(1000, 1200)
        self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        self.images = images

        self.cur_frame = 0
        self.images = list(map(lambda image: pygame.transform.scale(image, (self.width, self.height)), self.images))
        self.image = images[self.cur_frame]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed_x = 400
        self.health = 999999
        self.damage = 10

    def update(self, *args, **kwargs):
        self.cur_frame += 1
        self.x -= self.speed_x / FPS
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = self.images[self.cur_frame // 6 % len(self.images)]

