from game.interface.scene_interface import SceneInterface
from game.interface.transition_interface import TransitionInterface
from common.model.language import Language

class AppStats:
    current_view: SceneInterface = None
    current_lang = Language.Japanese
    current_transition: TransitionInterface = None

    @staticmethod
    def set_view(view: SceneInterface):
        if AppStats.current_view == view:
            return
        if AppStats.current_view is not None:
            # AppStats.current_view.on_unload()
            pass
        AppStats.current_view = view
        AppStats.current_view.on_load()

    cureent_bgm: str = None
    flags = {}