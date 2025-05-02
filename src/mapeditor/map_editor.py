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
from common.model.game_map import MapData, save_map_data
from common.util.file_manager import get_resource_file_path
from mapeditor.widgets.map_painter import ChipSetCanvas, MapTileCanvas, SharedImageCache

class MapEditor(QWidget):
    def __init__(self, map_data):
        super().__init__()
        self.current_map: MapData = map_data
        self.setLayout(QVBoxLayout())
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('マップエディタ')    
        # layout is not set in the constructor, so we need to create it here
        # ルートレイアウトを作成し、QVBoxLayoutを設定
        layout: QVBoxLayout = self.layout()  # 現在のレイアウトを取得
        if layout is None:
            layout = QVBoxLayout()
            self.setLayout(layout)
        else:
            for i in reversed(range(self.layout().count())):
                widget = self.layout().itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

        info_labels_layout = QVBoxLayout()
        painting_layout = QHBoxLayout()

        layout.addLayout(info_labels_layout)
        layout.addLayout(painting_layout)

        info_labels_layout.addWidget(QLabel(f"マップ名: {self.current_map.name} ({self.current_map.map_id})"))
        info_labels_layout.addWidget(QLabel(f"チップセット: {self.current_map.chipset.chipset_id}"))
        info_labels_layout.addWidget(QLabel(f"サイズ: {self.current_map.size_x} x {self.current_map.size_y}"))

        self.chipset = ChipSetCanvas(self.current_map.chipset)
        canvas = MapTileCanvas(self.current_map, self.chipset)

        scrollable = QScrollArea()
        scrollable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # 水平スクロールバーを常に表示
        scrollable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # 垂直スクロールバーを常に表示
        scrollable.setWidget(canvas)
        scrollable.setWidgetResizable(True)  # スクロールエリアをリサイズ可能にする

        scrollable_2 = QScrollArea()
        scrollable_2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # 水平スクロールバーを常に表示
        scrollable_2.setWidget(self.chipset)
        scrollable_2.setWidgetResizable(True)

        # Add the scroll areas to the painting layout with stretch factors for a 7:3 ratio.
        # scrollable (canvas) gets a stretch of 7 (70%) and scrollable_2 (chipset) gets a stretch of 3 (30%).
        painting_layout.addWidget(scrollable_2, 3)
        painting_layout.addWidget(scrollable, 7)

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
        
        background_button = QPushButton('背景画像設定')
        # 背景画像用のダイアログを開く
        def set_background_image():
            file_name, _ = QFileDialog.getOpenFileName(self, '背景画像選択', '', 'Images (*.png *.jpg *.bmp)')
            if file_name:
                self.current_map.background_image_path = file_name
                print(f"背景画像を設定しました: {file_name}")
            else:
                print("背景画像の選択がキャンセルされました。")
        background_button.clicked.connect(set_background_image)
        info_labels_layout.addWidget(background_button)

        resize_button.clicked.connect(resize_map)
        info_labels_layout.addWidget(resize_button)

        self.setLayout(layout)
        self.show()

    def save_map(self):
        # 保存処理をここに実装
        if self.current_map:
            # YAMLファイルに保存する処理を実装
            file_name = get_resource_file_path(f'map\\{self.current_map.name}.yaml')
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