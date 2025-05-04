from common.util.file_manager import get_asset_file_path
from game.interface import AppInterface
from game.common.scene import Scene
from game.consts import SCREEN_WIDTH, SCREEN_HEIGHT
import pyglet
from game.scenes.title.choice import TitleChoice, TitleChoiceSceneChange

class TitleScene(Scene):
    def get_screen_id(self):
        return "title"
    
    def get_event_handlers(self):
        return {"on_key_press": self.on_key_press}

    def setup(self):
        self.choices: list[TitleChoice] = [
            TitleChoiceSceneChange(self.app, "Start", TitleScene),
        ]
        background_image = pyglet.image.load(get_asset_file_path("img/croissant_boy.png"))
        self.bg = pyglet.sprite.Sprite(background_image, x=0, y=0, batch=self.surface)
        self.current_choice = 0
        self.surface = pyglet.graphics.Batch()
        self.labels = []
        for choice in self.choices:
            text_surface = pyglet.text.Label(
                choice.name,
                font_name='Unifont',
                font_size=50,
                x=SCREEN_WIDTH // 2 + 200,
                y=SCREEN_HEIGHT // 3 + len(self.labels) * 50,
                batch=self.surface,
                color=(0, 0, 0, 255),
            )
            self.labels.append(text_surface)
        self.cursor_label = pyglet.text.Label(
            ">",
            font_name='Unifont',
            font_size=50,
            x=SCREEN_WIDTH // 2 + 130,
            y=SCREEN_HEIGHT // 3 + self.current_choice * 50,
            batch=self.surface,
            color=(255, 0, 0, 255),
        )
        self.draw()
    
    def tick(self):
        pass

    def draw(self):
        self.bg.draw()
        self.surface.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.change_current_choice((self.current_choice + 1) % len(self.choices))
        elif symbol == pyglet.window.key.DOWN:
            self.change_current_choice((self.current_choice - 1) % len(self.choices))
        elif symbol == pyglet.window.key.ENTER:
            self.select()

    def change_current_choice(self, choice: int):
        self.current_choice = choice
        self.cursor_label.y = SCREEN_HEIGHT // 3 + self.current_choice * 50
        self.draw()

    def select(self):
        choice = self.choices[self.current_choice]
        choice.on_select()
        self.draw()