import pygame
from game.app_state import AppStats as stats
from common.utils.file_manager import get_static_file_path
from commons.view import Scene
from commons.widget import UIWidget
from game.consts import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FPS
from game.interfaces.observe import Observable, Observer
from game.ui.scenes.game_scene.components.message_box import MessageBox
from model.languages import get_lang_texts
from game.ui.scenes.game_scene.components.game_player import GamePlayer

SKIP_CD = 10

class GameScene(Scene):
    def define_text_labels(self):
        font = self.get_language().get_font(50)
        pause_menu_label = font.render("test", True, (255, 255, 255))
        self.set_text_label("pause_menu", pause_menu_label)

    def setup(self):
        self.message_box = MessageBox(self.display_surface)
        self.space_pressed = False
        self.skip_pressed = False
        self.skip = False
        self.skip_cd = SKIP_CD
        self.player = GamePlayer(self.display_surface)

        self.background_image = pygame.image.load(get_static_file_path("img/haikei.png"))

    def display(self):
        self.display_surface.blit(self.background_image, (0, 0))
        self.message_box.update()
        self.message_box.draw()
        self.player.draw()

        self.display_surface.blit(
            self.get_text_label("pause_menu"),
            (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        )

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
        bgm = "bgm/bgm_1.wav"
        if stats.flags.get("bgm") != bgm:
            pygame.mixer.music.load(get_static_file_path(bgm))
            stats.flags["bgm"] = bgm
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.unpause()