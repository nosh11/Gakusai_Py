import pygame
from game.app_controller import AppController
from game.app_state import AppStats as stats
from common.util.file_manager import get_asset_file_path
from common.model.language import Language
from game.scenes import *
from game.consts import *

def main():
    pygame.init()
    pygame.mouse.set_visible(True)
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, 32, 0)
    pygame.display.set_caption("croissant-boy")
    pygame.display.set_icon(pygame.image.load(get_asset_file_path("icon.png")))

    app_controller = AppController()
    stats.set_view(TitleScene(app_controller, Language.Japanese, "title"))

    pygame.mixer.music.load(get_asset_file_path("bgm/Best_Beat.mp3"))
    pygame.mixer.music.play(-1)

    while True:
        if pygame.event.get(pygame.QUIT):
            app_controller.quit()
            break

        if stats.current_lang != stats.current_view.get_language():
            stats.current_view.update_language(stats.current_lang)

        if stats.current_transition is not None:
            if not stats.current_transition.update():
                stats.current_view = stats.current_transition.get_next_view()
                stats.current_view.on_load()
                stats.current_transition = None

        else:
            stats.current_view.tick()
            stats.current_view.display()
            pygame.display.get_surface().blit(stats.current_view.display_surface, (0, 0))
            
        pygame.display.update()
        pygame.time.Clock().tick(SCREEN_FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
    exit(0)