from abc import abstractmethod, ABCMeta

import pygame

from app_controller import AppController
from . import *
from game.model.languages import Language, get_screen_texts
from game.consts import SCREEN_WIDTH, SCREEN_HEIGHT

class Scene(metaclass=ABCMeta):
    def __init__(self, app_controller: AppController, language: Language, screen_id: str = None):
        self.display_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._app_controller = app_controller
        self.__language = language
        self.__screen_id = screen_id

        self.__text_labels = {}
        self.__text_dict = {}
        self.reset_all_components()
        
    def get_language(self) -> Language:
        return self.__language
    
    def update_language(self, language: Language):
        if language != self.__language:
            self.__language = language
            self.load_text()
            self.define_text_labels()
            self.setup()
            self.display()

    def load_text(self):
        text_data = get_screen_texts(self.__screen_id, self.__language)
        if not text_data:
            raise ValueError(f"Language '{self.__language.lang_id}' not found.")
        if not isinstance(text_data, dict):
            raise ValueError(f"Invalid text data format for language '{self.__language.lang_id}'.")
        self.__text_dict = text_data

    def set_text_label(self, key: str, text_label: pygame.Surface):
            self.__text_labels[key] = text_label

    def get_text_label(self, key: str) -> pygame.Surface:
        if key in self.__text_labels:
            return self.__text_labels[key]
        else:
            return self.__language.get_font(10).render(f"{self.get_language().lang_id}#{key}", True, (255, 255, 255))
        

    @abstractmethod
    def define_text_labels(self) -> pygame.Surface:
        pass

    @abstractmethod
    def setup(self):
        pass

    def define_base_components(self):
        pass

    def get_text(self, key: str) -> str:
        if key in self.__text_dict:
            return self.__text_dict[key]
        else:
            return f"{self.get_language().lang_id}#{key}"

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def tick(self):
        pass

    def on_load(self):
        pass

    
    def reset_all_components(self):
        self.load_text()
        self.define_text_labels()
        self.setup()
        # self.display_surface.fill((0, 0, 0))




class ViewWithSprites(Scene):
    def __init__(self, app_controller: AppController, language: Language):
        super().__init__(app_controller, language)

        self.display_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.all_sprites = pygame.sprite.Group()
        self.reset_all_components()


    def reset_all_components(self):
        self.load_text()
        self.define_text_labels()
        self.setup()
        self.defineComponents()
        self.display_surface.fill((0, 0, 0))
        


    def get_language(self) -> Language:
        return self.__language

    @abstractmethod
    def load_text(self):
        pass

    @abstractmethod
    def define_text_labels(self) -> pygame.Surface:
        pass

    @abstractmethod
    def setup(self):
        pass

    def defineComponents(self):
        pass

    def get_text(self, key: str) -> str:
        if key in self.__text_dict:
            return self.__text_dict[key]
        else:
            print(f"Key '{key}' not found in text dictionary.")
            return key

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def tick(self):
        pass