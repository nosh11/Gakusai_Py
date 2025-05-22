import pygame
from game.app import AppModel
from util import get_asset_file_path
from game.scenes import TitleScene
from game.consts import *

def main():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, 32, 0)
    pygame.display.set_caption("croissant-boy")
    pygame.display.set_icon(pygame.image.load(get_asset_file_path("icon.png")))

    app = AppModel()
    app.change_scene(TitleScene(app))
    
    while True:
        app.update()
        pygame.display.update()
        pygame.time.Clock().tick(SCREEN_FPS)

if __name__ == "__main__":
    main()
    pygame.quit()
    exit(0)