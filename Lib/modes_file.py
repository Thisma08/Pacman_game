from constants_file import *
from enemies_file import *

class MainMode(object):
    def __init__(self):
        self.timer = 0
        self.scatter()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        self.mode = SCATTER
        self.duration = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.duration = 20
        self.timer = 0

class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.duration = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    def setFreightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.duration = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.timer >= self.duration:
                self.duration = None
                self.entity.normalMode()
                self.current = self.mainmode.mode
        else:
            self.current = self.mainmode.mode

