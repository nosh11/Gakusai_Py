from PyQt6.QtWidgets import (QWidget)
from PyQt6.QtGui import (
    QPainter, 
    QColor, 
    QPaintEvent, 
    QMouseEvent
)
from PyQt6.QtCore import (
    QRect, 
    Qt, 
)

from mapeditor.widgets.map_painter.chip_cache import SharedImageCache
from common.game_map import MapData
from common.consts.screen_settings import CHIP_SIZE

# グローバル変数
selected_chip_id = 0  # 選択されたタイルID

class MapTileCanvas(QWidget):
    def __init__(self, map_data: MapData):
        super().__init__()
        self.map_data = map_data
        self.zoom = 2  # ズーム倍率
        self.setMinimumSize(self.map_data.size_x * CHIP_SIZE * self.zoom, self.map_data.size_y * CHIP_SIZE * self.zoom)
        self.is_pushing_left_button = False
        self.setMouseTracking(True)  # マウスの動きを追跡するために必要
        self.viewport_rect = QRect(0, 0, self.width(), self.height())  # ビューポートの矩形
        self.update_needed_tiles = set()  # 差分描画用のタイルセット

        self.setStyleSheet("background-color: white;")  # 背景色を白に設定
        self.setAutoFillBackground(False)

    def paintEvent(self, _: QPaintEvent):
        self.setStyleSheet("background-color: white;") 
        painter = QPainter(self)
        tile_size = CHIP_SIZE * self.zoom

        # ビューポートの矩形を取得
        self.viewport_rect = self.rect()

        # 描画範囲を計算
        start_x = max(0, self.viewport_rect.left() // tile_size)
        end_x = min(self.map_data.size_x, (self.viewport_rect.right() + tile_size - 1) // tile_size)
        start_y = max(0, self.viewport_rect.top() // tile_size)
        end_y = min(self.map_data.size_y, (self.viewport_rect.bottom() + tile_size - 1) // tile_size)

        # 差分描画が必要な場合
        if self.update_needed_tiles:
            for x, y in self.update_needed_tiles:
                if start_x <= x < end_x and start_y <= y < end_y:
                    tile = self.map_data.get_tile(x, y)
                    image = SharedImageCache.get_image(self.map_data.chipset, tile)
                    if image:
                        scaled_image = image.scaled(tile_size, tile_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        painter.drawImage(QRect(x * tile_size, y * tile_size, tile_size, tile_size), scaled_image)
                    else:
                        print(f"Tile ID {tile} not found in cache.")
            self.update_needed_tiles.clear()  # 差分描画が終わったらリセット
        else:
            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    tile = self.map_data.get_tile(x, y)
                    image = SharedImageCache.get_image(self.map_data.chipset, tile)
                    if image:
                        scaled_image = image.scaled(tile_size, tile_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        painter.drawImage(QRect(x * tile_size, y * tile_size, tile_size, tile_size), scaled_image)
                    else:
                        print(f"Tile ID {tile} not found in cache.")

        painter.setPen(QColor(0, 0, 0))  # 黒色でペンを設定

        # グリッドの描画
        for x in range(start_x, end_x + 1):
            painter.drawLine(x * tile_size, start_y * tile_size, x * tile_size, end_y * tile_size)
        for y in range(start_y, end_y + 1):
            painter.drawLine(start_x * tile_size, y * tile_size, end_x * tile_size, y * tile_size)

        painter.end()

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom = min(self.zoom + 1, 10)
            elif delta < 0:
                self.zoom = max(self.zoom - 1, 1)
            self.setMinimumSize(self.map_data.size_x * CHIP_SIZE * self.zoom, self.map_data.size_y * CHIP_SIZE * self.zoom)
            self.update()  # ズーム変更時に再描画を要求

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            x = pos.x() // (CHIP_SIZE * self.zoom)
            y = pos.y() // (CHIP_SIZE * self.zoom)

            if 0 <= x < self.map_data.size_x and 0 <= y < self.map_data.size_y:
                self.map_data.chips_map[y][x] = selected_chip_id  # 選択されたタイルIDをマップに設定
                self.update_needed_tiles.add((x, y))  # 差分描画用にタイルを追加
                self.update()  # 再描画を要求