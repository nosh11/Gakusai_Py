from abc import ABCMeta, abstractmethod
import pygame

class ImageProcessor(metaclass=ABCMeta):
    def __init__(self, image: pygame.Surface):
        self.image = image

    @abstractmethod
    def process(self) -> pygame.Surface:
        pass

class BrightnessProcessor(ImageProcessor):
    def process(self,  brighten: int) -> pygame.Surface:
        new_image = self.image.copy()
        width, height = new_image.get_size()
        
        for x in range(width):
            for y in range(height):
                r, g, b, a = new_image.get_at((x, y))
                r = max(0, min(255, r + brighten))
                g = max(0, min(255, g + brighten))
                b = max(0, min(255, b + brighten))
                new_image.set_at((x, y), (r, g, b, a))
        
        return new_image

class ImageProcessorFactory:
    def create_processor(self, image: pygame.Surface, processor_type: str) -> ImageProcessor:
        if processor_type == "brightness":
            return BrightnessProcessor(image)
        else:
            raise ValueError("Invalid processor type")