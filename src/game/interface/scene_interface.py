import pygame

class SceneInterface:
    def draw(self):
        pass

    def tick(self):
        pass

    def setup(self):
        pass

    def on_load(self):
        pass

    def on_unload(self):
        pass

    def get_root_surface(self) -> pygame.Surface:
        pass