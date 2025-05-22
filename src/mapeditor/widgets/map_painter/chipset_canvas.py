import PyQt6, yaml, os, sys
from PyQt6.QtWidgets import (
    QWidget, 
)
from PyQt6.QtGui import (
    QPainter, 
    QColor, 
    QMouseEvent,
    QPixmap,
    QPaintEvent,
    QGuiApplication
)
from PyQt6.QtCore import (
    QRect, 
    Qt, 
)
import PyQt6.QtGui

from core.const import CHIP_SIZE
from core.model.game_map import ChipSet
from core.model.mapdata.chip import Chip
from mapeditor.widgets.map_painter.chip_cache import SharedImageCache

class ChipSetCanvasObserver:
    def update_from_chipset_canvas(self, *args, **kwargs):
        pass

class ChipSetCanvas(QWidget):
    def __init__(self, chipset: ChipSet):
        """
        Initialize the ChipSetCanvas.

        Args:
            chipset (ChipSet): The chipset object containing tile data to be displayed on the canvas.
        """
        super().__init__()
        self.chipset = chipset
        self.zoom = 2
        self.selected_chip_id = 0
        self.background_cache = None  # 背景用キャッシュPixMapを追加
        self.setStyleSheet("background-color: white;")

        self.build_background_cache()  # 初回キャッシュ作成

        self.observer: list[ChipSetCanvasObserver] = []
    
    def add_observer(self, o: ChipSetCanvasObserver):
        self.observer.append(o)

    @property
    def current_chip(self) -> Chip | None:
        if self.selected_chip_id is not None:
            return self.chipset.load_chip(self.selected_chip_id)
        return None

    def notify_observer(self):
        for o in self.observer:
            o.update_from_chipset_canvas()

    def build_background_cache(self):
        # キャンバスサイズを計算
        tile_size = CHIP_SIZE * self.zoom
        width = tile_size * 30
        height = tile_size * 16
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)  # 最大サイズを設定

        self.background_cache = QPixmap(width, height)
        self.background_cache.fill(QColor(255, 255, 255))  # 背景色を白に

        painter = QPainter(self.background_cache)

        for x in range(30):
            for y in range(16):
                tile_id = x + y * 30
                image = SharedImageCache.get_image(self.chipset, tile_id)
                if image:
                    scaled_image = image.scaled(tile_size, tile_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    painter.drawImage(QRect(x * tile_size, y * tile_size, tile_size, tile_size), scaled_image)
                else:
                    print(f"Tile ID {tile_id} not found in cache.")
        painter.end()

    def set_selected_chip_id(self, new_id: int):
        if new_id != self.selected_chip_id:
            self.selected_chip_id = new_id
            self.update()  # 必要な時だけ再描画トリガー

    def paintEvent(self, _: QPaintEvent):
        if self.background_cache:
            painter = QPainter(self)
            # 背景をPixMapから描画
            painter.drawPixmap(0, 0, self.background_cache)

            # 選択中のタイル枠を描画
            tile_size = CHIP_SIZE * self.zoom
            x, y = self.selected_chip_id % 30, self.selected_chip_id // 30
            painter.setPen(QColor(255, 0, 0))
            painter.drawRect(QRect(x * tile_size, y * tile_size, tile_size, tile_size))
            painter.end()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            x = pos.x() // (CHIP_SIZE * self.zoom)
            y = pos.y() // (CHIP_SIZE * self.zoom)
            self.set_selected_chip_id(x + y * 30)
            self.notify_observer()
