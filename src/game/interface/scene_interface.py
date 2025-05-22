import pygame

from abc import ABC, abstractmethod

class App:
    pass

class SceneInterface(ABC):
    def __init__(self, app: App):
        self.app = app

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    def on_load(self):
        pass

    def on_unload(self):
        pass

    @abstractmethod
    def get_root_surface(self) -> pygame.Surface:
        pass