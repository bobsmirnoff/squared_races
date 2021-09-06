import pygame as pg
from os import path
from settings import *
import pytmx

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


class TiledMap:
    def __init__(self, map_filename):
        self.tmx_data = pytmx.load_pygame(map_filename, pixelalpha=True)
        self.width = self.tmx_data.tilewidth * self.tmx_data.width
        self.height = self.tmx_data.tileheight * self.tmx_data.height
        print(self.width, self.height)

    def render(self, surface):
        ti = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def make_map(self):
        tmp_surface = pg.Surface((self.width, self.height))
        self.render(tmp_surface)
        return tmp_surface
