from game.interface.app_interface import AppInterface
from game.interface.scene_interface import SceneInterface
from game.interface.transition_interface import TransitionInterface
from common.model.language import Language

class AppModel(AppInterface):
    def __init__(self):
        self.current_view: SceneInterface = None
        self.current_transition: TransitionInterface = None
        self.current_lang: Language = None

    def get_current_view(self):
        return self.current_view
    
    def get_current_transition(self):
        return self.current_transition
    
    def get_current_lang(self):
        return self.current_lang

    def change_view(self, view: SceneInterface):
        self.current_view = view
        self.current_view.setup()

    def change_transition(self, transition: TransitionInterface):
        self.current_transition = transition

    def draw(self):
        if self.current_view:
            self.current_view.draw()
        if self.current_transition:
            self.current_transition.update()
            if self.current_transition.update():
                self.change_view(self.current_transition.get_next_view())