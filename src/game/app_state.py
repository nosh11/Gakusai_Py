from commons.interfaces import ViewUpdater
from model.languages import Language

current_view = "title"
showing_view = "title"
current_lang = Language.Japanese
current_transition: ViewUpdater = None
flags = {}