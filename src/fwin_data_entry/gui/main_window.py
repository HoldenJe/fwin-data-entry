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
from fwin_data_entry.gui.catch_summary_dialog import (
    CatchSummaryDialog,
)
from fwin_data_entry.gui.effort_dialog import (
    EffortDialog,
)
from fwin_data_entry.gui.fish_sample_dialog import (
    FishSampleDialog,
)
from fwin_data_entry.gui.project_dialog import (
    ProjectDialog,
)
from fwin_data_entry.models.catch_summary import (
    CatchSummary,
)
from fwin_data_entry.models.effort import Effort
from fwin_data_entry.models.fish_sample import (
    FishSample,
)
from fwin_data_entry.models.project import Project
from fwin_data_entry.services.catch_summary_service import (
    create_catch_summary,
)
from fwin_data_entry.services.effort_service import (
    create_effort,
    get_next_sam,
)
from fwin_data_entry.services.fish_sample_service import (
    create_fish_sample,
    get_next_fish,
)
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

        new_effort_action = file_menu.addAction(
                "New Effort"
            )
        
        new_catch_action = file_menu.addAction(
            "New Catch Summary"
        )

        new_catch_action.triggered.connect(
            self.new_catch_summary
        )

        new_effort_action.triggered.connect(
                self.new_effort
            )

        new_fish_action = file_menu.addAction(
            "New Fish Sample"
        )

        new_fish_action.triggered.connect(
            self.new_fish_sample
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
                f"Project: {project.prj_cd}\n"
                f"Name: {project.prj_nm}\n"
                f"Waterbody: {project.wby_nm}"
            )

    def new_effort(self):
        """Open effort dialog."""

        if self.current_project is None:
            QMessageBox.warning(
                self,
                "No Project",
                "Open a project first.",
            )
            return

        next_sam = get_next_sam(
            self.current_database,
            self.current_project.prj_cd,
        )

        dialog = EffortDialog(
            sam=next_sam,
        )

        if not dialog.exec():
            return

        data = dialog.get_data()

        effort = Effort(
            prj_cd=self.current_project.prj_cd,
            sam=int(data["sam"]),
            gr=data["gr"],
            area=data["area"],
            effdt0=data["effdt0"],
            efftm0=data["efftm0"],
            dd_lat0=float(data["dd_lat0"])
            if data["dd_lat0"]
            else None,
            dd_lon0=float(data["dd_lon0"])
            if data["dd_lon0"]
            else None,
            secchi=float(data["secchi"])
            if data["secchi"]
            else None,
            crew=data["crew"],
            comment=data["comment"],
        )

        create_effort(
            self.current_database,
            effort,
        )

        QMessageBox.information(
            self,
            "Success",
            f"Saved SAM {effort.sam}",
        )

    def new_catch_summary(self):
        """Create FN123 record."""

        if self.current_project is None:
            QMessageBox.warning(
                self,
                "No Project",
                "Open a project first.",
            )
            return

        dialog = CatchSummaryDialog()

        if not dialog.exec():
            return

        data = dialog.get_data()

        record = CatchSummary(
            prj_cd=self.current_project.prj_cd,
            sam=int(data["sam"]),
            eff=int(data["eff"]),
            spc=int(data["spc"]),
            catcnt=int(data["catcnt"]),
            biocnt=int(data["biocnt"]),
        )

        create_catch_summary(
            self.current_database,
            record,
        )

        QMessageBox.information(
            self,
            "Success",
            (
                f"Saved catch summary "
                f"for SPC {record.spc}"
            ),
        )
    
    def new_fish_sample(self):
        """Create FN125 record."""

        if self.current_project is None:
            QMessageBox.warning(
                self,
                "No Project",
                "Open a project first.",
            )
            return

        dialog = FishSampleDialog()

        if not dialog.exec():
            return

        data = dialog.get_data()

        next_fish = get_next_fish(
            self.current_database,
            self.current_project.prj_cd,
            int(data["sam"]),
            999,
            int(data["spc"]),
        )

        record = FishSample(
            prj_cd=self.current_project.prj_cd,
            sam=int(data["sam"]),
            eff=999,
            spc=int(data["spc"]),
            fish=next_fish,
            flen=float(data["flen"])
            if data["flen"]
            else None,
            tlen=float(data["tlen"])
            if data["tlen"]
            else None,
            rwt=float(data["rwt"])
            if data["rwt"]
            else None,
            sex=int(data["sex"])
            if data["sex"]
            else None,
            mat=int(data["mat"])
            if data["mat"]
            else None,
            agest=data["agest"],
            stom=data["stom"],
            taxon=data["taxon"],
            gonwt=float(data["gonwt"])
            if data["gonwt"]
            else None,
            eviswt=float(data["eviswt"])
            if data["eviswt"]
            else None,
            tissue=data["tissue"],
        )

        create_fish_sample(
            self.current_database,
            record,
        )

        QMessageBox.information(
            self,
            "Success",
            (
                f"Saved fish {record.fish} "
                f"for SPC {record.spc}"
            ),
        )