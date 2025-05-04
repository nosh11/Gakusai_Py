import pyglet
from game.interface.app_interface import AppInterface

class AppEventDispatcher:
    def __init__(self, window, app_model: AppInterface):
        self.window = window
        self.app_model = app_model
        window.push_handlers(self)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
            return
        current_scene = self.app_model.get_current_view()
        handlers = current_scene.get_event_handlers()
        if "on_key_press" in handlers:
            handlers["on_key_press"](symbol, modifiers)
    
    def on_draw(self):
        self.window.clear()
        self.app_model.draw()