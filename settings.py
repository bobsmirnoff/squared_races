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
TILESIZE = 25
WIDTH = TILESIZE * 30
HEIGHT = TILESIZE * 30
FPS = 60
BGCOLOR = LIGHTGREY
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# game rules
VELOCITY_INCREMENTS = list(filter(lambda i: abs(i[0]) + abs(i[1]) < 2, itertools.product(range(-1, 2), range(-1, 2))))

# paths
res_folder = "/Users/bobsmirnov/Races/res"
CIRCLE_IMG = "circle.png"
CAR_IMG = "car_mask.png"
MAP_FILE = "map.txt"
