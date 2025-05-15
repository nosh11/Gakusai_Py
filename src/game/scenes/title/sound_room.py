import pygame
from common.util.file_manager import get_asset_file_path
from game.app.scene import Scene
from game.app.widget import UIWidget
from game.consts.screen_settings import SCREEN_WIDTH
from game.interface.observe import Observer


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


class SoundRoomScene(Scene, Observer):
    def get_screen_id(self):
        return "sound_room"

    def setup(self):
        self.selected_bgm = (0, 0)
        self.bgm_frames: list[list[BGMFrame]] = [[]]
        width_sum = 0
        row = 0
        font_24 = pygame.font.Font(self.app.get_language().get_font(), 24)
        self.sound_room_text = pygame.font.Font(self.app.get_language().get_font(), 50).render("Sound Room", True, (0, 0, 0))
        for name, filename in BGMS.items():
            x = width_sum + 75
            y = row * 75 + 125
            bgm_frame = BGMFrame(self.root_surface, x, y, name, font_24, filename)
            width_sum += bgm_frame.showing_image.get_width() + 20
            if width_sum > SCREEN_WIDTH - 50:
                row += 1
                self.bgm_frames.append([])
                x = 75
                y = row * 75 + 125
                bgm_frame = BGMFrame(self.root_surface, x, y, name, font_24, filename)
                width_sum = bgm_frame.showing_image.get_width() + 20
            self.bgm_frames[row].append(bgm_frame)
        self.draw()


    def draw(self):
        self.root_surface.fill((100, 100, 100))
        for row_idx, row in enumerate(self.bgm_frames):
            for col_idx, frame in enumerate(row):
                frame.update()
                frame.draw()
                color = (255, 0, 0) if (col_idx, row_idx) == self.selected_bgm else (224, 255, 224)
                frame.draw_outline(color=color)

        self.root_surface.blit(self.sound_room_text, (100, 50))

    def __move_cursor_horizontally(self, direction: int):
        col, row = self.selected_bgm
        new_col = col + direction
        if 0 <= new_col < len(self.bgm_frames[row]):
            self.__set_selected_bgm((new_col, row))
        else:
            new_row = (row - 1 if direction < 0 else row + 1) % len(self.bgm_frames)
            new_col = len(self.bgm_frames[new_row]) - 1 if direction < 0 else 0
            self.__set_selected_bgm((new_col, new_row))

    def __move_cursor_vertically(self, direction: int):
        col, row = self.selected_bgm
        current_x = self.bgm_frames[row][col].pos[0]
        new_row = (row + direction) % len(self.bgm_frames)
        new_col = min(
            range(len(self.bgm_frames[new_row])),
            key=lambda i: abs(current_x - self.bgm_frames[new_row][i].pos[0])
        )
        self.__set_selected_bgm((new_col, new_row))

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.app.back_scene()
                    return
                elif event.key == pygame.K_RETURN:
                    col, row = self.selected_bgm
                    self.bgm_frames[row][col].play()
                    return
                elif event.key == pygame.K_LEFT:
                    self.__move_cursor_horizontally(-1)
                elif event.key == pygame.K_RIGHT:
                    self.__move_cursor_horizontally(1)
                elif event.key == pygame.K_UP:
                    self.__move_cursor_vertically(-1)
                elif event.key == pygame.K_DOWN:
                    self.__move_cursor_vertically(1)
                else:
                    continue
                self.draw()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for row_idx, row in enumerate(self.bgm_frames):
                    for col_idx, frame in enumerate(row):
                        rect = frame.showing_image.get_rect(topleft=frame.pos)
                        if rect.collidepoint(mouse_x, mouse_y):
                            self.selected_bgm = (col_idx, row_idx)
                            frame.play()
                            return
    
    def __set_selected_bgm(self, bgm: tuple[int, int]):
        self.selected_bgm = bgm
        self.draw()

    def on_load(self):
        pygame.mixer.music.stop()

    def on_unload(self):
        pygame.mixer.music.stop()