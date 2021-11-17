import pygame as pg
from pygame.locals import *
from constants import *
from player import Player
from nodes import NodeGroup
from pellets import PelletGroup
from enemies import Enemy
from walls import WallGroup


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
        self.nodes = NodeGroup("maze1.txt")
        self.pellets = PelletGroup("maze1.txt")
        self.walls = WallGroup("maze1.txt")
        self.nodes.setPortalPair((18, 17), (45, 17))
        self.player = Player(self.nodes.getStartTempNode())
        self.enemy = Enemy(self.nodes.getStartTempNode(), self.player)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.player.update(dt)
        self.enemy.update(dt)
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

    def checkPelletEvents(self):
        pellet = self.player.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.walls.render(self.screen)
        self.player.render(self.screen)
        self.enemy.render(self.screen)
        pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.startGame()
    while True:
        game.update()
