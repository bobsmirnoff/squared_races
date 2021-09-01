import itertools

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
GAME_AREA_BG = (150, 150, 150)
LIGHTGREY = (100, 100, 100)
LIGHTGREY2 = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (50, 50, 255)

# graphic settings
TITLE = "Demo"
TILESIZE = 30
MARGIN = 20
WINDOW_WIDTH = TILESIZE * 30 + 2 * MARGIN + 300
WINDOW_HEIGHT = TILESIZE * 30 + 2 * MARGIN
MAP_WIDTH = 600
MAP_HEIGHT = 600
FPS = 60
BGCOLOR = DARKGREY
GRIDWIDTH = MAP_WIDTH / TILESIZE
GRIDHEIGHT = MAP_HEIGHT / TILESIZE

FONT_SIZE = 30
SMALL_FONT_SIZE = 18

# game rules
PLAYER_SPEED = 300
VELOCITY_INCREMENTS = list(filter(lambda i: abs(i[0]) + abs(i[1]) < 2, itertools.product(range(-1, 2), range(-1, 2))))

# paths
res_folder = "res"
font_folder = "fonts"
font_name = "verminvibes1989.ttf"
CIRCLE_IMG = "circle.png"
CAR_IMG = "car_mask.png"
MAP_FILE = "map2.txt"
