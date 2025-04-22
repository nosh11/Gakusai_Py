import pygame
from commons.view import Scene
from consts import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS

class PauseScene(Scene):
    def define_text_labels(self):
        self.font_console = self.get_language().get_font(10)

    def setup(self):
        self.current_tick = 0

    def display(self):
        self.display_surface.fill((224, 224, 224))
        texts = [
            f"ticks: {self.current_tick}, seconds: {self.current_tick / SCREEN_FPS:.2f}, fps={SCREEN_FPS}",
            f"screen={SCREEN_WIDTH}x{SCREEN_HEIGHT}",
        ]
        for text in texts:
            self.display_surface.blit(
                self.font_console.render(text, True, (0, 0, 0))
                , (0, texts.index(text) * 10)
            )


        self.current_tick += 1

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._app_controller.set_transition_type("slide>slide")
                self._app_controller.set_transition_seconds((0.01, 0.01))
                self._app_controller.set_next_view("game")

    def on_load(self):
        pygame.mixer.music.pause()