from pathlib import Path

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

BLOCK_COLORS = (
    RED,
    GREEN,
    BLUE,
    YELLOW,
    CYAN,
    MAGENTA,
)
BONUS_BLOCK_COLOR = RED

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
SOUNDS_DIR = ASSETS_DIR / 'sounds'
FONTS_DIR = ASSETS_DIR / 'fonts'

MENU_FONT = FONTS_DIR / 'PressStart2P-Regular.ttf'
MENU_COLOR = WHITE

HUD_FONT = FONTS_DIR / 'PressStart2P-Regular.ttf'
HUD_COLOR = WHITE

ROWS_OF_BLOCKS = 6

IS_DEBUG = False
FPS = 60
