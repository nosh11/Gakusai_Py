from abc import ABC, abstractmethod

import pyglet

from game.interface import AppInterface
from game.interface.scene_interface import SceneInterface


class Scene(SceneInterface, ABC):
    def __init__(self, app: AppInterface):
        super().__init__()
        self.app = app
        self.surface = pyglet.graphics.Batch()
        self.screen_id: str = self.get_screen_id()
    
    @abstractmethod
    def get_screen_id(self) -> str:
        pass