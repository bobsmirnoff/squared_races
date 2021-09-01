import pygame as pg
from os import path
from settings import *


class Map:
    def __init__(self, map_filename):
        self.data = []
        with open(map_filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE


class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.camera = pg.Rect(0, 0, width, height)
        self.vx = 0
        self.vy = 0

    # overboard scrolling prevention
    def correct_onto_borders(self):
        x = max(-(self.width - MAP_WIDTH), min(0, self.camera.x))
        y = max(-(self.height - MAP_HEIGHT), min(0, self.camera.y))
        self.camera = pg.Rect(x, y, self.width, self.height)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target_rect):
        new_x = -target_rect.x + int(MAP_WIDTH / 2)
        new_y = -target_rect.y + int(MAP_HEIGHT / 2)
        self.camera = pg.Rect(new_x, new_y, self.width, self.height)
        self.correct_onto_borders()

    def move(self, dx=0, dy=0):
        self.camera = self.camera.move(self.vx * self.game.dt, self.vy * self.game.dt)
        self.correct_onto_borders()
