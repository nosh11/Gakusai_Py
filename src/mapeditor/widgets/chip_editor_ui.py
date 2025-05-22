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
from core.model import game_map
from core.model.game_map import MapData, save_map_data
from core.model.mapdata.chip_set import ChipSet
from mapeditor.widgets.map_painter import ChipSetCanvas, MapTileCanvas, SharedImageCache
from mapeditor.widgets.map_painter.chipset_canvas import ChipSetCanvasObserver


class ChipEditorUi(QWidget, ChipSetCanvasObserver):
    def __init__(self, chipset_canvas: ChipSetCanvas):
        super().__init__()
        self.chipset_canvas = chipset_canvas
        self.setLayout(QHBoxLayout())
        self.init_ui()
        return None

    def init_ui(self):
        layout: QVBoxLayout = self.layout()

        self.selected_chip_info_label = QLabel("")
        layout.addWidget(self.selected_chip_info_label)

        passable_button = QPushButton("Passable")
        passable_button.clicked.connect(self.set_passable)

        layout.addWidget(passable_button)
    
    def update_from_chipset_canvas(self):
        self.update()

    def update(self):
        chip = self.chipset_canvas.current_chip
        if chip is not None:
            self.selected_chip_info_label.setText(f"""
                                                Selected Chip ID: {chip.id}, 
                                                passable: {chip.passable},
                                                durability: {chip.durability}
                                                """)
        else:
            self.selected_chip_info_label.setText("No chip selected.")
        self.selected_chip_info_label.repaint()

    def set_passable(self):
        selected_chip_id = self.chipset_canvas.selected_chip_id
        if selected_chip_id is not None:
            self.chipset_canvas.chipset.load_chip(selected_chip_id).passable = not self.chipset_canvas.chipset.load_chip(selected_chip_id).passable
            print(f"Set chip {selected_chip_id} as passable.")
            self.update()
        else:
            print("No chip selected.")