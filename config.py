from pathlib import Path

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BASE_BLOCK_COLOR = WHITE
BONUS_BLOCK_COLOR = RED

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
SOUNDS_DIR = ASSETS_DIR / 'sounds'
FONTS_DIR = ASSETS_DIR / 'fonts'

MENU_FONT = FONTS_DIR / 'PressStart2P-Regular.ttf'
MENU_COLOR = WHITE

HUD_FONT = FONTS_DIR / 'PressStart2P-Regular.ttf'
HUD_COLOR = WHITE

ROWS_OF_BLOCKS = 3

IS_DEBUG = False
FPS = 60
