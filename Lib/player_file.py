import pygame as pg
from pygame.locals import *
from vector import Vector2
from constants_file import *
from characters_file import Character

class Player(Character):
    def __init__(self, node):
        Character.__init__(self, node)
        self.name = PLAYER
        self.directions = {STOP: Vector2(), UP: Vector2(0, -1), DOWN: Vector2(0, 1), LEFT: Vector2(-1, 0),
                           RIGHT: Vector2(1, 0)}
        self.direction = STOP
        self.speed = 120
        self.radius = 12
        self.color = YELLOW
        self.node = node
        self.setPosition()
        self.target = node
        self.collideRadius = 3

    def getValidKey(self):
        key_pressed = pg.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            d = self.pos - pellet.pos
            dSquared = d.magnitudeSquared()
            rSquared = (pellet.radius + self.collideRadius)**2
            if dSquared <= rSquared:
                return pellet
        return None

    def update(self, dt):
        self.pos += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def render(self, screen):
        pos = self.pos.asInt()
        pg.draw.circle(screen, YELLOW, pos, self.radius)
