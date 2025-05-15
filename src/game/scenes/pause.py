import pygame
from game.app.scene import Scene
from game.app.transition_controller import ViewTransitionSwitcher
from consts import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS
from game.app.transition import FadeTransition

class PauseScene(Scene):
    def get_screen_id(self):
        return "pause"

    def __init__(self, app):
        super().__init__(app)

    def define_text_labels(self):
        self.font_console = pygame.font.Font(self.get_language().get_font(), 10)

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
                from game.scenes.title.title import TitleScene
                t = [FadeTransition(0.5), FadeTransition(0.5)]
                t[0].set_view(self)
                t[1].set_view_from_class(TitleScene, self._app_controller, self.get_language(), "title")
                self._app_controller.set_transition(ViewTransitionSwitcher(t[0], t[1]))

    def on_load(self):
        pygame.mixer.music.pause()