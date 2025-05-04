

import random
import pygame
from common.util.file_manager import get_asset_file_path
from game.common.transition_controller import ViewTransitionSwitcher
from game.common.view_transition import FadeTransition
from game.interface.observe_interface import Observable, Observer
from game.common.scene import Scene
from common.widget import UIWidget
from game.consts import SCREEN_WIDTH, SCREEN_HEIGHT


class BGMFrame(UIWidget):
    def __init__(self, view_display_surface: pygame.Surface, x, y, name, font: pygame.font.Font, filename: str):
        super().__init__(view_display_surface, x, y)
        text_label = font.render(name, True, (255, 255, 255))
        self.showing_image = pygame.Surface((text_label.get_width() + 20, text_label.get_height() + 20))
        self.showing_image.fill((60, 60, 120))
        self.showing_image.blit(font.render(name, True, (255, 255, 255)), (10, 10))
        self.filename = filename

    def play(self):
        pygame.mixer.music.load(get_asset_file_path(f"bgm/{self.filename}"))
        pygame.mixer.music.play(-1)

    def update(self) -> bool:
        return False
    
    def draw_outline(self, color=(255, 0, 0)):
        pygame.draw.rect(self.showing_image, color, self.showing_image.get_rect(), 3)

BGMS = {
    "BARIKI DRINK": "bariki.mp3",
    "断界桟": "bgm_1.wav",
    "蛍光": "bgm_2.wav",
    "sky_bridge_music": "bgm_3.wav",
    "applu": "bgm.mp3",
    "えげつない音楽": "bgm_pa.wav",
    "えげつなさがえげつない音楽": "bgm_pa2.mp3",
    "な": "isaf.wav",
    "ado - ぽんぽこぽん": "ado.wav",
    "5rremi": "5rremi.mp3",
    "left hand": "lj9t_left.mp3",
    "right hand": "d.wav",
}


class SoundRoomScene(Scene):
    def __init__(self, app_controller, language, screen_id: str = "sound_room"):
        super().__init__(app_controller, language, screen_id)

    def setup(self):
        self.bgm_frames = [[]]
        bgm_frame = None
        width_sum = 0
        row = 0
        for name, filename in BGMS.items():
            x = width_sum + 75
            y = row * 75 + 125
            bgm_frame = BGMFrame(self.display_surface, x, y, name, 
                                pygame.font.Font(self.get_language().get_font(), 24), filename)
            width_sum += bgm_frame.showing_image.get_width() + 20
            if width_sum > SCREEN_WIDTH - 50:
                row += 1
                self.bgm_frames.append([])
                x = 75
                y = row * 75 + 125
                bgm_frame = BGMFrame(self.display_surface, x, y, name, pygame.font.Font(self.get_language().get_font(), 24), filename)
                width_sum = bgm_frame.showing_image.get_width() + 20
                
            self.bgm_frames[row].append(bgm_frame)
                

        self.selected_bgm = (0, 0)
        self.sound_room_text = pygame.font.Font(self.get_language().get_font(), 50).render("Sound Room", True, (0, 0, 0))


    def display(self):
        self.display_surface.fill((100, 100, 100))
        # 2重リストをフラットにする
        i = 0
        for row in range(len(self.bgm_frames)):
            for column in range(len(self.bgm_frames[row])):
                frame: BGMFrame = self.bgm_frames[row][column]
                frame.update()
                frame.draw()
                if (column, row) == self.selected_bgm:
                    frame.draw_outline()
                else:
                    frame.draw_outline(color=(224, 255, 224))
                i += 1

        texts = [
            f"Sound Room",
            f"Press ESC to return {random.randint(0, 100)}",
        ]

        self.display_surface.blit(self.sound_room_text, (100, 50))

        for text in texts:
            self.display_surface.blit(
                self.font_console.render(text, True, (0, 0, 0)),
                (0, texts.index(text) * 20)
            )
    

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from game.scenes.title.title import TitleScene
                t = [FadeTransition(0.5), FadeTransition(0.5)]
                t[0].set_view(self)
                t[1].set_view_from_class(TitleScene, self._app_controller, self.get_language(), "title")
                self._app_controller.set_transition(ViewTransitionSwitcher(t[0], t[1]))

            column, row = self.selected_bgm
            current_bgm_frame: BGMFrame =  self.bgm_frames[row][column]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.bgm_frames[row][column].play()
                    return
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    if event.key == pygame.K_LEFT:
                        column = (column - 1) % len(self.bgm_frames[row])
                    else:
                        column = (column + 1) % len(self.bgm_frames[row])
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    current_x = current_bgm_frame.pos[0]
                    direction = -1 if event.key == pygame.K_UP else 1
                    row = (row + direction) % len(self.bgm_frames)
                    column = 0
                    min_diff = abs(current_x - self.bgm_frames[row][column].pos[0])
                    for i in range(len(self.bgm_frames[row])):
                        diff = abs(current_x - self.bgm_frames[row][i].pos[0])
                        if diff < min_diff:
                            min_diff = diff
                            column = i
                    column = min(max(column, 0), len(self.bgm_frames[row]) - 1)
                self.selected_bgm = (column, row)    
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    for row in range(len(self.bgm_frames)):
                        for column in range(len(self.bgm_frames[row])):
                            frame: BGMFrame = self.bgm_frames[row][column]
                            if frame.showing_image.get_rect(topleft=(frame.pos[0], frame.pos[1])).collidepoint(mouse_x, mouse_y):
                                self.selected_bgm = (column, row)
                                frame.play()
                                return
    
    def load_text(self):
        self.text_dict = {
            "bgm": "BGM",
            "sfx": "SFX",
            "volume": "Volume"
        }

    def define_text_labels(self):
        font = pygame.font.Font(self.get_language().get_font(), 50)
        self.set_text_label("title", font.render(self.get_text("title"), True, (255, 255, 255)))
        self.font_console = pygame.font.Font(self.get_language().get_font(), 10)
        self.set_text_label("console", self.font_console.render(self.get_text("console"), True, (0, 0, 0)))


    def on_load(self):
        pygame.mixer.music.stop()
    