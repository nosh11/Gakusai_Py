from game.interface.scene_interface import SceneInterface
from abc import ABC, abstractmethod


class TransitionInterface(ABC):
    @abstractmethod
    def update(self) -> bool:
        pass

    @abstractmethod
    def get_next_view(self) -> SceneInterface:
        pass
