"""Main application window."""

from pathlib import Path

from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
)

from fwin_data_entry.database.initialize import (
    initialize_database,
)
from fwin_data_entry.gui.project_dialog import (
    ProjectDialog,
)
from fwin_data_entry.models.project import Project
from fwin_data_entry.services.project_service import (
    create_project,
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
        """Create a new project."""

        dialog = ProjectDialog()

        if not dialog.exec():
            return

        data = dialog.get_data()

        db_path = (
            Path("data/projects")
            / f"{data['prj_cd']}.sqlite"
        )

        initialize_database(str(db_path))

        project = Project(
            prj_cd=data["prj_cd"],
            prj_nm=data["prj_nm"],
            wby_nm=data["wby_nm"],
            prj_date0=data["prj_date0"],
            prj_date1=data["prj_date1"],
            comment=data["comment"],
        )

        create_project(
            str(db_path),
            project,
        )

        QMessageBox.information(
            self,
            "Success",
            f"Project created:\n{db_path}",
        )

    def open_project(self):
        """Placeholder open project action."""

        QMessageBox.information(
            self,
            "Open Project",
            "Open Project not implemented yet.",
        )