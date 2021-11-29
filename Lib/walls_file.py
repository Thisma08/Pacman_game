import pygame as pg
from vector import Vector2
from constants_file import *
import numpy as np


class Wall(object):
    def __init__(self, row, col):
        self.name = WALL
        self.pos = Vector2(col * TILE_W - TILE_W/2, row * TILE_H - TILE_H/2)
        self.color = GREEN
        self.visible = True

    def render(self, screen):
        if self.visible:
            p = self.pos.asInt()
            pg.draw.rect(screen, self.color, pg.Rect(p, (TILE_W, TILE_H)))

class WallGroup(object):
    def __init__(self, wallfile):
        self.wallList = []
        self.createWallList(wallfile)

    def createWallList(self, wallfile):
        data = self.readWallfile(wallfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['X']:
                    self.wallList.append(Wall(row, col))

    def readWallfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def isEmpty(self):
        if len(self.wallList) == 0:
            return True
        return False

    def render(self, screen):
        for wall in self.wallList:
            wall.render(screen)