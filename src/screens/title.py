import pygame
from commons.view import View
from settings import *

class TitleView(View):
    def load_text(self):
        pass

    def setup(self):
        self.title_logo = pygame.transform.scale(
            pygame.image.load("static/img/title_logo.png"), 
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display_surface.fill((100, 150, 30))
        self.display_surface.blit(self.title_logo, (0, 0))
                             

    def display(self):
        pass

    def tick(self):
        if pygame.mouse.get_pressed()[0]:
            pygame.mixer.music.load("static/bgm/bgm_2.mp3")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            self._view_manager.set_current_view(1)