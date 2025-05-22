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

    def setup(self):
        self.current_tick = 0
        self.font_console = pygame.font.Font(self.app.get_language().get_font(), 20)

    def display(self):
        self.root_surface.fill((224, 224, 224))
        texts = [
            f"frame={self.current_tick},seconds={self.current_tick / SCREEN_FPS:.2f},fps={SCREEN_FPS}",
            f"screen={SCREEN_WIDTH}x{SCREEN_HEIGHT}",
        ]
        for text in texts:
            self.root_surface.blit(
                self.font_console.render(text, True, (0, 0, 0))
                , (0, texts.index(text) * 20)
            )


        self.current_tick += 1

    def tick(self):
        self.display()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.app.back_scene()

    def on_load(self):
        pygame.mixer.music.pause()