import pygame as pg
import pygame.gfxdraw
from queue import Queue
import sys
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.lines = []
        self.circles = []
        self.players = Queue()
        # self.active_player = None

    def load_data(self):
        self.circle_img = pg.image.load(path.join(res_folder, CIRCLE_IMG)).convert_alpha()
        self.car_img = pg.transform.scale(pg.image.load(path.join(res_folder, CAR_IMG)).convert_alpha(),
                                          (TILESIZE, TILESIZE))
        self.map_data = []
        # read map file
        with open(path.join(res_folder, MAP_FILE), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        self.all = pg.sprite.LayeredUpdates()
        self.av_move_sprites = pg.sprite.LayeredUpdates()
        self.curb_sprites = pg.sprite.Group()
        # player color setup
        self.players.put(Player(self, GREEN))
        self.players.put(Player(self, RED, 22, 8))
        # self.players.put(Player(self, BLUE, 15, 15))
        self.active_player = self.players.get()
        self.active_player.set_available_moves()
        # convert map data to curb tiles
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    CurbTile(self, col, row)
        self.curb_sprites.draw(self.screen)
        pg.display.flip()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all.update()

    def draw_line(self, tpl):
        pg.draw.line(self.screen, tpl[0], tpl[1], tpl[2], tpl[3])

    def draw_circle(self, tpl):
        darker_color = tuple(int(t * 0.6) for t in tpl[0])
        pg.draw.circle(self.screen, darker_color, ((tpl[1] + 0.5) * TILESIZE, (tpl[2] + 0.5) * TILESIZE), 5)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY2, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY2, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for tpl in self.circles:
            self.draw_circle(tpl)
        for tpl in self.lines:
            self.draw_line(tpl)
        self.all.draw(self.screen)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                new_x = int(pos[0] / TILESIZE)
                new_y = int(pos[1] / TILESIZE)
                # print("X: ", new_x)
                # print("Y: ", new_y)
                if self.active_player.move(new_x, new_y):
                    self.pass_turn()
            if event.type == pg.MOUSEMOTION:
                pos = pg.mouse.get_pos()
                for am in self.av_move_sprites:
                    # repaint all circles as light
                    pg.draw.circle(am.image, self.active_player.lighter_color, (TILESIZE / 2, TILESIZE / 2), 5)
                    if am.rect.collidepoint(pos):
                        # repaint one hovered over
                        pg.draw.circle(am.image, self.active_player.color, (TILESIZE / 2, TILESIZE / 2), 5)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def pass_turn(self):
        for s in self.av_move_sprites.sprites():
            s.kill()
        self.players.put(self.active_player)
        self.active_player = self.players.get()
        self.active_player.set_available_moves()

    def is_available_move(self, mov_x, mov_y):
        for p in self.players.queue:
            if p.x == mov_x and p.y == mov_y:
                return False
        return True


g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()