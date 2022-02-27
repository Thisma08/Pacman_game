import pygame as pg
from pygame.locals import *
from constants_file import *
from player_file import Player
from intersections_file import InterGroup
from nonosses_file import NonosseGroup
from enemies_file import EnemyGroup
from walls_file import WallGroup
from fruit_file import Fruit
from pause_file import Pause

class Game(object):
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN, 0, 32)
        self.background = None
        self.clock = pg.time.Clock()
        self.running = True
        self.score = 0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.fruit = None
        self.lives = 3
        self.level = 0
        self.pause = Pause(True)

    def setBackground(self):
        self.background = pg.surface.Surface(SCREEN).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.inters = InterGroup("maze1.txt")
        self.nonosses = NonosseGroup("maze1.txt")
        self.walls = WallGroup("maze1.txt")
        self.inters.setPortalPair((18, 17), (46, 17))
        self.player = Player(self.inters.getInterFromTiles(32, 20))
        self.enemies = EnemyGroup(self.inters.getStartTempInter(), self.player)
        self.enemies.enemy1.setStartInter(self.inters.getInterFromTiles(32, 14))
        self.enemies.enemy2.setStartInter(self.inters.getInterFromTiles(32, 17))
        self.enemies.enemy3.setStartInter(self.inters.getInterFromTiles(30, 17))
        self.enemies.enemy4.setStartInter(self.inters.getInterFromTiles(34, 17))
        self.enemies.setSpawnInter(self.inters.getInterFromTiles(32, 17))

        self.inters.denyHomeAccess(self.player)
        self.inters.denyHomeAccessList(self.enemies)
        self.inters.denyAccessList(32, 17, LEFT, self.enemies)
        self.inters.denyAccessList(32, 17, RIGHT, self.enemies)
        self.enemies.enemy3.startInter.denyAccess(RIGHT, self.enemies.enemy3)
        self.enemies.enemy4.startInter.denyAccess(LEFT, self.enemies.enemy4)

    def restartGame(self):
        self.lives = 3
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()

    def resetLevel(self):
        self.pause.paused = True
        self.player.reset()
        self.enemies.reset()
        self.fruit = None

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.nonosses.update(dt)
        if not self.pause.paused:
            self.player.update(dt)
            self.enemies.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkNonosseEvents()
            self.checkEnemiesEvents()
            self.checkFruitEvents()
        postPauseMethod = self.pause.update(dt)
        if postPauseMethod is not None:
            postPauseMethod()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_SPACE:
                    if self.player.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.showCharacters()
                        else:
                            self.hideCharacters()

    def checkNonosseEvents(self):
        nonosse = self.player.eatNonosses(self.nonosses.nonosseList)
        if nonosse:
            self.nonosses.numEaten += 1
            self.score += 10
            self.nonosses.nonosseList.remove(nonosse)
            if nonosse.name == S_NONOSSE:
                self.enemies.startFreight()
            if self.nonosses.numEaten == 30:
                self.enemies.enemy3.startInter.allowAccess(RIGHT, self.enemies.enemy3)
            if self.nonosses.numEaten == 60:
                self.enemies.enemy4.startInter.allowAccess(LEFT, self.enemies.enemy4)
            if self.nonosses.isEmpty():
                self.hideCharacters()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def checkEnemiesEvents(self):
        for enemy in self.enemies:
            if self.player.collideEnemy(enemy):
                if enemy.mode.current is FREIGHT:
                    self.player.visible = False
                    enemy.visible = False
                    self.pause.setPause(pauseTime=1, func=self.showCharacters)
                    enemy.startSpawn()
                    self.inters.allowHomeAccess(enemy)
                    self.score += enemy.points
                elif enemy.mode.current is not SPAWN:
                    if self.player.alive:
                        self.lives -= 1
                        self.player.die()
                        self.enemies.hide()
                        if self.lives <= 0:
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def checkFruitEvents(self):
        if self.nonosses.numEaten == 50 or self.nonosses.numEaten == 100:
            if self.fruit is None:
                self.fruit = Fruit(self.inters.getInterFromTiles(32, 20))
        if self.fruit is not None:
            if self.player.collideCheck(self.fruit):
                self.fruit = None
            elif self.fruit.disappear:
                self.fruit = None

    def nextLevel(self):
        self.showCharacters()
        self.level += 1
        self.pause.paused = True
        self.startGame()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def showCharacters(self):
        self.player.visible = True
        self.enemies.show()

    def hideCharacters(self):
        self.player.visible = False
        self.enemies.hide()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.inters.render(self.screen)
        self.nonosses.render(self.screen)
        self.walls.render(self.screen)
        self.player.render(self.screen)
        self.enemies.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.draw_text("SCORE : ", 40, WHITE, 100, 30)
        self.draw_text(str(self.score), 40, WHITE, 210, 30)
        self.draw_text("NIVEAU : ", 40, WHITE, 100, 80)
        self.draw_text(str(self.level), 40, WHITE, 210, 80)
        self.draw_text("VIES : ", 40, WHITE, 100, 130)
        self.draw_text(str(self.lives), 40, WHITE, 210, 130)
        pg.display.update()

if __name__ == "__main__":
    game = Game()
    game.startGame()
    while game.running:
        game.update()