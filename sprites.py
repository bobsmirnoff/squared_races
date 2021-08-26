import pygame as pg
import numpy as np
from colorsys import rgb_to_hls, hls_to_rgb
from settings import *

def print_crd(x, y):
    return "(" + str(x) + "," + str(y) + ")"

def get_lighter_color(color):
    h, l, s = rgb_to_hls(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    r, g, b = hls_to_rgb(h, max(min(l * 1.5, 1.0), 0.0), s)
    return int(r * 255), int(g * 255), int(b * 255)

class Velocity():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class CurbTile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.curb_sprites, game.all
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class AvailableMoveSprite(pg.sprite.Sprite):
    def __init__(self, game, color, x, y):
        self.groups = game.av_move_sprites, game.all
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = color
        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA, 32)
        pg.draw.circle(self.image, self.color, (TILESIZE / 2, TILESIZE / 2), 5)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def update_color(self, color):
        self.color = color
        self.update()


class Circle(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 1
        self.groups = game.all
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.circle_img
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * TILESIZE + self.size[0]
        self.rect.y = self.y * TILESIZE + self.size[1]


class Player(pg.sprite.Sprite):
    def __init__(self, game, color, x=0, y=0):
        self._layer = 1
        self.groups = game.all
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = color
        self.lighter_color = get_lighter_color(color)
        self.image_path = game.car_img
        self.image = self.image_path
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.velocity = Velocity()
        self.available_sprites = []
        self.set_available_moves()

    def move(self, new_x=0, new_y=0):
        if self.is_available_move(new_x, new_y):
            # Circle(self.game, self.x, self.y)
            self.game.circles.append((self.color, self.x, self.y))
            self.game.lines.append((self.color,
                                    ((self.x + 0.5) * TILESIZE, (self.y + 0.5) * TILESIZE),
                                    ((new_x + 0.5) * TILESIZE, (new_y + 0.5) * TILESIZE), 1))
            for curb in self.game.curb_sprites:
                cl = curb.rect.clipline(((self.x + 0.5) * TILESIZE, (self.y + 0.5) * TILESIZE),
                               ((new_x + 0.5) * TILESIZE, (new_y + 0.5) * TILESIZE))
                if cl:
                    print("COLLISION ! ! !")
                    break
            # print("available moves from ", print_crd(self.x, self.y), "to", print_crd(new_x, new_y))
            # print("is move available:", self.is_available_move(new_x, new_y))
            self.velocity = Velocity(new_x - self.x, new_y - self.y)
            print("new velocity:", print_crd(self.velocity.x, self.velocity.y))
            self.x = new_x
            self.y = new_y
            self.set_available_moves()

            for curb in self.game.curb_sprites:
                if new_x == curb.x and new_y == curb.y:
                    print("COLLISION ! ! !")
                    break

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.image = pg.transform.rotate(self.image_path,
                                         np.angle(complex(self.velocity.x, np.negative(self.velocity.y)), deg=True))
        for a in self.available_sprites:
            a.update()

    def set_available_moves(self):
        pot_new_speed = [(self.velocity.x + i, self.velocity.y + j) for i, j in VELOCITY_INCREMENTS]
        # print("potential new speed:", pot_new_speed)
        # print("potential positions: ", [(self.x + v[0], self.y + v[1]) for v in pot_new_speed])
        pot_pos = list(filter(lambda p: p[0] >= 0 and p[1] >= 0, [(self.x + v[0], self.y + v[1]) for v in pot_new_speed]))
        # print("filtered new positions: ", pot_pos)
        self.available_moves = pot_pos
        for s in self.game.av_move_sprites.sprites():
            s.kill()
        self.available_sprites = [AvailableMoveSprite(self.game, self.lighter_color, p[0], p[1]) for p in pot_pos]

    def is_available_move(self, mov_x, mov_y):
        pot_pos = self.available_moves
        # print("is move available: ", any(mov_x == p[0] and mov_y == p[1] for p in pot_pos))
        return any(mov_x == p[0] and mov_y == p[1] for p in pot_pos)

