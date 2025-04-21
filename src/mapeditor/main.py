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
)
from PyQt6.QtCore import ( 
    Qt, 
)
from common import game_map
from common.game_map import MapData, save_map_data
from mapeditor.widgets.map_painter import ChipSetCanvas, MapTileCanvas, SharedImageCache

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
        alayout = QHBoxLayout()
        canvas = MapTileCanvas(self.current_map)
        alayout.addWidget(canvas)
        self.chipset = ChipSetCanvas(self.current_map.chipset)
        alayout.addWidget(self.chipset)
        layout.addLayout(alayout)

        resize_button = QPushButton('サイズ変更')
        # 利サイズ用のダイアログを開く
        def resize_map():
            new_x, ok_x = QInputDialog.getInt(self, 'サイズ変更', '新しいXサイズ:', self.current_map.size_x, 1, 1000)
            new_y, ok_y = QInputDialog.getInt(self, 'サイズ変更', '新しいYサイズ:', self.current_map.size_y, 1, 1000)
            if ok_x and ok_y:
                self.current_map.resize(new_x, new_y)
                canvas.update()
                print(f"マップのサイズを変更しました: {new_x} x {new_y}")
            else:
                print("サイズ変更がキャンセルされました。")
        resize_button.clicked.connect(resize_map)
        layout.addWidget(resize_button)

        self.setLayout(layout)

    def load_map(self):
        # ファイルダイアログを開く
        file_name, _ = QFileDialog.getOpenFileName(self, 'マップファイルを選択', 'resource/map', 'YAML Files (*.yaml *.yml)')
        
        if file_name:  # ファイルが選ばれたら
            try:
                self.current_map = game_map.load_map_data(file_name.split('/')[-1].split('.')[0])
            except FileNotFoundError:
                print('ファイルが見つかりません:', file_name)
            except yaml.YAMLError as e:
                print('YAML読み込みエラー:', e)
            except game_map.InvalidMapDataError as e:
                print('無効なマップデータ:', e)
            except Exception as e:
                print('読み込みエラー:', e)
            self.editor_ui()  # UIを更新

    
    def save_map(self):
        # 保存処理をここに実装
        if self.current_map:
            # YAMLファイルに保存する処理を実装
            file_name = self.current_map.path
            if file_name:
                save_map_data(self.current_map)
                print(f'マップが保存されました: {file_name}')
        else:
            print('保存するマップがありません。')

    # ctrl+Sで保存
    def keyPressEvent(self, event: PyQt6.QtGui.QKeyEvent):
        if event.key() == PyQt6.QtCore.Qt.Key.Key_S and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            print("Ctrl+S pressed")
            self.save_map()
        if event.key() == PyQt6.QtCore.Qt.Key.Key_P and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.chipset.hide()
        elif event.key() == PyQt6.QtCore.Qt.Key.Key_C and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.chipset.show()
        elif event.key() == PyQt6.QtCore.Qt.Key.Key_E and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # チップセットのキャッシュを更新
            SharedImageCache.clear_cache()
            self.chipset.update()
        else:
            super().keyPressEvent(event)  # 他のキーイベントは親クラスに処理を委譲

if __name__ == '__main__':
    app = QApplication([])
    editor = MapEditor()
    editor.show()
    app.exec()