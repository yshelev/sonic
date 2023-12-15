import pygame


class Eggman(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, robot_sprites, machine_sprites, man_sprites, *sprite_group):
        super().__init__(*sprite_group)
        self.x = x
        self.y = y

        self.animation_stages = {
            "jump",
            "run",
            "walk_into_with_car",
            "car_death",
            "walk_into_with_robot"
        }

        self.machine_width = width * 3
        self.robot_width = width * 2
        self.machine_height = height * 2
        self.robot_height = height * 2
        self.man_width = width
        self.man_height = height

        self.types = {
            "robot": robot_sprites,
            "machine": machine_sprites,
            "man": man_sprites
        }

        self.type = self.start_type = "man"

        self.image = self.start_image = self.types[self.start_type][0]

        self.rect = pygame.Rect(self.x, self.y, self.man_width, self.man_height)



