import pygame as pg
from settings import *


class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.viewport = pg.Rect(0, 0, width, height)
        self.zoom = DEFAULT_ZOOM
        self.vx = 0
        self.vy = 0

    # overboard scrolling prevention
    def correct_onto_borders(self):
        x = max(-(self.width - MAP_WINDOW_WIDTH), min(0, self.viewport.x))
        y = max(-(self.height - MAP_WINDOW_HEIGHT), min(0, self.viewport.y))

        x = min(MAP_WINDOW_WIDTH / 2 * (1 - 1 / self.zoom), self.viewport.x)
        y = min(MAP_WINDOW_HEIGHT / 2 * (1 - 1 / self.zoom), self.viewport.y)

        # if self.viewport.x - MAP_WINDOW_WIDTH / 2 * (1 - 1 / self.zoom) - MAP_WINDOW_WIDTH / self.zoom < -self.game.map.width:
        #     self.viewport.x = -self.game.map.width + MAP_WINDOW_WIDTH / 2 * (1 - 1 / self.zoom) + MAP_WINDOW_WIDTH / self.zoom
        # if self.viewport.y - MAP_WINDOW_HEIGHT / 2 * (1 - 1 / self.zoom) - MAP_WINDOW_HEIGHT / self.zoom < -self.game.map.height:
        #     self.viewport.y = -self.game.map.height + MAP_WINDOW_HEIGHT / 2 * (1 - 1 / self.zoom) + MAP_WINDOW_HEIGHT / self.zoom

        x = max(MAP_WINDOW_WIDTH * ((1 - 1 / self.zoom) / 2 + 1 / self.zoom) - self.game.map.width, x)
        y = max(MAP_WINDOW_HEIGHT * ((1 - 1 / self.zoom) / 2 + 1 / self.zoom) - self.game.map.height, y)
        self.viewport = pg.Rect(x, y, self.width, self.height)

    def apply(self, entity):
        return self.apply_img(entity.image), self.apply_rect(entity.rect)

    def apply_img(self, img):
        return pg.transform.scale(img, (int(TILESIZE * self.zoom), int(TILESIZE * self.zoom)))

    def apply_map_img(self, img):
        return pg.transform.scale(img, (int(self.game.map.width * self.zoom), int(self.game.map.height * self.zoom)))

    def apply_rect(self, rect):
        transformed_rect = pg.Rect(rect.x * self.zoom, rect.y * self.zoom, rect.width * self.zoom,
                                   rect.height * self.zoom)
        new_x = self.viewport.x + (self.zoom - 1) * (self.viewport.x - MAP_WINDOW_WIDTH / 2)
        new_y = self.viewport.y + (self.zoom - 1) * (self.viewport.y - MAP_WINDOW_HEIGHT / 2)
        if self.viewport.x - MAP_WINDOW_WIDTH / 2 * (1 - 1 / self.zoom) > 0:
            new_x = (self.viewport.x - MAP_WINDOW_WIDTH / 2 * (1 - 1 / self.zoom)) * self.zoom
        if self.viewport.y - MAP_WINDOW_HEIGHT / 2 * (1 - 1 / self.zoom) > 0:
            new_y = (self.viewport.y - MAP_WINDOW_HEIGHT / 2 * (1 - 1 / self.zoom)) * self.zoom
        self.correct_onto_borders()
        return transformed_rect.move(new_x, new_y)

    def update(self, target_rect):
        new_x = -target_rect.x + int(MAP_WINDOW_WIDTH / 2) - TILESIZE / 2
        new_y = -target_rect.y + int(MAP_WINDOW_HEIGHT / 2) - TILESIZE / 2
        self.viewport = pg.Rect(new_x, new_y, self.width, self.height)
        self.correct_onto_borders()

    def move(self):
        self.viewport = self.viewport.move(self.vx * self.game.dt * self.zoom * TILESIZE,
                                           self.vy * self.game.dt * self.zoom * TILESIZE)
        self.correct_onto_borders()