"""Main application window."""

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
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
    get_first_project,
)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FWIN Data Entry")

        self.project_label = QLabel("No project loaded")

        self.project_label.setMargin(20)

        self.setCentralWidget(
            self.project_label
        )

        self.current_project = None
        self.current_database = None

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
        """Open an existing project."""

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "data/projects",
            "SQLite Database (*.sqlite)",
        )

        if not filename:
            return

        project = get_first_project(
            filename,
        )

        if project is None:
            QMessageBox.warning(
                self,
                "Error",
                "No project found.",
            )
            return

        self.current_project = project
        self.current_database = filename

        self.project_label.setText(
            (
                f"Project: {project.prj_cd}\n"
                f"Name: {project.prj_nm}\n"
                f"Waterbody: {project.wby_nm}"
            )
    )