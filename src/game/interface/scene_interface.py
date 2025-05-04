import pyglet
from common.model.language import Language
from abc import ABC, abstractmethod

class SceneInterface:
    def tick(self):
        pass

    def get_event_handlers(self) -> dict:
        """
        Returns a dictionary of event handlers.
        The keys are the event names, and the values are the handler functions.
        """
        return {}
    
    def setup(self):
        """
        Called when the scene is set up.
        This is where you can initialize your scene.
        """
        pass

    def draw(self):
        """
        Called when the scene is drawn.
        This is where you can draw your scene.
        """
        pass