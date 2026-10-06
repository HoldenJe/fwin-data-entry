"""Main application window."""

from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
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
        """Placeholder new project action."""

        QMessageBox.information(
            self,
            "New Project",
            "New Project not implemented yet.",
        )

    def open_project(self):
        """Placeholder open project action."""

        QMessageBox.information(
            self,
            "Open Project",
            "Open Project not implemented yet.",
        )