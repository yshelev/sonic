import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
GRAVITY = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
LEFT_INVISIBLE_LINE = ((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3),
                       (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3 * 2))
RIGHT_INVISIBLE_LINE = ((SCREEN_WIDTH // 3 * 2, SCREEN_HEIGHT // 3),
                        (SCREEN_WIDTH // 3 * 2, SCREEN_HEIGHT // 3 * 2))
BOTTOM_INVISIBLE_LINE = ((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3 * 2),
                         (SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT // 3 * 2))
TOP_INVISIBLE_LINE = ((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3),
                      (SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT // 3))

sound = 0.1

dict_movement_buttons = {
    "top": pygame.K_w,
    "left": pygame.K_a,
    "right": pygame.K_d
}

dict_movement_arrows = {
    "top": pygame.K_UP,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT
}

dict_movement_pointer = 0

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
