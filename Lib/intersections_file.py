import pygame as pg
from vector import Vector2
from constants_file import *
import numpy as np

class Intersection(object):
    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None, PORTAL: None}

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.pos.asTuple()
                line_end = self.neighbors[n].pos.asTuple()
                # pg.draw.line(screen, WHITE, line_start, line_end, 4)
                # pg.draw.circle(screen, RED, self.pos.asInt(), 12)


class InterGroup(object):
    def __init__(self, level):
        self.level = level
        self.interLUT = {}
        self.interSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createInterTable(data)
        self.connectHor(data)
        self.connectVer(data)
        self.homekey = None

    def connectHor(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.interSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.interLUT[key].neighbors[RIGHT] = self.interLUT[otherkey]
                        self.interLUT[otherkey].neighbors[LEFT] = self.interLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVer(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.interSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.interLUT[key].neighbors[DOWN] = self.interLUT[otherkey]
                        self.interLUT[otherkey].neighbors[UP] = self.interLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def readMazeFile(self, textFile):
        return np.loadtxt(textFile, dtype='<U1')

    def constructKey(self, x, y):
        return x * TILE_W, y * TILE_H

    def createInterTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.interSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.interLUT[(x, y)] = Intersection(x, y)

    def getInterFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.interLUT.keys():
            return self.interLUT[(xpixel, ypixel)]
        return None

    def getInterFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.interLUT.keys():
            return self.interLUT[(x, y)]
        return None

    def getStartTempInter(self):
        inters = list(self.interLUT.values())
        return inters[0]

    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.interLUT.keys() and key2 in self.interLUT.keys():
            self.interLUT[key1].neighbors[PORTAL] = self.interLUT[key2]
            self.interLUT[key2].neighbors[PORTAL] = self.interLUT[key1]

    def render(self, screen):
        for inter in self.interLUT.values():
            inter.render(screen)

    def createHomeInters(self, xoffset, yoffset):
        homedata = np.array([['X', 'X', '+', 'X', 'X'],
                             ['X', 'X', '.', 'X', 'X'],
                             ['+', 'X', '.', 'X', '+'],
                             ['+', '.', '+', '.', '+'],
                             ['+', 'X', 'X', 'X', '+']])

        self.createInterTable(homedata, xoffset, yoffset)
        self.connectHor(homedata, xoffset, yoffset)
        self.connectVer(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset + 2, yoffset)
        return self.homekey

    def connectHomeInters(self, homekey, otherkey, direction):
        key = self.constructKey(*otherkey)
        self.interLUT[homekey].neighbors[direction] = self.interLUT[key]
        self.interLUT[key].neighbors[direction * -1] = self.interLUT[homekey]