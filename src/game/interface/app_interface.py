from game.interface.scene_interface import SceneInterface
from game.interface.transition_interface import TransitionInterface


class AppInterface:
    def get_current_view(self) -> SceneInterface:
        pass

    def get_current_transition(self) -> TransitionInterface:
        pass

    def change_view(self, view: SceneInterface):
        pass

    def change_transition(self, transition: TransitionInterface):
        pass

    def quit(self):
        pass

    def draw(self):
        pass