from math import ceil, floor
import cv2
import pygame
from common.consts.screen_settings import CHIP_SIZE
from common.models.game_map import ChipSet, MapData
from game.consts.screen_settings import SCREEN_HEIGHT, SCREEN_SIZE, SCREEN_WIDTH, ZOOM, ZOOMED_CHIP
from game.model.languages import Language
from game.ui.scenes.utils.image_manager import convert_opencv_img_to_pygame

def get_chip_image(chipset_image, chip_id: int):
    x = (chip_id % (chipset_image.shape[1] // CHIP_SIZE)) * CHIP_SIZE
    y = (chip_id // (chipset_image.shape[1] // CHIP_SIZE)) * CHIP_SIZE
    chip_image = chipset_image[y:y + CHIP_SIZE, x:x + CHIP_SIZE]
    chip_image = cv2.resize(chip_image, (CHIP_SIZE * ZOOM, CHIP_SIZE * ZOOM), interpolation=cv2.INTER_NEAREST)
    return convert_opencv_img_to_pygame(chip_image)

class MapField:
    def __init__(self, view_surface, map_data: MapData):
        self.view_surface = view_surface # 描画するSurface
        self.surface = pygame.Surface((SCREEN_WIDTH + ZOOMED_CHIP * 2, SCREEN_HEIGHT + ZOOMED_CHIP*2))
        self.map_data = map_data
        self.chipset_image = cv2.imread(self.map_data.chipset.chipset_image_path, cv2.IMREAD_UNCHANGED)

        self.current_topleft = (0, 0) # スクリーン座標系の左上座標
        self.chip_image_cache = {} # 
        self.screen_size = (self.map_data.size[0] * ZOOMED_CHIP, self.map_data.size[1] * ZOOMED_CHIP)
    
    def update_topleft(self, topleft: tuple[int, int]):
        if (self.current_topleft != topleft):
            self.move_surface(topleft)
            self.current_topleft = topleft

    def draw(self):
        self.view_surface.blit(self.surface, (-((self.current_topleft[0]+1)% ZOOMED_CHIP), -((self.current_topleft[1]+1)% ZOOMED_CHIP)))
    
    def reset_map_data(self, map_data: MapData):
        self.map_data = map_data
        self.screen_size = (self.map_data.size[0] * ZOOMED_CHIP, self.map_data.size[1] * ZOOMED_CHIP)
        self.surface = pygame.Surface((SCREEN_WIDTH + ZOOMED_CHIP * 2, SCREEN_HEIGHT + ZOOMED_CHIP))
        self.chip_image_cache.clear()
        self.reset_map_surface()

    def move_surface(self, topleft: tuple[int, int]):
        # Calculate the displacement in terms of tiles
        displacement = [topleft[i] // ZOOMED_CHIP - self.current_topleft[i] // ZOOMED_CHIP for i in range(2)]
        tile_topleft = [topleft[i] / ZOOMED_CHIP for i in range(2)]
        self.surface.blit(self.surface, (-displacement[0] * ZOOMED_CHIP, -displacement[1] * ZOOMED_CHIP))

        # Determine the visible tile range
        visible_tiles = [SCREEN_SIZE[i] // ZOOMED_CHIP for i in range(2)]

        # Redraw tiles for horizontal displacement
        if displacement[0] != 0:
            if displacement[0] > 0:
                # When moving right, draw the new right-side tiles.
                x_start = floor(tile_topleft[0]) + visible_tiles[0]
                x_end = ceil(tile_topleft[0]) + visible_tiles[0] + 1
            else:
                # When moving left, draw the new left-side tiles.
                x_start = floor(tile_topleft[0]) - 1
                x_end = ceil(tile_topleft[0])
            # extend the vertical range by one tile on both ends to prevent gaps
            for y in range(floor(tile_topleft[1]) - 1, ceil(tile_topleft[1]) + visible_tiles[1] + 1):
                for x in range(x_start, x_end):
                    self.draw_at(topleft, (x, y))
        # Redraw tiles for vertical displacement
        if displacement[1] != 0:
            y_start = floor(tile_topleft[1] - 1) if displacement[1] > 0 else ceil(tile_topleft[1]) - visible_tiles[1]
            y_end = ceil(tile_topleft[1] + 1) if displacement[1] > 0 else floor(tile_topleft[1])
            # extend the horizontal range by one tile on both ends to prevent gaps
            for y in range(y_start, y_end):
                for x in range(floor(tile_topleft[0]) - 1, ceil(tile_topleft[0]) + visible_tiles[0] + 1):
                    self.draw_at(topleft, (x, y))
    
    def draw_at(self, topleft: tuple[int, int], pos: tuple[int, int]):
        chip_id: int = self.map_data.get_tile(pos)
        if chip_id is None:
            return
        if chip_id not in self.chip_image_cache:
            chip_image = get_chip_image(self.chipset_image, chip_id)
            self.chip_image_cache[chip_id] = chip_image
        else:
            chip_image = self.chip_image_cache[chip_id]
        self.surface.blit(chip_image, ((pos[0]-(topleft[0] // ZOOMED_CHIP))*ZOOMED_CHIP, (pos[1]-(topleft[1] // ZOOMED_CHIP))*ZOOMED_CHIP))

    # 全体を改めて描画する場合、Surfaceを作り直す
    def reset_map_surface(self):
        chipset_image = cv2.imread(self.map_data.chipset.chipset_image_path, cv2.IMREAD_UNCHANGED)
        tl = [self.current_topleft[i] / ZOOMED_CHIP for i in range(2)]
        mass = [SCREEN_SIZE[i] // ZOOMED_CHIP for i in range(2)]
        draw_range = (
            floor(tl[0]), 
            floor(tl[1]),
            ceil(tl[0]) + mass[0],
            ceil(tl[1]) + mass[1]
        )

        for y in range(draw_range[1] - 1, draw_range[3] + 1):
            for x in range(draw_range[0] - 1, draw_range[2] + 1):
                self.draw_at(self.current_topleft, (x, y))