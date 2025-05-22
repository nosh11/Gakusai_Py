import PyQt6
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, 
    QScrollArea,
)
from PyQt6.QtCore import ( 
    Qt, 
)
from core.model.mapdata.chip_set import ChipSet, save_chipset
from mapeditor.widgets.chip_editor_ui import ChipEditorUi
from mapeditor.widgets.map_painter import ChipSetCanvas

class ChipEditor(QWidget):
    def __init__(self, chipset: ChipSet):
        super().__init__()
        self.chipset = chipset
        self.setLayout(QVBoxLayout())
        self.init_ui()

    def init_ui(self):
        layout: QVBoxLayout = self.layout()  # type: ignore
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('チップエディタ')    
        
        chip_canvas = ChipSetCanvas(self.chipset)
        layout.addWidget(chip_canvas)

        scrollable = QScrollArea()
        scrollable.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # 水平スクロールバーを常に表示
        scrollable.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # 垂直スクロールバーを常に表示
        scrollable.setWidget(chip_canvas)
        scrollable.setWidgetResizable(True)  # スクロールエリアをリサイズ可能にする
        scrollable.setMaximumSize(500, 700)  # 最小サイズを設定

        layout.addWidget(scrollable)

        chip_editor_ui = ChipEditorUi(chip_canvas)
        chip_canvas.add_observer(chip_editor_ui)
        layout.addWidget(chip_editor_ui)

    def keyPressEvent(self, event: PyQt6.QtGui.QKeyEvent): # type: ignore
        from PyQt6 import QtCore
        if event.key() == QtCore.Qt.Key.Key_S and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            print("Ctrl+S pressed")
            save_chipset(self.chipset)