import pygame

class ViewManager:
    def __init__(self):
        super().__init__()
        self.__current_view = 0
        self.__current_lang = "Japanese"

    def set_bgm(self, music: str):
        pygame.mixer.music.load(music)

    def get_current_view(self) -> int:
        return self.__current_view
    
    def set_current_view(self, view: int):
        self.__current_view = view

    def get_current_lang(self) -> str:
        return self.__current_lang
    
    def set_current_lang(self, lang: str):
        self.__current_lang = lang