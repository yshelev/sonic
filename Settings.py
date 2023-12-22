import sys

import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 50
GRAVITY = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
LEFT_INVISIBLE_LINE = ((SCREEN_WIDTH // 2.5, SCREEN_HEIGHT // 2.5),
                       (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT // 1.5))
RIGHT_INVISIBLE_LINE = ((SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 2.5),
                        (SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 1.5))
BOTTOM_INVISIBLE_LINE = ((SCREEN_WIDTH // 2.5, SCREEN_HEIGHT // 1.5),
                         (SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 1.5))
TOP_INVISIBLE_LINE = ((SCREEN_WIDTH // 2.5, SCREEN_HEIGHT // 2.5),
                      (SCREEN_WIDTH // 1.5, SCREEN_HEIGHT // 2.5))


with open("data/txts/settings.txt") as f:
    settings = {i.split(" = ")[0]: i.split(" = ")[1] for i in f.readlines()}

sound = float(settings["sound"])
dict_movement_pointer = int(settings["dict_movement_pointer"])
max_score_sonic = int(settings["max_score_sonic"])
max_score_tiles = int(settings["max_score_tiles"])

dict_movement_buttons = {
    "top": pygame.K_w,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "down": pygame.K_s
}

dict_movement_arrows = {
    "top": pygame.K_UP,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "down": pygame.K_DOWN
}

dict_movement = [dict_movement_buttons, dict_movement_arrows]

OK = "OK"
STOPPED_BY_RIGHT_INVISIBLE_WALL = "stopped by right invisible wall"
STOPPED_BY_LEFT_INVISIBLE_WALL = "stopped by left invisible wall"
STOPPED_BY_LEFT_WALL_OUTSIDE = "stopped by right wall outside"
STOPPED_BY_RIGHT_WALL_OUTSIDE = "stopped by left wall outside"
STOPPED_BY_TOP_INVISIBLE_WALL = "stopped by top invisible wall"
STOPPED_BY_BOT_INVISIBLE_WALL = "stopped by bot invisible wall"
STOPPED_BY_TOP_WALL_OUTSIDE = "stopped by top wall outside"
STOPPED_BY_BOT_WALL_OUTSIDE = "stopped by bot wall outside"

MOVING = "sonic_is_moving"
LEFT = 'left'
RIGHT = 'right'
STAY = 'stay'
TOP = 'top'
BOT = 'bot'
exit_codes = {
    "sonic_movement_x": [
        OK,
        STOPPED_BY_RIGHT_INVISIBLE_WALL,
        STOPPED_BY_LEFT_INVISIBLE_WALL,
        STOPPED_BY_RIGHT_WALL_OUTSIDE,
        STOPPED_BY_LEFT_WALL_OUTSIDE,
        MOVING,
    ],
    "sonic_movement_y": [
        OK,
        STOPPED_BY_TOP_INVISIBLE_WALL,
        STOPPED_BY_BOT_INVISIBLE_WALL,
        STOPPED_BY_TOP_WALL_OUTSIDE,
        STOPPED_BY_BOT_WALL_OUTSIDE,
        MOVING,
    ],
}


def quit():
    with open("data/txts/settings.txt", "w") as f:
        f.write("\n".join([f"{sound = }",
                           f"{dict_movement_pointer = }",
                           f"{max_score_sonic = }",
                           f"{max_score_tiles = }"]))
    pygame.quit()
    sys.exit()