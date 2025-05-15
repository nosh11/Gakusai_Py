

import sys
import pygame
from common.model.language import Language
from game.interface.app_interface import AppInterface
from game.interface.scene_interface import SceneInterface
from game.interface.transition_interface import TransitionInterface


class AppModel(AppInterface):
    def __init__(self):
        self.scene: SceneInterface = None
        self.scene_queue: list[SceneInterface] = []
        self.transition: TransitionInterface = None
        self.language: Language = Language.Japanese
    
    def change_scene(self, scene_holder: SceneInterface | type[SceneInterface]):
        if isinstance(scene_holder, type):
            scene = scene_holder(self)
        else:
            scene = scene_holder
        if self.scene is not None:
            self.scene.on_unload()
        self.scene = scene
        self.scene.on_load()

    def change_transition(self, transition: TransitionInterface):
        self.transition = transition

    def change_language(self, language: Language):
        self.language = language

    def get_language(self) -> Language:
        return self.language
    
    def back_scene(self):
        if len(self.scene_queue) > 0:
            self.change_scene(self.scene_queue[-1])
            self.scene_queue.pop()
        else:
            print("No previous scene to go back to.")
    
    def add_scene(self, scene: SceneInterface):
        self.scene_queue.append(self.scene)
        self.change_scene(scene)
    
    def quit(self):
        print("Exiting...")

        # do something here

        print("All done. Bye!")
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.font.quit()
        pygame.quit()
        sys.exit()
        exit(0)

    def update(self):
        if pygame.event.get(pygame.QUIT):
            self.quit()

        elif self.transition != None:
            if not self.transition.update():
                self.change_scene(self.transition.get_next_view())
                self.scene = self.transition.get_next_view()
                self.transition = None
        else:
            self.scene.tick()
            pygame.display.get_surface().blit(self.scene.get_root_surface(), (0, 0))