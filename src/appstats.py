import pygame

from commons.interfaces import ViewUpdater

class ViewManager:
    def __init__(self):
        super().__init__()
        self.__current_view = 0
        self.__showing_view = 0
        self.__current_lang = "Japanese"
        self.__current_transition: ViewUpdater = None

    def set_bgm(self, music: str):
        pygame.mixer.music.load(music)

    def get_showing_view(self) -> int:
        return self.__showing_view
    
    def set_showing_view(self, view: int):
        self.__showing_view = view

    def get_current_view(self) -> int:
        return self.__current_view
    
    def set_current_view(self, view: int):
        if self.__current_transition is not None:
            return
        self.__current_view = view

    def get_current_transition(self) -> ViewUpdater:
        return self.__current_transition
    
    def set_current_transition(self, transition):
        self.__current_transition = transition

    def get_current_lang(self) -> str:
        return self.__current_lang
    
    def set_current_lang(self, lang: str):
        self.__current_lang = lang