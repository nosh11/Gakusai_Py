from abc import ABC, abstractmethod

from core.model.language import Language
from game.interface.scene_interface import App, SceneInterface
from game.interface.transition_interface import TransitionInterface

class AppInterface(App, ABC):
    @abstractmethod
    def change_scene(self, scene: SceneInterface | type[SceneInterface]):
        pass

    @abstractmethod
    def change_transition(self, transition: TransitionInterface):
        pass

    @abstractmethod
    def change_language(self, language: Language):
        pass

    @abstractmethod
    def get_language(self) -> Language:
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def back_scene(self):
        pass
    
    @abstractmethod
    def add_scene(self, scene: SceneInterface):
        pass