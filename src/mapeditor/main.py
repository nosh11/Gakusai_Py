from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMenu, QHBoxLayout, QWidget

from core.model import game_map
from mapeditor.chip_editor import ChipEditor
from mapeditor.map.map_list import MapListWidget
from mapeditor.map_editor import MapEditor
class Editor:
    pass

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1280, 720)
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        self.setWindowTitle('マップエディタ')
        self.editor: Editor | None = None
        self.central_widget = QWidget(self)
        self.layout = QHBoxLayout()  # Save the layout in an instance variable
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.editor_placeholder = QWidget()
        self.editor_placeholder.setStyleSheet("background-color: #AAAAAA; color: white;")
        self.layout.addWidget(MapListWidget(), 1)
        self.layout.addWidget(self.editor_placeholder, 9)  # Placeholder for the editor
        self.init_ui()
    
    def update_editor(self, editor: Editor) -> None:
        self.editor = editor
        # Remove and delete the old placeholder widget
        self.layout.removeWidget(self.editor_placeholder)
        self.editor_placeholder.deleteLater()
        # Add the new editor widget to the layout at the same position/ratio
        self.editor_placeholder = editor
        self.layout.addWidget(self.editor_placeholder, 9)
    
    def init_ui(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('ファイル')
        self.create_load_editor_func(file_menu, MapEditor, 'マップ')
        self.create_load_editor_func(file_menu, ChipEditor, 'チップセット')
        self.show()
    
    def create_load_editor_func(self, menu: QMenu, editor_class: type[Editor], name: str) -> None:
        load_action = menu.addAction(f'{name}を読み込む')
        def load_func():
            file_name, _ = QFileDialog.getOpenFileName(self, f'{name}ファイルを選択', '', 'YAML Files (*.yaml *.yml)')
            if file_name:
                editor = editor_class(game_map.load_map_data(file_name.split('/')[-1].split('.')[0]))
                self.update_editor(editor)
        load_action.triggered.connect(load_func)





if __name__ == '__main__':
    app = QApplication([])
    editor = Main()
    editor.show()
    app.exec()