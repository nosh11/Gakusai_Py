import sys
import pygame
from model.languages import Language
import app_state

class AppController:
    def __init__(self):
        self.__transition_type: str = "slide"
        self.__transition_seconds = (1.0, 1.0)

    def set_next_view(self, view: str):
        app_state.current_view = view
    
    def set_language(self, lang: Language):
        app_state.current_lang = lang

    def set_transition_type(self, transition_type: str):
        self.__transition_type = transition_type

    def get_transition_type(self) -> str:
        return self.__transition_type 
    
    def set_transition_seconds(self, seconds: tuple[float, float]):
        self.__transition_seconds = seconds

    def get_transition_seconds(self):
        return self.__transition_seconds

    def quit(self):
        print("Exiting...")

        # do something here

        print("All done. Bye!")
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.quit()
        sys.exit()