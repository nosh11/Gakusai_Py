from game.interface.scene_interface import SceneInterface


class TransitionInterface:
    def update(self) -> bool:
        pass

    def get_next_view(self) -> SceneInterface:
        pass
