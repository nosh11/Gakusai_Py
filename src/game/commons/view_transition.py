from abc import ABCMeta, abstractmethod

import pygame

from game.commons.view import Scene
from game.interfaces.view_updater import ViewUpdater
from game.consts import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS


class ViewTransition(ViewUpdater, metaclass=ABCMeta):
    def __init__(self, seconds: float = 1.0):
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        self.ticks = int(seconds * SCREEN_FPS)  # 秒からticksに変換
        self.progress_func = lambda tick: tick / self.ticks
        self.easing_func = lambda x: x
        self.current_tick = 0
    
    # トランジションの進行の向き
    def update_progress_func(self, is_forward: bool):
        if is_forward:
            self.progress_func = lambda tick: tick / self.ticks
        else:
            self.progress_func = lambda tick: 1 - tick / self.ticks

    def update(self) -> bool:
        if self.current_tick >= self.ticks:
            return False
        progress = self.easing_func(self.progress_func(self.current_tick))
        self.transition(progress)
        self.current_tick += 1
        return True
        
    @abstractmethod
    def transition(self, progress: float):
        pass


class SingleViewTransition(ViewTransition, metaclass=ABCMeta):
    def __init__(self, view: Scene, seconds: float):
        super().__init__(seconds)
        self.view = view

    @abstractmethod
    def transition(self, progress: float):
        pass

class View2ViewTransition(ViewTransition, metaclass=ABCMeta):
    def __init__(self, first_view: Scene, second_view: Scene, seconds: float):
        super().__init__(seconds)
        self.first_view = first_view
        self.second_view = second_view
        self.showing_view = first_view

    @abstractmethod
    def transition(self, progress: float):
        pass


# Fade in/out transition
class FadeTransition(SingleViewTransition):
    def transition(self, progress: float):
        alpha = int(255 * progress)
        self.fade_surface.set_alpha(alpha)
        self.view.display()
        pygame.display.get_surface().blit(self.view.display_surface, (0, 0))
        pygame.display.get_surface().blit(self.fade_surface, (0, 0))



class SingleSlideTransition(SingleViewTransition):
    def __init__(self, view: Scene, seconds: float, direction: int = 1):
        super().__init__(view, seconds)
        self.direction = direction

    def transition(self, progress: float):
        
        self.view.display()

        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT

        if self.direction == 1:  # Slide from left to right
            offset_x = int(width * progress)
            offset_y = 0
        elif self.direction == -1:  # Slide from right to left
            offset_x = -int(width * progress)
            offset_y = 0
        elif self.direction == 2:  # Slide from top to bottom
            offset_x = 0
            offset_y = int(height * progress)
        elif self.direction == -2:  # Slide from bottom to top
            offset_x = 0
            offset_y = -int(height * progress)
        else:
            raise ValueError("Invalid direction value. Use 1, -1, 2, or -2.")

        # fill
        pygame.display.get_surface().fill((0, 0, 0))
        pygame.display.get_surface().blit(self.view.display_surface, (offset_x, offset_y))


# 横からスライドするトランジション
class SlideTransition(View2ViewTransition):
    def __init__(self, first_view: Scene, second_view: Scene, seconds: float, direction: int = 1):
        super().__init__(first_view, second_view, seconds)
        self.direction = direction

    def transition(self, progress: float):
        self.showing_view.display()
        self.second_view.display()

        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT

        if self.direction == 1:  # Slide from left to right
            offset_x = int(width * progress)
            offset_y = 0
        elif self.direction == -1:  # Slide from right to left
            offset_x = -int(width * progress)
            offset_y = 0
        elif self.direction == 2:  # Slide from top to bottom
            offset_x = 0
            offset_y = int(height * progress)
        elif self.direction == -2:  # Slide from bottom to top
            offset_x = 0
            offset_y = -int(height * progress)
        else:
            raise ValueError("Invalid direction value. Use 1, -1, 2, or -2.")

        if self.showing_view == self.first_view:
            pygame.display.get_surface().blit(self.showing_view.display_surface, (0, 0))
            pygame.display.get_surface().blit(self.second_view.display_surface, (offset_x, offset_y))
        else:
            pygame.display.get_surface().blit(self.showing_view.display_surface, (offset_x, offset_y))
            pygame.display.get_surface().blit(self.second_view.display_surface, (0, 0))


# Radial transition
class RadialTransition(SingleViewTransition):
    def transition(self, progress: float):
        self.view.display()

        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT

        center_x = width // 2
        center_y = height // 2

        radius = int(((width ** 2 + height ** 2) ** 0.5) * progress)

        # Create a mask
        mask = pygame.Surface((width, height))
        mask.fill((0, 0, 0))
        pygame.draw.circle(mask, (255, 255, 255), (center_x, center_y), radius)

        # Apply the mask
        pygame.display.get_surface().blit(self.view.display_surface, (0, 0))
        pygame.display.get_surface().blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
