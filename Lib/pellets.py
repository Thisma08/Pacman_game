import pygame
from vector import Vector2
from constants import *
import numpy as np


class Pellet(object):
    def __init__(self, row, column):
        self.name = PELLET
        self.pos = Vector2(column * TILE_W, row * TILE_H)
        self.color = WHITE
        self.radius = int(4 * TILE_W / 16)
        self.collideRadius = int(4 * TILE_W / 16)
        self.points = 10
        self.visible = True

    def render(self, screen):
        if self.visible:
            p = self.pos.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)


class PowerPellet(Pellet):
    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.name = P_PELLET
        self.radius = int(8 * TILE_W / 16)
        self.points = 50
        self.flashTime = 0.1
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup(object):
    def __init__(self, pelletfile):
        self.pelletList = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.numEaten = 0

    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)

    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False

    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)
