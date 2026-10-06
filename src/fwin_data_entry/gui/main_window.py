"""Main application window."""

from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
)

from fwin_data_entry.gui.project_dialog import (
    ProjectDialog,
)

class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FWIN Data Entry")

        label = QLabel("FWIN Data Entry")
        label.setMargin(20)

        self.setCentralWidget(label)

        self._create_menu()

    def _create_menu(self):
        """Create application menus."""

        file_menu = self.menuBar().addMenu("&File")

        new_project_action = file_menu.addAction("New Project")
        new_project_action.triggered.connect(
            self.new_project
        )

        open_project_action = file_menu.addAction(
            "Open Project"
        )
        open_project_action.triggered.connect(
            self.open_project
        )

        file_menu.addSeparator()

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

    def new_project(self):
        """Open project creation dialog."""

        dialog = ProjectDialog()

        if dialog.exec():
            project_data = dialog.get_data()

            print(project_data)
        else:
            print("Project cancelled")

    def open_project(self):
        """Placeholder open project action."""

        QMessageBox.information(
            self,
            "Open Project",
            "Open Project not implemented yet.",
        )