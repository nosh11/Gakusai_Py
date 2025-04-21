import pygame
from game.app_controller import AppController
from game.app_state import AppStats as stats
from common.utils.file_manager import get_static_file_path
from game.interfaces.view_updater import ViewUpdater
from game.model.languages import Language
from game.commons.view_transition import FadeTransition, SingleSlideTransition, RadialTransition, SlideTransition
from game.screens import *
from game.consts import *
from game.commons.view import View
from game.commons.transition_controller import ViewTransitionSwitcher

def main():
    # Initialize pygame
    pygame.init()
    pygame.mouse.set_visible(True)
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, 32, 0)
    pygame.display.set_caption("croissant-boy")
    pygame.display.set_icon(pygame.image.load(get_static_file_path("icon.png")))

    app_controller = AppController()

    views = {
        "title": TitleView(app_controller, Language.Japanese, "title"),
        "pause": PauseView(app_controller, Language.Japanese, "pause"),
        "game": GameView(app_controller, Language.Japanese, "game"),
        "sound_room": SoundRoomView(app_controller, Language.Japanese, "sound_room"),
        "map": MapView(app_controller, Language.Japanese, "map"),
        "options": OptionView(app_controller, Language.Japanese, "options"),
    }
    pygame.mixer.music.load(get_static_file_path("bgm/Best_Beat.mp3"))
    pygame.mixer.music.play(-1)

    while True:
        if pygame.event.get(pygame.QUIT):
            app_controller.quit()
            break

        showing_view: View = views[stats.showing_view]
        showing_screen: str = stats.showing_view
        current_transition = stats.current_transition

        if stats.current_lang != showing_view.get_language():
            for _, view in views.items():
                view: View
                view.update_language(stats.current_lang)

        if current_transition is not None:
            if not current_transition.update():
                stats.current_transition = None
                stats.showing_view = stats.current_view
                views[stats.current_view].on_load()

        elif stats.current_view != showing_screen:
            view_list = [showing_view, views[stats.current_view]]

            transition_script = app_controller.get_transition_type()

            transition: ViewUpdater = None
            transition_second = app_controller.get_transition_seconds()

            if ">" in transition_script:
                transitions = transition_script.split(">")
                for i in range(len(transitions)):
                    if transitions[i] == "radial":
                        transitions[i] = RadialTransition(
                            view_list[i], transition_second[i]
                        )
                    elif transitions[i] == "fade":
                        transitions[i] = FadeTransition(
                            view_list[i], transition_second[i]
                        )
                    elif transitions[i] == "slide":
                        transitions[i] = SingleSlideTransition(
                            view_list[i], transition_second[i], 1
                        )
                transition = ViewTransitionSwitcher(
                    transitions[0], transitions[1]
                )
            else:
                if transition_script == "slide_in":
                    transition = SlideTransition(
                        view_list[0], view_list[1], transition_second[0], transition_second[1]
                    )
                elif transition_script  == "radial":
                    transition = RadialTransition(
                        view_list[0], transition_second[0]
                    )
                elif transition_script == "fade":
                    transition = FadeTransition(
                        view_list[0], transition_second[0]
                    )
                elif transition_script == "slide":
                    transition = SingleSlideTransition(
                        view_list[0], transition_second[0], 2
                    )
            stats.current_transition = transition
            continue

        else:
            showing_view.tick()
            showing_view.display()
            pygame.display.get_surface().blit(showing_view.display_surface, (0, 0))
            
        pygame.display.update()
        pygame.time.Clock().tick(SCREEN_FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
    exit(0)