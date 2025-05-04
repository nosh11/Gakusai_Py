from game.interface import AppInterface
from game.interface.scene_interface import SceneInterface

from abc import ABC, abstractmethod
class TitleChoice(ABC):
    def __init__(self, app: AppInterface, name: str):
        self.app: AppInterface = app
        self.name: str = name

    @abstractmethod
    def on_select(self):
        pass

class TitleChoiceSceneChange(TitleChoice):
    def __init__(self, app: AppInterface, name: str, scene_class: type[SceneInterface]):
        super().__init__(app, name)
        self.scene_class = scene_class

    def on_select(self):
        self.app.change_view(self.scene_class(self.app))