from PyQt6.QtGui import (
    QPainter, 
    QColor, 
    QPaintEvent, 
    QPixmap,
)
from PyQt6.QtCore import (
    QRect, 
    Qt, 
    QPoint
)
from PyQt6.QtWidgets import (
    QScrollArea, 
)

from mapeditor.widgets.map_painter.chip_cache import SharedImageCache
from common.model.game_map import MapData
from common.consts.screen_settings import CHIP_SIZE
from mapeditor.widgets.map_painter.chipset_canvas import ChipSetCanvas

class MapTileCanvas(QScrollArea):
    def __init__(self, map_data: MapData, chipset_canvas: ChipSetCanvas):
        super().__init__()
        self.chipset_canvas = chipset_canvas
        self.map_data = map_data
        self.zoom = 2  # ズーム倍率
        self.is_pushing_left_button = False
        self.update_needed_tiles = set()
        self.background_cache = None  # 背景用キャッシュPixMapを追加
        self.setWidgetResizable(True)  # スクロールエリアのサイズを自動調整
        self.build_background_cache()  # 初回キャッシュ作成

    def reset_size(self):
        tile_size = CHIP_SIZE * self.zoom
        self.size = self.map_data.size
        size_x, size_y = self.size
        self.setFixedSize(size_x * tile_size, size_y * tile_size)  # 固定サイズを設定

    def build_background_cache(self):
        # キャンバスサイズを計算
        if self.size != self.map_data.size:
            self.reset_size()
        tile_size = CHIP_SIZE * self.zoom
        self.viewport_rect = self.viewport().rect()  # ビューポートの矩形を取得
        self.background_cache = QPixmap(self.viewport_rect.size())  # ビューポートのサイズに合わせてキャッシュを作成
        self.background_cache.fill(QColor(255, 255, 255))

        painter = QPainter(self.background_cache)
        start_x = max(0, self.viewport_rect.left() // tile_size)
        end_x = min(self.map_data.size[0], (self.viewport_rect.right() + tile_size - 1) // tile_size)
        start_y = max(0, self.viewport_rect.top() // tile_size)
        end_y = min(self.map_data.size[1], (self.viewport_rect.bottom() + tile_size - 1) // tile_size)
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.map_data.get_tile((x, y))
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
        
        # map_data.init_posを描画
        if self.map_data.init_pos:
            init_x, init_y = self.map_data.init_pos
            painter.setPen(QColor(0, 200, 200))
            painter.drawRect(init_x * tile_size, init_y * tile_size, tile_size, tile_size)

        painter.end()



    def paintEvent(self, _: QPaintEvent):
        if self.background_cache:
            painter = QPainter(self.viewport())
            # 背景をPixMapから描画
            painter.drawPixmap(0, 0, self.background_cache)

            # 選択中のタイル枠を描画
            tile_size = CHIP_SIZE * self.zoom
            x, y = self.chipset_canvas.selected_chip_id % 16, self.chipset_canvas.selected_chip_id // 16
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(x * tile_size, y * tile_size, tile_size, tile_size)
            painter.end()
        # 必要なタイルだけ再描画
        for x, y in self.update_needed_tiles:
            tile_size = CHIP_SIZE * self.zoom
            rect = QRect(x * tile_size, y * tile_size, tile_size, tile_size)
            self.viewport().update(rect)
        self.update_needed_tiles.clear()  # 更新が終わったらセットをクリア

    def mousePressEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            # Iボタンも押下中　-> map_data.init_posをセット
            if a0.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                pos = a0.pos()
                self.map_data.init_pos = [pos.x() // (CHIP_SIZE * self.zoom), pos.y() // (CHIP_SIZE * self.zoom)]
                print(f"マップの初期位置を設定しました: {self.map_data.init_pos}")
            else:
                self.is_pushing_left_button = True
                self.draw(a0.pos())
    
    def mouseReleaseEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self.is_pushing_left_button = False
        
    def mouseMoveEvent(self, a0):
        if self.is_pushing_left_button:
            self.draw(a0.pos())

    def draw(self, pos: QPoint):
        if not self.is_pushing_left_button:
            return
        x = pos.x() // (CHIP_SIZE * self.zoom)
        y = pos.y() // (CHIP_SIZE * self.zoom)
        selected_chip_id = self.chipset_canvas.selected_chip_id
        if self.map_data.is_within_wall((x, y)) and selected_chip_id is not None:
            self.map_data.set_tile((x, y), selected_chip_id)
            self.update_needed_tiles.add((x, y))
            self.build_background_cache()  # 背景キャッシュを更新
            self.update()  # 必要な時だけ再描画トリガー