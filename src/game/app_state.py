from game.interfaces.view_updater import ViewUpdater
from game.model.languages import Language

class AppStats:
    current_view = "title"
    showing_view = "title"
    current_lang = Language.Japanese
    current_transition: ViewUpdater = None
    flags = {}