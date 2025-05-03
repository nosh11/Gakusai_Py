import os
import PyQt6
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, 
    QScrollArea,
    QPushButton,
)
from PyQt6.QtCore import ( 
    Qt, 
)
from common.model.game_map import MapData, load_map_data
from common.model.map.chip_set import ChipSet, save_chipset
from common.util.file_manager import get_resource_file_path
from mapeditor.widgets.chip_editor_ui import ChipEditorUi



def load_map_list() -> list[str]:
    map_list = []
    map_dir = get_resource_file_path('map')
    for file_name in os.listdir(map_dir):
        if file_name.endswith('.yaml') or file_name.endswith('.yml'):
            map_list.append(file_name.split('.')[0])
    return map_list

class MapListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.map_list = load_map_list()
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        self.setWindowTitle('マップリスト')
        self.init_ui()

    def init_ui(self):
        layout: QVBoxLayout = self.layout()
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('マップリスト')    
        
        for map_name in self.map_list:
            button = QPushButton(map_name)
            button.setStyleSheet("background-color: #2E2E2E; color: white;")
            layout.addWidget(button)
            button.clicked.connect(lambda _, name=lambda name: print(name): name)  # ボタンがクリックされたときにマップ名を表示する

        scrollable = QScrollArea()
        scrollable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # 水平スクロールバーを常に表示
        scrollable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # 垂直スクロールバーを常に表示
        scrollable.setWidgetResizable(True)  # スクロールエリアをリサイズ可能にする
        scrollable.setMaximumSize(500, 700)  # 最小サイズを設定

        layout.addWidget(scrollable)