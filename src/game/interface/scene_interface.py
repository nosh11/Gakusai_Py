import pygame
from common.model.language import Language


class SceneInterface:
    def __init__(self, app_controller, language: Language, screen_id: str = None):
        """
        Initialize the scene interface.
        :param app_controller: The application controller instance.
        :param language: The current language of the scene.
        :param screen_id: The ID of the screen (optional).
        """
        pass

    def get_language(self) -> Language:
        """
        Get the current language of the scene.
        :return: The current language.
        """
        raise NotImplementedError("This method should be overridden in subclasses")
    
    def update_language(self, language: Language):
        """
        Update the language of the scene and reload text data.
        :param language: The new language to set.
        """
        raise NotImplementedError("This method should be overridden in subclasses")

    def load_text(self):
        """
        Load text data for the current language.
        This method should be overridden in subclasses to provide specific text data.
        """
        raise NotImplementedError("This method should be overridden in subclasses")

    def set_text_label(self, key: str, text_label: pygame.Surface):
        """
        Set a text label for a specific key.
        :param key: The key for the text label.
        :param text_label: The text label to set.
        """
        raise NotImplementedError("This method should be overridden in subclasses")

    def get_text_label(self, key: str) -> pygame.Surface:
        raise NotImplementedError("This method should be overridden in subclasses")

    def define_text_labels(self) -> pygame.Surface:
        raise NotImplementedError("This method should be overridden in subclasses")

    def setup(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    def define_base_components(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    def get_text(self, key: str) -> str:
        raise NotImplementedError("This method should be overridden in subclasses")

    def display(self):
        raise NotImplementedError("This method should be overridden in subclasses")

    def tick(self):
        pass

    def on_load(self):
        pass

    def on_unload(self):
        pass

    def reset_all_components(self):
        self.load_text()
        self.define_text_labels()
        self.setup()

