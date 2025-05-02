from abc import ABCMeta, abstractmethod
import pygame
from common.util.file_manager import get_asset_file_path
from game.utils.image_processor import BrightnessProcessor
from game.interface.observe import Observable

class UIWidget(metaclass=ABCMeta):
    def __init__(self, view_display_surface: pygame.Surface, x, y):
        self.view_display_surface = view_display_surface
        self.pos = (x, y)
        self.showing_image = None
        self.is_hidden = False

    def get_showing_image(self) -> pygame.Surface:
        if self.showing_image is None:
            return pygame.Surface((0, 0)).set_colorkey((0, 255, 0))
        return self.showing_image

    def set_showing_image(self, image: pygame.Surface):
        self.showing_image = image
    
    @abstractmethod
    def update(self) -> bool:
        pass

    def draw(self) -> None:
        if not self.is_hidden:
            self.view_display_surface.blit(self.get_showing_image(), self.pos)


class SurfaceWithText:
    def __init__(self, text, font: pygame.font.Font, color=(255, 255, 255)):
        self.text_surface = font.render(text, True, color)


class UIWidgetHoberable(UIWidget):
    def __init__(self, view_display_surface: pygame.Surface, x, y):
        super().__init__(view_display_surface, x, y)
        self.image_normal: pygame.Surface = None
        self.image_brighten: pygame.Surface = None

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        pass

    def is_collide(self):
        pos = pygame.mouse.get_pos()
        return self.get_rect().collidepoint(pos)

    def update(self) -> bool:
        super().update()
        collide_flag = self.is_collide()

        if collide_flag:
            # マウスがボタン上にある
            self.showing_image = self.image_brighten

        else:
            # マウスがボタン上にない
            self.showing_image = self.image_normal

        # ボタンを描画
        return collide_flag
    
    
    


class UIWidgetClickable(UIWidgetHoberable, Observable):
    def __init__(self, view_display_surface: pygame.Surface, x, y):
        super().__init__(view_display_surface, x, y)
        Observable.__init__(self)
        self.clicked = False

    @abstractmethod
    def get_rect(self):
        pass

    def on_clicked(self):
        self.notify_observers()
        
    def update(self) -> bool:
        collide_flag = super().update()
        current_pressed = pygame.mouse.get_pressed()[0]
        if current_pressed and collide_flag:
            self.clicked = True
        elif not current_pressed and self.clicked:
            self.clicked = False
            self.on_clicked()
        return collide_flag

    
class Button(UIWidgetClickable, SurfaceWithText):
    @staticmethod
    def text_button(font: pygame.font.Font, text: str) -> pygame.Surface:
        image = pygame.image.load(get_asset_file_path("img/button.png"))
        text_surface = font.render(text, True, (255, 255, 255))
        width = image.get_width()
        height = image.get_height()
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_pos = ((width - text_width) // 2, (height - text_height) // 2)
        image.blit(text_surface, text_pos)
        return image

    def __init__(self, view_display_surface: pygame.Surface, x, y, text, font: pygame.font.Font):
        UIWidgetClickable.__init__(self, view_display_surface, x, y)
        SurfaceWithText.__init__(self, text, font)
        Observable.__init__(self)

        self.image_normal = self.text_button(font, text)
        self.image_brighten = BrightnessProcessor(self.image_normal).process(30)
        self.showing_image = self.image_normal
        self.rect = self.showing_image.get_rect().move(self.pos)
    
    def get_rect(self) -> pygame.Rect:
        return self.rect

    def get_showing_image(self) -> pygame.Surface:
        return self.showing_image
    
    def get_rect(self) -> pygame.Rect:
        return self.rect
    
