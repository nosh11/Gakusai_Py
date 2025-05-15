import pygame

from abc import ABC, abstractmethod

from game.interface.app_interface import AppInterface
from game.interface.scene_interface import SceneInterface
from game.consts import SCREEN_WIDTH, SCREEN_HEIGHT


class Scene(SceneInterface, ABC):
    @abstractmethod
    def get_screen_id(self) -> str:
        pass

    @abstractmethod
    def setup(self):
        pass

    def __init__(self, app: AppInterface):
        self.root_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.app = app
        self.language = app.get_language()
        self.setup()
        self.draw()

    def get_root_surface(self):
        return self.root_surface