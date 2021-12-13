import pygame as pg
from pygame.locals import *
from constants_file import *
from player_file import Player
from intersections_file import InterGroup
from nonosses_file import NonosseGroup
from enemies_file import Enemy
from walls_file import WallGroup


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
        self.inters = InterGroup("maze1.txt")
        self.nonosses = NonosseGroup("maze1.txt")
        self.walls = WallGroup("maze1.txt")
        self.inters.setPortalPair((18, 17), (45, 17))
        self.player = Player(self.inters.getStartTempInter())
        self.enemy = Enemy(self.inters.getStartTempInter(), self.player)
        self.enemy.setSpawnInter(self.inters.getInterFromTiles(2+29.5, 3+14))
        homekey = self.inters.createHomeInters(29.5, 14)
        self.inters.connectHomeInter(homekey, (30, 14), LEFT)
        self.inters.connectHomeInter(homekey, (33, 14), RIGHT)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.player.update(dt)
        self.enemy.update(dt)
        self.nonosses.update(dt)
        self.checkNonosseEvents()
        self.checkEnemiesEvents()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

    def checkNonosseEvents(self):
        nonosse = self.player.eatNonosses(self.nonosses.nonosseList)
        if nonosse:
            self.nonosses.numEaten += 1
            self.nonosses.nonosseList.remove(nonosse)
            if nonosse.name == S_NONOSSE:
                self.enemy.startFreight()

    def checkEnemiesEvents(self):
        if self.player.collideEnemy(self.enemy):
            if self.enemy.mode.current is FREIGHT:
                self.enemy.startSpawn()


    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.inters.render(self.screen)
        self.nonosses.render(self.screen)
        self.walls.render(self.screen)
        self.player.render(self.screen)
        self.enemy.render(self.screen)
        pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.startGame()
    while True:
        game.update()
