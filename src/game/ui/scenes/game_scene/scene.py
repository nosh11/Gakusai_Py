import pygame
from common.models.game_map import load_map_data
from common.utils.file_manager import get_asset_file_path
from game.commons.view import Scene
from game.ui.scenes.game_scene.components.map_field import MapField
from game.ui.scenes.game_scene.components.message_box import MessageBox
from game.ui.scenes.game_scene.components.game_player import GamePlayer

SKIP_CD = 10

class GameScene(Scene):
    def define_text_labels(self):
        pass

    def setup(self):
        self.message_box = MessageBox(self.display_surface)
        self.space_pressed = False
        self.skip_pressed = False
        self.skip = False
        self.skip_cd = SKIP_CD
        self.map_data = load_map_data("map1")
        self.map_field = MapField(self.display_surface, self.map_data)
        self.player = GamePlayer(self.display_surface, self.map_field)
        self.player.set_position(self.map_data.init_pos)
        self.map_field.reset_map_surface()
        self.background_image: pygame.Surface = None
        if self.map_data.background_image_path:
            path = get_asset_file_path(f"backgrounds\\{self.map_data.background_image_path}")
            self.background_image = pygame.image.load(path)
        

    def display(self):
        if self.background_image is not None:
            self.display_surface.blit(self.background_image, (0, 0))
        self.message_box.update()
        self.message_box.draw()
        self.map_field.draw()
        self.player.draw()

    def tick(self):
        self.player.move()

        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.space_key_pressed()
            elif pygame.key.get_pressed()[pygame.K_a]:
                self.message_box.is_hidden = not self.message_box.is_hidden
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self._app_controller.set_transition_type("slide>slide")
                self._app_controller.set_transition_seconds((0.01, 0.01))
                self._app_controller.set_next_view("pause")
            elif pygame.key.get_pressed()[pygame.K_z]:
                self.z_key_pressed()
        else:
            self.space_pressed = False
            self.skip_pressed = False
        if self.skip:
            self.skip_cd -= 1
        if self.skip_cd <= 0:
            self.next_message()

    def space_key_pressed(self):
        if self.space_pressed:
            return
        self.space_pressed = True
        self.next_message()

    def next_message(self):
        if not self.message_box.is_text_complete():
            self.message_box.show_text_complete()
            return
        self.show_next_message()

    def z_key_pressed(self):
        if self.skip_pressed:
            return
        self.skip_pressed = True
        self.skip = not self.skip

    def show_next_message(self):
        self.skip_cd = SKIP_CD
        self.message_box.next()

    def on_load(self):
        pygame.mixer.music.stop()