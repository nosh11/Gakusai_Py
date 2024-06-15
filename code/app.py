# 銃で敵を殴ろう！
import settings

import pygame, sys
from settings import *
from level import Level
from pause import Pause
from appstate import AppState

class App:
    def __init__(self):
        # Screen の基本設定
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("睡眠力バトル")
        pygame.display.set_icon(pygame.image.load("img/bed.png"))
        title_bed = pygame.transform.scale(pygame.image.load('img/bed.png'), (200, 200))
        self.screen.blit(title_bed, ((SCREEN_WIDTH-1000)//2, (SCREEN_HEIGHT-200)//2))
        title = pygame.transform.scale(pygame.image.load('img/suiminryoku.png'), (600, 200))
        self.screen.blit(title, ((SCREEN_WIDTH-600)//2, (SCREEN_HEIGHT-200)//2))
        pygame.display.update()
        # Level
        self.app_state = AppState("level")
        self.level = Level(self.app_state)
        self.pause = Pause(self.app_state)
        self.states = {"level": self.level, "pause": self.pause}
        pygame.time.wait(3000)
        
        self.bgm = pygame.mixer.Sound("bgm/BGM_1.mp3")
        self.bgm.play()

    def run(self):
        while True:
            # Event Handler
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Main Gameloop
            dt = self.clock.tick() / 1000
            self.states[self.app_state.get()].run(dt)
            pygame.display.update()

if __name__ == "__main__":
    root = App()
    root.run()