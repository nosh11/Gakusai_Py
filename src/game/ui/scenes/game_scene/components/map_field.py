


import cv2
import numpy as np
import pygame
from common.consts.screen_settings import CHIP_SIZE
from common.models.game_map import ChipSet, MapData
from game.consts.screen_settings import SCREEN_HEIGHT, SCREEN_WIDTH, ZOOM
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
        topleft_pos[0] // (chip_size * ZOOM),
        topleft_pos[1] // (chip_size * ZOOM),
        (topleft_pos[0] + screen_width + chip_size * ZOOM - 1) // (chip_size * ZOOM),
        (topleft_pos[1] + screen_height + chip_size * ZOOM - 1) // (chip_size * ZOOM),
    )

class MapField:
    def __init__(self, view_surface, map_data: MapData):
        self.view_surface = view_surface
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.topleft_pos: list[float, float] = [0.0, 0.0]
        self.map_data = map_data
        self.chip_image_cache = {}
        self.cached_map_surface = None
        self.needs_update = True

    def draw(self):
        if self.needs_update:
            self.update_map_surface()
        self.view_surface.blit(self.cached_map_surface, (0, 0))

    def update_map_surface(self):
        """
        マップの描画を更新するメソッド
        """
        # 描画範囲を取得
        draw_range = get_draw_range(
            (int(self.topleft_pos[0]), int(self.topleft_pos[1])), CHIP_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
        # マップのサイズを取得
        map_width = self.map_data.size_x * CHIP_SIZE * ZOOM
        map_height = self.map_data.size_y * CHIP_SIZE * ZOOM

        # マップ全体を描画するSurfaceを作成
        self.cached_map_surface = pygame.Surface((map_width, map_height))

        # チップを描画
        for y in range(draw_range[1], draw_range[3]):
            for x in range(draw_range[0], draw_range[2]):
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

        # スクリーンに合わせてマップ全体を描画するSurfaceを作成
        # self.cached_map_surface = pygame.transform.scale(self.cached_map_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.needs_update = False