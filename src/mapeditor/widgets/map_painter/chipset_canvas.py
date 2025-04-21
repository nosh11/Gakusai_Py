import PyQt6, yaml, os, sys
from PyQt6.QtWidgets import (
    QWidget, 
)
from PyQt6.QtGui import (
    QPainter, 
    QColor, 
    QMouseEvent
)
from PyQt6.QtCore import (
    QRect, 
    Qt, 
)

from common.consts.screen_settings import CHIP_SIZE
from common.game_map import ChipSet
from mapeditor.widgets.map_painter import SharedImageCache
from mapeditor.widgets.map_painter import selected_chip_id

class ChipSetCanvas(QWidget):
    def __init__(self, chipset: ChipSet):
        super().__init__()
        self.chipset = chipset
        self.zoom = 2
        self.setMinimumSize(400, 800)

    def paintEvent(self, _):
        # fill the background with white color
        self.setStyleSheet("background-color: white;")

        # 碁盤目の描画処理をここに書く
        painter = QPainter(self)
        # タイルの描画
        tile_size = CHIP_SIZE * self.zoom  # ズーム倍率を考慮
        for x in range(16):  # 仮に16x16のチップセットとする
            for y in range(24):
                tile_id = x + y * 16
                image = SharedImageCache.get_image(self.chipset, tile_id)
                if image:
                    scaled_image = image.scaled(tile_size, tile_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    painter.drawImage(QRect(x * tile_size, y * tile_size, tile_size, tile_size), scaled_image)
                else:
                    print(f"Tile ID {tile_id} not found in cache.")
        
        x, y = selected_chip_id % CHIP_SIZE, selected_chip_id // CHIP_SIZE
        painter.setPen(QColor(255, 0, 0))
        painter.drawRect(QRect(x * tile_size, y * tile_size, tile_size, tile_size))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            x = pos.x() // (CHIP_SIZE * self.zoom)
            y = pos.y() // (CHIP_SIZE * self.zoom)
            global selected_chip_id
            selected_chip_id = x + y * 16
            print(f"Selected tile ID: {selected_chip_id}")
    
    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom = min(self.zoom + 1, 10)
            elif delta < 0:
                self.zoom = max(self.zoom - 1, 1)
            self.setMinimumSize(16 * CHIP_SIZE * self.zoom, 24 * CHIP_SIZE * self.zoom)
            self.update()  # ズーム変更時に再描画を要求