import pygame as pg
from pygame.locals import *
from vector import Vector2
from constants_file import *
from characters_file import Character
from modes_file import ModeController

class Enemy(Character):
    def __init__(self, node, player=None):
        Character.__init__(self, node)
        self.name = ENEMY
        self.points = 200
        self.color = RED
        self.radius = 12
        self.speed = 120
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.player = player
        self.mode = ModeController(self)

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Character.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.player.pos

    def setFreightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.duration = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.color = BLUE
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

    def normalMode(self):
        self.color = RED
        self.setSpeed(78)
        self.directionMethod = self.goalDirection