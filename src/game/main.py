import threading
import pyglet

from common.util.file_manager import *

from game.interface import *
from game.scenes import *
from game.consts import *
from game.app import *

def main():
    config = pyglet.gl.Config(double_buffer=True, depth_size=24, alpha_size=8)
    window = pyglet.window.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, config=config)
    window.set_caption('croissant-boy')
    window.set_icon(pyglet.image.load(get_asset_file_path("icon.png")))

    def load_gbm():
        pyglet.media.load(get_asset_file_path("bgm/Best_Beat.mp3")).play()
    threading.Thread(target=load_gbm).start()

    app_model: AppInterface = AppModel()
    app_model.change_view(TitleScene(app_model))

    # _ に代入することで、AppEventDispatcherのインスタンスを保持する
    _ = AppEventDispatcher(window, app_model)

    def update(_):
        app_model.get_current_view().tick()

    pyglet.clock.schedule_interval(update, 1.0 / SCREEN_FPS)
    pyglet.app.run()

if __name__ == "__main__":
    main()