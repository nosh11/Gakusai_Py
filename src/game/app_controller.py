import sys
import pygame
from common.model.language import Language
from game.interface.scene_interface import SceneInterface
from game.interface.transition_interface import TransitionInterface
from game.app_state import AppStats as stats

class AppController:
    def set_next_view(self, view: SceneInterface):
        stats.current_view = view
    
    def set_language(self, lang: Language):
        stats.current_lang = lang

    def set_transition(self, transition: TransitionInterface):
        stats.current_transition = transition

    def quit(self):
        print("Exiting...")

        # do something here

        print("All done. Bye!")
        pygame.mixer.quit()
        pygame.font.quit()
        pygame.quit()
        sys.exit()