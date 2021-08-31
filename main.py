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
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.lines = []
        self.circles = []
        self.players = Queue()
        # self.active_player = None

        self.game_area = pygame.Surface((MAP_WIDTH + 1, MAP_HEIGHT + 1))

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
        self.players.put(Player(self, 'player 1', GREEN))
        self.players.put(Player(self, 'player 2', RED, 22, 8))
        self.players.put(Player(self, 'player 3', BLUE, 15, 15))
        self.players.put(Player(self, 'player 4', YELLOW, 20, 20))
        self.players_list = list(self.players.queue)
        self.active_player = self.players.get()
        self.active_player.set_available_moves()
        # convert map data to curb tiles
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    CurbTile(self, col, row)
        self.curb_sprites.draw(self.game_area)
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
        pg.draw.line(self.game_area, tpl[0], tpl[1], tpl[2], tpl[3])

    def draw_circle(self, tpl):
        darker_color = tuple(int(t * 0.6) for t in tpl[0])
        pg.draw.circle(self.game_area, darker_color, ((tpl[1] + 0.5) * TILESIZE, (tpl[2] + 0.5) * TILESIZE), 5)

    def draw_grid(self):
        for x in range(TILESIZE, MAP_WIDTH, TILESIZE):
            pg.draw.line(self.game_area, LIGHTGREY2, (x, 0), (x, MAP_HEIGHT))
        for y in range(TILESIZE, MAP_HEIGHT, TILESIZE):
            pg.draw.line(self.game_area, LIGHTGREY2, (0, y), (MAP_WIDTH, y))
        pg.draw.line(self.game_area, BLACK, (0, 0), (0, MAP_HEIGHT))
        pg.draw.line(self.game_area, BLACK, (0, 0), (MAP_WIDTH, 0))
        pg.draw.line(self.game_area, BLACK, (0, MAP_HEIGHT), (MAP_WIDTH, MAP_HEIGHT))
        pg.draw.line(self.game_area, BLACK, (MAP_WIDTH, 0), (MAP_WIDTH, MAP_HEIGHT))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.game_area.fill(LIGHTGREY)
        self.draw_grid()
        for tpl in self.circles:
            self.draw_circle(tpl)
        for tpl in self.lines:
            self.draw_line(tpl)
        self.all.draw(self.game_area)
        self.screen.blit(self.game_area, (MARGIN, MARGIN))
        large_font = pygame.font.SysFont('verminvibes1989', FONT_SIZE)
        small_font = pygame.font.SysFont(None, SMALL_FONT_SIZE)
        # doesn't work somehow
        # font = pygame.font.SysFont(path.join(res_folder, font_folder, font_name), 50)

        for i, p in enumerate(self.players_list):
            main_text = large_font.render(p.name.upper(), True, p.color)
            main_text_rect = main_text.get_rect()
            main_text_rect.x = MAP_WIDTH + 3 * MARGIN + 35
            main_text_rect.y = 75 * (i + 1)
            self.screen.blit(main_text, main_text_rect)

            subtext = small_font.render('velocity: ' + print_crd(p.velocity.x, (-1) * p.velocity.y)
                                        + ',   moves: ' + str(p.moves), True, p.color)
            subtext_rect = subtext.get_rect()
            subtext_rect.x = MAP_WIDTH + 3 * MARGIN + 35
            subtext_rect.y = 30 + 75 * (i + 1)
            self.screen.blit(subtext, subtext_rect)

            if p == self.active_player:
                car_img = p.image_original
                car_rect = car_img.get_rect()
                car_rect.x = MAP_WIDTH + 3 * MARGIN
                car_rect.y = 75 * (i + 1) + 2
                self.screen.blit(car_img, car_rect)
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
                new_x = int((pos[0] - MARGIN) / TILESIZE)
                new_y = int((pos[1] - MARGIN) / TILESIZE)
                # print("X: ", new_x)
                # print("Y: ", new_y)
                if self.active_player.move(new_x, new_y):
                    self.active_player.moves += 1
                    self.pass_turn()
            if event.type == pg.MOUSEMOTION:
                pos = pg.mouse.get_pos()
                pos = (pos[0] - MARGIN, pos[1] - MARGIN)
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