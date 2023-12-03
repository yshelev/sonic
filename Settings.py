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

OK = "OK"
STOPPED_BY_RIGHT_INVISIBLE_WALL = "stopped by right invisible wall"
STOPPED_BY_LEFT_INVISIBLE_WALL = "stopped by left invisible wall"
STOPPED_BY_LEFT_WALL_OUTSIDE = "stopped by right wall outside"
STOPPED_BY_RIGHT_WALL_OUTSIDE = "stopped by left wall outside"
MOVING = "sonic_is_moving"
LEFT = 'left'
RIGHT = 'right'
STAY = 'stay'
TOP = 'top'
BOT = 'bot'
exit_codes = {
    "sonic_movement": [
        OK,
        STOPPED_BY_RIGHT_INVISIBLE_WALL,
        STOPPED_BY_LEFT_INVISIBLE_WALL,
        STOPPED_BY_RIGHT_WALL_OUTSIDE,
        STOPPED_BY_LEFT_WALL_OUTSIDE,
        MOVING,
    ],
}

