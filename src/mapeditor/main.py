import PyQt6, yaml
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget,
    QFileDialog, 
    QPushButton, 
    QVBoxLayout, 
    QLabel, 
    QHBoxLayout, 
    QInputDialog,
    QMainWindow,
    QScrollArea,
)
from PyQt6.QtCore import ( 
    Qt, 
)
from common.model import game_map
from common.model.game_map import MapData, save_map_data
from common.model.map.chip_set import load_chipset
from mapeditor.chip_editor import ChipEditor
from mapeditor.map_editor import MapEditor
from mapeditor.widgets.map_painter import ChipSetCanvas, MapTileCanvas, SharedImageCache



class Editor:
    pass

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1280, 720)
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        self.setWindowTitle('マップエディタ')    

        self.editor: Editor = None
        self.init_ui()

    def init_ui(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('ファイル')
        load_map_action = file_menu.addAction('マップを読み込む')
        load_map_action.triggered.connect(self.create_map_editor)

        load_chipset_action = file_menu.addAction('チップセットを読み込む')
        load_chipset_action.triggered.connect(self.create_chip_editor)
        
        self.show()

    def create_map_editor(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'マップファイルを選択', 'resource/map', 'YAML Files (*.yaml *.yml)')
        if file_name:  # ファイルが選ばれたら
            map_data = game_map.load_map_data(file_name.split('/')[-1].split('.')[0])
            editor = MapEditor(map_data)
            self.set_editor(editor)
    
    def create_chip_editor(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'チップセットファイルを選択', 'resource/chipset', 'YAML Files (*.yaml *.yml)')
        if file_name:
            chipset = game_map.load_chipset(file_name.split('/')[-1].split('.')[0])
            editor = ChipEditor(chipset)
            self.set_editor(editor)
            
    def set_editor(self, editor: Editor):
        self.editor = editor
        self.setCentralWidget(editor)


if __name__ == '__main__':
    app = QApplication([])
    editor = Main()
    editor.show()
    app.exec()