

import random
import pygame
from commons.file_manager import get_static_file_path
from commons.observe import Observable, Observer
from commons.view import View
from commons.widget import UIWidget
from settings import SCREEN_WIDTH


class BGMFrame(UIWidget):
    def __init__(self, view_display_surface: pygame.Surface, x, y, name, font: pygame.font.Font, filename: str):
        super().__init__(view_display_surface, x, y)
        text_label = font.render(name, True, (255, 255, 255))
        self.showing_image = pygame.Surface((text_label.get_width() + 20, text_label.get_height() + 20))
        self.showing_image.fill((60, 60, 120))
        self.showing_image.blit(font.render(name, True, (255, 255, 255)), (10, 10))
        self.filename = filename

    def play(self):
        pygame.mixer.music.load(get_static_file_path(f"bgm/{self.filename}"))
        pygame.mixer.music.play(-1)

    def update(self) -> bool:
        return False
    
    def draw_outline(self, color=(255, 0, 0)):
        pygame.draw.rect(self.showing_image, color, self.showing_image.get_rect(), 3)

BGMS = {
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


class SoundRoomView(View):
    def setup(self):
        self.bgm_frames = [[]]
        bgm_frame = None
        width_sum = 0
        row = 0
        for name, filename in BGMS.items():
            x = width_sum + 75
            y = row * 75 + 125
            bgm_frame = BGMFrame(self.display_surface, x, y, name, self.get_language().get_font(24), filename)
            width_sum += bgm_frame.showing_image.get_width() + 20
            if width_sum > SCREEN_WIDTH - 50:
                row += 1
                self.bgm_frames.append([])
                x = 75
                y = row * 75 + 125
                bgm_frame = BGMFrame(self.display_surface, x, y, name, self.get_language().get_font(24), filename)
                width_sum = bgm_frame.showing_image.get_width() + 20
                
            self.bgm_frames[row].append(bgm_frame)
                

        self.selected_bgm = (0, 0)
        self.sound_room_text = self.get_language().get_font(50).render("Sound Room", True, (0, 0, 0))


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
                self._app_controller.set_transition_type("slide>slide")
                self._app_controller.set_transition_seconds((0.2, 0.2))
                self._app_controller.set_next_view("title")

            column, row = self.selected_bgm
            current_bgm_frame: BGMFrame =  self.bgm_frames[row][column]

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                column = (column - 1) % len(self.bgm_frames[row])

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                column = (column + 1) % len(self.bgm_frames[row])

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                current_x = current_bgm_frame.pos[0]
                row = (row - 1) % len(self.bgm_frames)
                # column の取得方法:
                # self.bgm_frames[row]: list[BGMFrame] について、
                # abs(current_x - self.bgm_frames[row][column]) が最小となる column を求める。
                # ただし、column は 0 <= column < len(self.bgm_frames[row]) を満たす必要がある。
                # そのため、column の初期値は 0 とする。
                column = 0
                min_diff = abs(current_x - self.bgm_frames[row][column].pos[0])
                for i in range(len(self.bgm_frames[row])):
                    diff = abs(current_x - self.bgm_frames[row][i].pos[0])
                    if diff < min_diff:
                        min_diff = diff
                        column = i
                column = min(max(column, 0), len(self.bgm_frames[row])-1)


            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                current_x = current_bgm_frame.pos[0]
                row = (row + 1) % len(self.bgm_frames)
                column = 0
                min_diff = abs(current_x - self.bgm_frames[row][column].pos[0])
                for i in range(len(self.bgm_frames[row])):
                    diff = abs(current_x - self.bgm_frames[row][i].pos[0])
                    if diff < min_diff:
                        min_diff = diff
                        column = i
                column = min(max(column, 0), len(self.bgm_frames[row])-1)
            
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.bgm_frames[row][column].play()
                return
            
            self.selected_bgm = (column, row)
    
    def load_text(self):
        self.text_dict = {
            "bgm": "BGM",
            "sfx": "SFX",
            "volume": "Volume"
        }

    def define_text_labels(self):
        font = self.get_language().get_font(50)
        self.set_text_label("title", font.render(self.get_text("title"), True, (255, 255, 255)))
        self.font_console = self.get_language().get_font(10)
        self.set_text_label("console", self.font_console.render(self.get_text("console"), True, (0, 0, 0)))


    def on_load(self):
        pygame.mixer.music.stop()
    