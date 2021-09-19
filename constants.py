from enum import Enum
from os import path
import pygame


class COLOR(Enum):
    # RGB ЦВЕТА
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


SIZE_OF_PIN = 50
NUMBER_OF_PINS = 5
FIELD_WIDTH = SIZE_OF_PIN * NUMBER_OF_PINS
FIELD_HEIGHT = SIZE_OF_PIN * NUMBER_OF_PINS
WINDOW_WIDTH = SIZE_OF_PIN * NUMBER_OF_PINS
WINDOW_HEIGHT = SIZE_OF_PIN * (NUMBER_OF_PINS + 1)
FPS = 60
LOCKED = NUMBER_OF_PINS + 1
TYPES = 3
IMG_DIR = path.join(path.dirname(__file__), 'assets')
BLUE_PLAYER_IMG = pygame.image.load(path.join(IMG_DIR, 'blue_pin.png'))
BROWN_PLAYER_IMG = pygame.image.load(path.join(IMG_DIR, 'brown_pin.png'))
RED_PLAYER_IMG = pygame.image.load(path.join(IMG_DIR, 'red_pin.png'))
SELECTED_PIN_IMG = pygame.image.load(path.join(IMG_DIR, 'selected_pin.png'))
LOCKED_PIN_IMG = pygame.image.load(path.join(IMG_DIR, 'locked_pin.png'))
FREE_PIN_IMG = pygame.image.load(path.join(IMG_DIR, 'free_pin.png'))
FONT_NAME = pygame.font.match_font('arial')
SOUND_DIR = path.join(path.dirname(__file__), "sound")
SPRITE_CONFIG = {"blue": (BLUE_PLAYER_IMG, (SIZE_OF_PIN-5, SIZE_OF_PIN-5)),
                 "red": (RED_PLAYER_IMG, (SIZE_OF_PIN-5, SIZE_OF_PIN-5)),
                 "brown": (BROWN_PLAYER_IMG, (SIZE_OF_PIN-5, SIZE_OF_PIN-5)),
                 "select": (SELECTED_PIN_IMG, (SIZE_OF_PIN, SIZE_OF_PIN)),
                 "lock": (LOCKED_PIN_IMG, (SIZE_OF_PIN, SIZE_OF_PIN)),
                 "free": (FREE_PIN_IMG, (SIZE_OF_PIN-5, SIZE_OF_PIN-5))}
