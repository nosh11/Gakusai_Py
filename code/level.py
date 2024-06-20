import pygame
from settings import *
from player import Player
from entities import Bed, Mob
from ui import Button
from appstate import AppState

class Level:
    def __init__(self, app_state: AppState):
        self.app_state = app_state
        self.change = True

        # Display Surface を取得
        self.display_surface = pygame.display.get_surface()
        # Sprite Group を定義
        self.all_sprites = pygame.sprite.Group()
        self.all_nocollide_sprites = pygame.sprite.Group()
        # Setup
        self.setup()

    def setup(self):
        self.player = Player(((SCREEN_WIDTH-900)//2, (SCREEN_HEIGHT+300)//2), self.all_sprites)
        self.bed = Bed((140, 260), self.all_nocollide_sprites, self.all_sprites)
        Mob(((SCREEN_WIDTH)//2, (SCREEN_HEIGHT-500)//2), self.all_sprites,"blue_cloth_guy", (60, 60), 100)
        self.button = []
        for i in range(2):
            self.button.append(Button(50, 600, pygame.image.load(f'img/bullet_levelup_{i}.png'), 3))
        self.pause_button = Button(5, 5, pygame.image.load('img/setting.png'), 3)
    
    def run(self, dt):
        self.display_surface.fill((224,224,224))
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
        self.all_nocollide_sprites.draw(self.display_surface)
        self.all_nocollide_sprites.update(dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.app_state.set("pause")
        if self.button[self.app_state.lang].draw():
            print("Clicked!")
        if self.pause_button.draw():
            self.app_state.set("pause")