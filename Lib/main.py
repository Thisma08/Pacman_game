import pygame as pg
from pygame.locals import *
from constants import *
from player import Player
from nodes import NodeGroup


class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN, 0, 32)
        self.background = None
        self.clock = pg.time.Clock()

    def setBackground(self):
        self.background = pg.surface.Surface(SCREEN).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup()
        self.nodes.setupTestNodes()
        self.player = Player(self.nodes.nodeList[0])

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.player.update(dt)
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.player.render(self.screen)
        pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.startGame()
    while True:
        game.update()
