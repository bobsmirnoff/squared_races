import itertools

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# graphic settings
TITLE = "Demo"
WIDTH = 600   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 600  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
BGCOLOR = DARKGREY
TILESIZE = 20
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# game rules
VELOCITY_INCREMENTS = list(filter(lambda i: abs(i[0]) + abs(i[1]) < 2, itertools.product(range(-1, 2), range(-1, 2))))

# paths
res_folder = "/Users/bobsmirnov/Races/res"
CIRCLE_IMG = "circle.png"
CAR_IMG = "car.png"
MAP_FILE = "map.txt"
