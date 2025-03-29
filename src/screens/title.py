import pygame
from commons.view import View
from commons.file_manager import get_static_file_path
from settings import *

class TitleView(View):
    def load_text(self):
        pass

    def setup(self):
        file_path = get_static_file_path("img/title_logo.png")
        self.title_logo = pygame.transform.scale(
            pygame.image.load(file_path).convert_alpha(), 
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display_surface.fill((100, 150, 30))
        self.display_surface.blit(self.title_logo, (0, 0))
                             

    def display(self):
        pass

    def tick(self):
        if pygame.mouse.get_pressed()[0]:
            pygame.mixer.music.load(get_static_file_path("bgm/bgm_2.mp3"))
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            self._app_controller.set_next_view(2)