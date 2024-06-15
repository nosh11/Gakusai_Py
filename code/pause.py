import pygame
from settings import *
from player import Player
from entities import Bed
from appstate import AppState
from ui import Button

class Pause:
    def __init__(self, appstate: AppState):
        self.appstate = appstate
        # Display Surface を取得
        self.display_surface = pygame.display.get_surface()
        # Sprite Group を定義
        self.all_sprites = pygame.sprite.Group()
        # Setup
        self.setup()

    def setup(self):
        font = pygame.font.Font('font/TsukimiRounded-Medium.ttf', 32)
        self.label = {0: [], 1: []}
        self.start_button = []
        self.language_button = []
        button = pygame.image.load('img/button.png')
        for i in range(2):
            for line in HOW_TO_PLAY[i]:
                self.label[i].append(font.render(line, True, (255,255,255)))
            self.start_button.append(Button(100, 500, button, 1, BACK[i]))
            self.language_button.append(Button(100, 400, button, 1, LANG[i]))

    def run(self, dt):
        lang = self.appstate.lang
        self.display_surface.fill((112,112,112))
        for line in range(len(self.label[lang])):
            label: pygame.surface.Surface = self.label[lang][line]
            pos = ((SCREEN_WIDTH-label.get_rect().size[0])//2,SCREEN_HEIGHT//4+(line*32)+(15*line))
            self.display_surface.blit(label,pos)
        if self.start_button[lang].draw():
            self.appstate.set("level")
        if self.language_button[lang].draw():
            self.appstate.lang = (lang + 1) % 2
