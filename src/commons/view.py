
from abc import ABC, abstractmethod, ABCMeta

import pygame

from app_controller import AppController
from settings import *
from commons.languages import Language

class View(metaclass=ABCMeta):
    def __init__(self, app_controller: AppController, language: Language):
        self.display_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.all_sprites = pygame.sprite.Group()
        self.all_nocollide_sprites = pygame.sprite.Group()
        self.sound_channel = pygame.mixer.Channel(0)
        self._app_controller = app_controller
        self.__language = language
        self.update_language(language)
        self.load_text()
        self.setup()

    def get_language(self) -> Language:
        return self.__language
    
    def update_language(self, lang):
        self.__language = lang
        self.load_text()

    @abstractmethod
    def load_text(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def tick(self):
        pass
