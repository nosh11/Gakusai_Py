import pygame
from commons.view import View
from commons.languages import Language
from commons.observe import Observer
from settings import *
from commons.widget import Button

class PauseView(View, Observer):
    def load_text(self):
        self.font_console = self.get_language().get_font(10)
        self.language_button = Button(self.display_surface, 100, 400, 
                                      self.get_language().get_display_name(),
                                      self.get_language().get_font(20))
        self.language_button.add_observer(self)

    def setup(self):
        self.current_tick = 0

    def display(self):
        self.display_surface.fill((224, 224, 224))
        texts = [
            f"ticks: {self.current_tick}, seconds: {self.current_tick / FPS:.2f}, fps={FPS}",
            f"screen={SCREEN_WIDTH}x{SCREEN_HEIGHT}",
        ]
        for text in texts:
            self.display_surface.blit(
                self.font_console.render(text, True, (0, 0, 0))
                , (0, texts.index(text) * 10)
            )

        self.language_button.update()
        self.language_button.draw()


        self.current_tick += 1

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._app_controller.set_next_view(2)

    def update(self, o):
        if o == self.language_button and not self.language_button.clicked:
            languages = list(Language)
            lang = languages[(languages.index(self.get_language()) + 1) % len(languages)]
            self.update_language(lang)