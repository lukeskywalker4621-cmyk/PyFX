import sys
import os

from PySide6.QtCore import Qt
from PySide6.QWidgets import (
    QApplication,
    QDockWidget,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from file_importer import import_files
from project_manager import load_files, save_files

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init___()

        self.setWindowTitle("PyFX - a python editing software")
        self.resize(1400, 850)

        # composition viewer
        viewer = QLabel("Composition Viewer")
        viewer.setAlignment(Qt.AlignCenter)
        viewer.setStyleSheet("""
            QLabel { 
                background-color: #202020; 
                color: #aaaaaa; 
                font-size: 24px;
            }
        """)
        self.setCentralWidget(viewer)

        # project panel
        project_panel = QDockWidget("Project", self)

        project_widget = QWidget()
        project_layout = QVBoxLayout(project_widget)

        import_button = QPushButton("Import Files")
        import_button.clicked.connect(self.open_import_dialog)

        self.project_list = QListWidget()

        project_layout.addWidget(import_button)
        project_layout.addWidget(self.project_list)

        project_panel.setWidget(project_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, project_panel)

        # other panels
        properties_panel = QDockWidget("Properties", self)
        properties_panel.setWidget(QLabel("Layer properties"))
        self.addDockWidget(Qt.RightDockWidgetArea, properties_panel)

        timeline_panel = QDockWidget("Timeline", self)
        timeline_panel.setWidget(QLabel("Timeline tracks and keyframes"))
        self.addDockWidget(Qt.BottomDockWidgetArea, timeline_panel)

        effects_panel = QDockWidget("Effects", self)
        effects_panel.setWidget(QLabel("Available effects"))
        self.addDockWidget(Qt.RightDockWidgetArea, effects_panel)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #303030;
            }

            QDockWidget {
                color: white;
                font-weight: bold;
            }

            QDockWidget::title {
                background-color: #3d3d3d;
                padding: 6px;
            }

            QLabel {
                background-color: #252525;
                color: #dddddd;
                padding: 8px;
            }

            QListWidget {
                background-color: #252525;
                color: #dddddd;
                border: none;
            }

            QPushButton {
                background-color: #444444;
                color: white;
                padding: 6px;
                border: 1px solid #555555;
            }

            QPushButton:hover {
                background-color: #555555;
            }
        """)

        self.load_saved_files()

    def open_import_dialog(self):
        files = import_files(self)

        if not files:
            return

        existing_files = self.get_saved_files()

        for file_path in files:
            if file_path not in existing_files:
                existing_files.append(file_path)
                self.add_file_to_project_list(file_path)

        save_files(existing_files)

    def load_saved_files(self):
        for file_path in load_files():
            # Only display files that still exist
            if os.path.exists(file_path):
                self.add_file_to_project_list(file_path)

    def add_file_to_project_list(self, file_path):
        file_name = os.path.basename(file_path)

        self.project_list.addItem(file_name)

        item = self.project_list.item(self.project_list.count() - 1)

        # Store the complete path invisibly
        item.setData(Qt.UserRole, file_path)

    def get_saved_files(self):
        files = []

        for index in range(self.project_list.count()):
            item = self.project_list.item(index)
            file_path = item.data(Qt.UserRole)
            files.append(file_path)

        return files


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
