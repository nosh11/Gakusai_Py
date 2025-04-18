from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QVBoxLayout, QLabel
import yaml

from PyQt6.QtGui import QPainter

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common import game_map
from common.game_map import MapData

from mapeditor.chipset_image import get_chip_image


class MapTileCanvas(QWidget):
    def __init__(self, map_data: MapData):
        super().__init__()
        self.map_data = map_data
        self.setMinimumSize(400, 400)
        self.update()

    def update(self):
        # fill the background with white color
        self.setStyleSheet("background-color: white;")
        

        # 碁盤目の描画処理をここに書く
        painter = QPainter(self)
        for x in range(self.map_data.size_x):
            for y in range(self.map_data.size_y):
                tile = self.map_data.get_tile(x, y)

                image = get_chip_image(self.map_data.chipset, tile)  # チップの画像を取得
                if image is not None:
                    painter.drawImage(x, y, image)

                # 碁盤目の線を描画

        pass
class ChipSetCanvas(QWidget):
    def __init__(self, chipset: str):
        super().__init__()
        self.chipset = chipset
        self.setMinimumSize(400, 400)

    def paintEvent(self, event):
        # 描画処理をここに書く
        pass


class MapEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('マップエディタ')
        self.setGeometry(100, 100, 800, 600)

        self.current_map: MapData = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.load_button = QPushButton('マップを読み込む')
        self.load_button.clicked.connect(self.load_map)

        layout.addWidget(self.load_button)
        self.setLayout(layout)
        self.setWindowTitle('マップエディタ')
        self.resize(300, 100)

    def editor_ui(self):
        if not self.current_map:
            print("マップが読み込まれていません。")
            return

        self.setMinimumSize(800, 600)
        self.setWindowTitle(f'マップエディタ - {self.current_map.name}')
        self.resize(800, 600)        
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        
        layout = self.layout()  # 現在のレイアウトを取得

        info_label = QLabel(f"マップ名: {self.current_map.name}")
        layout.addWidget(info_label)

        size_label = QLabel(f"サイズ: {self.current_map.size_x} x {self.current_map.size_y}")
        layout.addWidget(size_label)

        canvas = MapTileCanvas(self.current_map)
        layout.addWidget(canvas)

        self.setLayout(layout)

    def load_map(self):
        # ファイルダイアログを開く
        file_name, _ = QFileDialog.getOpenFileName(self, 'マップファイルを選択', 'resource/map', 'YAML Files (*.yaml *.yml)')
        
        if file_name:  # ファイルが選ばれたら
            try:
                self.current_map = game_map.load_map_data(file_name.split('/')[-1].split('.')[0])
                print(self.current_map.__dict__)
            except FileNotFoundError:
                print('ファイルが見つかりません:', file_name)
            except yaml.YAMLError as e:
                print('YAML読み込みエラー:', e)
            except game_map.InvalidMapDataError as e:
                print('無効なマップデータ:', e)
            except Exception as e:
                print('読み込みエラー:', e)
            self.editor_ui()  # UIを更新

if __name__ == '__main__':
    app = QApplication([])
    editor = MapEditor()
    editor.show()
    app.exec()