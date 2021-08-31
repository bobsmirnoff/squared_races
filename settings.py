import itertools

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
LIGHTGREY2 = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (20, 20, 255)

# graphic settings
TITLE = "Demo"
TILESIZE = 20
MARGIN = 20
WINDOW_WIDTH = TILESIZE * 30 + 2 * MARGIN + 300
WINDOW_HEIGHT = TILESIZE * 30 + 2 * MARGIN
MAP_WIDTH = TILESIZE * 30
MAP_HEIGHT = TILESIZE * 30
FPS = 60
BGCOLOR = LIGHTGREY
GRIDWIDTH = MAP_WIDTH / TILESIZE
GRIDHEIGHT = MAP_HEIGHT / TILESIZE

FONT_SIZE = 30
SMALL_FONT_SIZE = 18

# game rules
VELOCITY_INCREMENTS = list(filter(lambda i: abs(i[0]) + abs(i[1]) < 2, itertools.product(range(-1, 2), range(-1, 2))))

# paths
res_folder = "res"
font_folder = "fonts"
font_name = "verminvibes1989.ttf"
CIRCLE_IMG = "circle.png"
CAR_IMG = "car_mask.png"
MAP_FILE = "map.txt"
