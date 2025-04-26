from math import floor
import cv2
import pygame
from common.consts.screen_settings import CHIP_SIZE
from common.models.game_map import ChipSet, MapData
from game.consts.screen_settings import SCREEN_HEIGHT, SCREEN_WIDTH, ZOOM, ZOOMED_CHIP
from game.model.languages import Language
from game.ui.scenes.utils.image_manager import convert_opencv_img_to_pygame

def get_chip_image(chipset: ChipSet, chip_id: int):
    """
    チップセットから指定されたチップの画像を取得する関数
    :param chipset: チップセットのIDまたはパス
    :param chip_id: チップのID
    :param zoom: チップの拡大倍率
    :return: チップの画像のSurface
    """
    chipset_image = cv2.imread(chipset.chipset_image_path, cv2.IMREAD_UNCHANGED)
    x = (chip_id % (chipset_image.shape[1] // CHIP_SIZE)) * CHIP_SIZE
    y = (chip_id // (chipset_image.shape[1] // CHIP_SIZE)) * CHIP_SIZE
    chip_image = chipset_image[y:y + CHIP_SIZE, x:x + CHIP_SIZE]
    chip_image = cv2.resize(chip_image, (CHIP_SIZE * ZOOM, CHIP_SIZE * ZOOM), interpolation=cv2.INTER_NEAREST)
    return convert_opencv_img_to_pygame(chip_image)

def get_draw_range(topleft_pos, chip_size, screen_width, screen_height):
    """
    描画範囲に応じて、使用するチップデータ行列データの範囲を取得する関数
    :param topleft_pos: 左上の座標
    :param chip_size: チップのサイズ
    :param screen_width: スクリーンの幅
    :param screen_height: スクリーンの高さ
    :param zoom: チップの拡大倍率
    :return: 描画範囲
    """
    return (
        topleft_pos[0] // ZOOMED_CHIP, # 左上のX座標
        topleft_pos[1] // ZOOMED_CHIP, # 左上のY座標
        (topleft_pos[0] + screen_width + ZOOMED_CHIP - 1) // ZOOMED_CHIP, # 右下のX座標
        (topleft_pos[1] + screen_height + ZOOMED_CHIP - 1) // ZOOMED_CHIP, # 右下のY座標
    )

class MapField:
    def __init__(self, view_surface, map_data: MapData):
        self.view_surface = view_surface
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.map_data = map_data
        self.current_topleft = [0.0, 0.0]
        self.chip_image_cache = {}
        self.cached_map_surface = None
        self.needs_update = True

        self.screen_size = (self.map_data.size_x * ZOOMED_CHIP, self.map_data.size_y * ZOOMED_CHIP)
    
    def update_topleft(self, topleft):
        if (self.current_topleft != topleft):
            self.needs_update = True
            self.current_topleft = topleft

    def draw(self):
        if self.needs_update:
            self.update_map_surface()
        self.view_surface.blit(self.cached_map_surface, 
                                (-ZOOMED_CHIP - self.current_topleft[0] % ZOOMED_CHIP, 
                                -ZOOMED_CHIP - self.current_topleft[1] % ZOOMED_CHIP))

    def update_map_surface(self):
        """
        マップの描画を更新するメソッド
        """
        topleft = self.current_topleft
        draw_range = get_draw_range(
            (floor(topleft[0]), floor(topleft[1])), CHIP_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)        

        # マップ全体を描画するSurfaceを作成
        self.cached_map_surface = pygame.Surface(self.screen_size)

        # チップを描画
        for y in range(draw_range[1] - 1, draw_range[3] + 1):
            if 0 <= y < self.map_data.size_y:
                # チップの行を描画
                self.cached_map_surface.fill((0, 0, 0, 0), (0, (y - draw_range[1]) * CHIP_SIZE * ZOOM, 
                                                             self.screen_size[0], CHIP_SIZE * ZOOM))
            else:
                continue
            # チップの列を描画
            for x in range(draw_range[0] - 1, draw_range[2] + 1):
                if 0 <= x < self.map_data.size_x and 0 <= y < self.map_data.size_y:
                    chip_id = self.map_data.get_tile(x, y)
                    if chip_id not in self.chip_image_cache:
                        chip_image = get_chip_image(self.map_data.chipset, chip_id)
                        self.chip_image_cache[chip_id] = chip_image
                    else:
                        chip_image = self.chip_image_cache[chip_id]
                    # チップの位置を計算
                    pos_x = (x - draw_range[0]) * CHIP_SIZE * ZOOM
                    pos_y = (y - draw_range[1]) * CHIP_SIZE * ZOOM
                    
                    # チップを描画
                    self.cached_map_surface.blit(chip_image, (pos_x, pos_y))
        self.needs_update = False