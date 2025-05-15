from abc import ABC, abstractmethod

import pygame
from game.interface.app_interface import AppInterface
from game.interface.scene_interface import SceneInterface
from game.interface.transition_interface import TransitionInterface


class Choice(ABC):
    def __init__(self, app: AppInterface, name: str):
        print(f"Choice: {name}")
        self.app = app
        self.label: pygame.Surface = pygame.font.Font(self.app.get_language().get_font(), 50).render(name, True, (0, 0, 0, 255))
    
    @abstractmethod
    def on_select(self):
        pass

class SceneChangeChoice(Choice):
    def __init__(self, app, name, scene_holder: SceneInterface | type[SceneInterface]):
        super().__init__(app, name)
        self.scene_holder = scene_holder
        
    def on_select(self):
        self.app.change_scene(self.scene_holder)

class ScenePushChoice(SceneChangeChoice):
    def __init__(self, app, name, scene_holder: SceneInterface | type[SceneInterface]):
        super().__init__(app, name, scene_holder)

    def on_select(self):
        self.app.add_scene(self.scene_holder)

class SceneBackChoice(Choice):
    def __init__(self, app, name):
        super().__init__(app, name)

    def on_select(self):
        self.app.back_scene()

class SceneTransitionChoice(Choice):
    def __init__(self, app, name, transition: TransitionInterface):
        super().__init__(app, name)
        self.transition = transition

    def on_select(self):
        self.app.change_transition(self.transition)

class QuitChoice(Choice):
    def on_select(self):
        self.app.quit()