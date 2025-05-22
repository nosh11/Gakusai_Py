from abc import ABCMeta, abstractmethod

import pygame


class ImageProcessor(metaclass=ABCMeta):
    def __init__(self, image: pygame.Surface):
        self.image = image

    @abstractmethod
    def process(self) -> pygame.Surface:
        pass