import pygame, sys
from settings import *
from level import Level
from pause import Pause
from appstate import AppState
from ui import Button
from entities import Bed

class App:
    def __init__(self):
        # Screen の基本設定
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("睡眠力バトル")
        pygame.display.set_icon(pygame.image.load("img/bed.png"))

        # タイトル表示 / Level の読み込み
        title = pygame.transform.scale(pygame.image.load('img/suiminryoku.png'), (600, 200))
        self.screen.blit(title, ((SCREEN_WIDTH-600)//2, (SCREEN_HEIGHT-200)//2))
        pygame.display.update()
        self.app_state = AppState("level")
        self.level = Level(self.app_state)
        self.pause = Pause(self.app_state)
        self.states = {"level": self.level, "pause": self.pause}
        self.bgm = pygame.mixer.Sound("bgm/BGM_1.mp3")
        pygame.time.wait(3000)
        font = pygame.font.Font('font/unifont.otf', 32)
        btn = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT-200//2, font.render("CLICK HERE", True, (255,255,255)), 3)
        while True:
            if btn.draw():
                break
            self.screen.blit(title, ((SCREEN_WIDTH-600)//2, (SCREEN_HEIGHT-200)//2))
            self.clock.tick()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
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