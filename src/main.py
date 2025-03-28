import sys
import pygame
from commons.languages import Language
from appstats import ViewManager
from commons.view_transition import *
from screens.pause import PauseView
from screens.title import TitleView
from settings import *
from commons.view import View

pygame.init()
pygame.mouse.set_visible(True)
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("APPLU")
pygame.display.set_icon(pygame.image.load("static/icon.png"))

app_stats = ViewManager()
showing_screen = app_stats.get_current_view()

views = [
    TitleView(app_stats, Language.Japanese),
    PauseView(app_stats, Language.Japanese)
]

def quit():
    print("Exiting...")

    # do something here

    print("All done. Bye!")
    pygame.mixer.quit()
    pygame.font.quit()
    pygame.quit()
    sys.exit()

class ViewTransitionSingle(ViewUpdater):
    def __init__(self, transition: ViewTransition):
        self.transition = transition

    def update(self) -> bool:
        is_transitioning = self.transition.update()
        if not is_transitioning:
            global showing_screen
            showing_screen = app_stats.get_current_view()
        return is_transitioning

class ViewTransitionSwitcher(ViewUpdater):
    def __init__(self, transition_in: SingleViewTransition, transition_out: SingleViewTransition):
        transition_in.update_progress_func(True)
        transition_out.update_progress_func(False)
        self.transitions = [transition_in, transition_out]
        self.current_transition = 0

    def update(self) -> bool:
        if self.transitions[self.current_transition].update():
            return True
        elif self.current_transition == 0:
            global showing_screen
            showing_screen = app_stats.get_current_view()
            self.current_transition = 1
            return True
        else:
            return False

current_transition: ViewUpdater = None

while True:
    if pygame.event.get(pygame.QUIT):
        quit()

    showing_view: View = views[showing_screen]

    if current_transition is not None:
        
        if not current_transition.update():
            current_transition = None

    elif app_stats.get_current_view() != showing_screen:
        first_view: View = showing_view
        second_view: View = views[app_stats.get_current_view()]
        current_transition = ViewTransitionSwitcher(
            SingleSlideTransition(first_view, 0.4, 1),
            RadialTransition(second_view, 1.0),
        )
        continue

    else:
        showing_view.tick()
        showing_view.display()
        pygame.display.get_surface().blit(showing_view.display_surface, (0, 0))
    
    pygame.display.update()
    pygame.time.Clock().tick(FPS)