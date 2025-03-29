import sys
import pygame
from app_controller import AppController
from commons.file_manager import get_static_file_path
from commons.languages import Language
from appstats import ViewManager
from commons.view_transition import *
from screens.game import GameView
from screens.pause import PauseView
from screens.title import TitleView
from settings import *
from commons.view import View
from commons.transition_controller import ViewTransitionSwitcher

pygame.init()
pygame.mouse.set_visible(True)
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("croissant-boy")
pygame.display.set_icon(pygame.image.load(get_static_file_path("icon.png")))

app_stats = ViewManager()
app_controller = AppController(app_stats)

views = [
    TitleView(app_controller, Language.Japanese),
    PauseView(app_controller, Language.Japanese),
    GameView(app_controller, Language.Japanese),
]

def quit():
    print("Exiting...")

    # do something here

    print("All done. Bye!")
    pygame.mixer.quit()
    pygame.font.quit()
    pygame.quit()
    sys.exit()

# current_transition: ViewUpdater = None

while True:
    if pygame.event.get(pygame.QUIT):
        quit()

    showing_view: View = views[app_stats.get_showing_view()]
    showing_screen: int = app_stats.get_showing_view()
    current_transition = app_stats.get_current_transition()

    if current_transition is not None:
        if not current_transition.update():
            app_stats.set_current_transition(None)
            app_stats.set_showing_view(app_stats.get_current_view())

    elif app_stats.get_current_view() != showing_screen:
        first_view: View = showing_view
        second_view: View = views[app_stats.get_current_view()]
        app_stats.set_current_transition(
            ViewTransitionSwitcher(
                SingleSlideTransition(first_view, 0.4, 1),
                RadialTransition(second_view, 1.0),
            )
        )
        continue

    else:
        showing_view.tick()
        showing_view.display()
        pygame.display.get_surface().blit(showing_view.display_surface, (0, 0))
    
    pygame.display.update()
    pygame.time.Clock().tick(FPS)