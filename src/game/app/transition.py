from abc import ABCMeta, abstractmethod
import threading

import pygame

# from game.common.view import Scene
from game.interface.app_interface import AppInterface
from game.interface.scene_interface import App, SceneInterface
from game.interface.transition_interface import TransitionInterface
from game.consts import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS


class ViewTransition(TransitionInterface, metaclass=ABCMeta):
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
        
    def can_transition(self) -> bool:
        return False

    def update(self) -> bool:
        if not self.can_transition():
            return False
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
    def __init__(self, seconds: float):
        super().__init__(seconds)

    def set_view(self, view: SceneInterface):
        self.view = view
    
    def set_view_from_class(self, view: type[SceneInterface], app: AppInterface):
        def get_scene_from_class(view: type[SceneInterface]):
            self.view = view(app)
            print("scene loaded")
        threading.Thread(target=get_scene_from_class, args=(view,)).start()
    
    def can_transition(self) -> bool:
        return self.view is not None

    @abstractmethod
    def transition(self, progress: float):
        pass

    def get_next_view(self) -> SceneInterface:
        return self.view

class View2ViewTransition(ViewTransition, metaclass=ABCMeta):
    def __init__(self, first_view: SceneInterface, seconds: float):
        super().__init__(seconds)
        self.first_view = first_view
        self.showing_view = first_view

    def set_second_view(self, second_view: SceneInterface):
        self.second_view = second_view
    
    def set_seconf_view_from_class(self, view: type[SceneInterface], app_controller: App):
        def get_scene_from_class(view: type[SceneInterface]):
            self.second_view = view(app_controller)
            print("scene loaded")
        threading.Thread(target=get_scene_from_class, args=(view,)).start()
    
    def can_transition(self):
        if self.progress_func(self.current_tick) >= 0.5:
            return self.second_view is not None
        return True
    
    @abstractmethod
    def transition(self, progress: float):
        pass

    def get_next_view(self) -> SceneInterface:
        return self.second_view


# Fade in/out transition
class FadeTransition(SingleViewTransition):
    def transition(self, progress: float):
        alpha = int(255 * progress)
        self.fade_surface.set_alpha(alpha)
        self.view.draw()
        pygame.display.get_surface().blit(self.view.get_root_surface(), (0, 0))
        pygame.display.get_surface().blit(self.fade_surface, (0, 0))


class SingleSlideTransition(SingleViewTransition):
    def __init__(self, seconds: float, direction: int = 1):
        super().__init__(seconds)
        self.direction = direction

    def transition(self, progress: float):
        self.view.draw()

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
        pygame.display.get_surface().blit(self.view.get_root_surface(), (offset_x, offset_y))


# 横からスライドするトランジション
class SlideTransition(View2ViewTransition):
    def __init__(self, first_view: SceneInterface, seconds: float, direction: int = 1):
        super().__init__(first_view, seconds)
        self.direction = direction

    def transition(self, progress: float):
        self.showing_view.draw()
        self.second_view.draw()

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
        showing_root_surface = self.showing_view.get_root_surface()
        second_root_surface = self.second_view.get_root_surface()

        if self.showing_view == self.first_view:
            pygame.display.get_surface().blit(showing_root_surface, (0, 0))
            pygame.display.get_surface().blit(second_root_surface, (offset_x, offset_y))
        else:
            pygame.display.get_surface().blit(showing_root_surface, (offset_x, offset_y))
            pygame.display.get_surface().blit(second_root_surface, (0, 0))


# Radial transition
class RadialTransition(SingleViewTransition):
    def transition(self, progress: float):
        self.view.draw()

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
        pygame.display.get_surface().blit(self.view.get_root_surface(), (0, 0))
        pygame.display.get_surface().blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
