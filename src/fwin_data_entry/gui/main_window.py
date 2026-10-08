"""Main application window."""

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
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
from fwin_data_entry.gui.project_workspace import (
    ProjectWorkspace,
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
    get_fish_sample,
    update_fish_sample,
)
from fwin_data_entry.services.project_service import (
    create_project,
    get_first_project,
)
from fwin_data_entry.services.workspace_service import (
    get_project_samples,
    get_sample_catch_summaries,
    get_sample_details,
    get_sample_fish,
)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FWIN Data Entry")

        self.workspace = ProjectWorkspace()

        self.setCentralWidget(
            self.workspace
        )

        self.current_project = None
        self.current_database = None
        self.current_sam = None
        self.selected_fish = None
        self.workspace.add_catch_button.clicked.connect(
            self.new_catch_summary
        )

        self.workspace.add_fish_button.clicked.connect(
            self.new_fish_sample
        )
        self.workspace.add_sam_button.clicked.connect(
            self.new_effort
        )
        self._create_menu()

        self.workspace.catch_table.itemSelectionChanged.connect(
           self.catch_selection_changed
        )

        self.workspace.fish_table.itemSelectionChanged.connect(
            self.fish_selection_changed
        )

        self.workspace.edit_fish_button.clicked.connect(
           self.edit_fish
        )
        
        
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

        self.workspace.project_label.setText(
 
                f"{project.prj_cd}\n"
                f"{project.prj_nm}\n"
                f"{project.wby_nm}"
 
        )


        self.workspace.sam_list.clear()

        for sam in get_project_samples(
            filename
        ):
            self.workspace.sam_list.addItem(
                f"SAM {sam}"
            )
        self.workspace.sam_list.itemClicked.connect(
            self.select_sample
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

        self.current_sam = effort.sam
        
        self.refresh_workspace()

        QMessageBox.information(
            self,
            "Success",
            f"Saved SAM {effort.sam}",
        )

    def new_catch_summary(self):
        """Create FN123 records."""

        if self.current_project is None:
            QMessageBox.warning(
                self,
                "No Project",
                "Open a project first.",
            )
            return

        dialog = CatchSummaryDialog(
            sam=self.current_sam,
        )

        while True:

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

            self.refresh_workspace()

            if dialog.result_action == "close":

                QMessageBox.information(
                    self,
                    "Success",
                    (
                        f"Saved catch summary "
                        f"for SPC {record.spc}"
                    ),
                )

                return

            dialog.clear_species_fields()
    
    def new_fish_sample(self):
        """Create FN125 records."""

        if self.current_project is None:
            QMessageBox.warning(
                self,
                "No Project",
                "Open a project first.",
            )
            return

        dialog = FishSampleDialog(
            sam=self.current_sam,
        )

        while True:

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

            self.refresh_workspace()

            if dialog.result_action == "close":

                QMessageBox.information(
                    self,
                    "Success",
                    (
                        f"Saved fish {record.fish} "
                        f"for SPC {record.spc}"
                    ),
                )

                return

            next_fish = get_next_fish(
                self.current_database,
                self.current_project.prj_cd,
                record.sam,
                record.eff,
                record.spc,
            )

            dialog.fish.setText(
                str(next_fish)
            )

            dialog.clear_fish_fields()
            
    def refresh_workspace(self):
        """Refresh workspace display."""

        if self.current_database is None:
            return

        # Refresh SAM list
        self.workspace.sam_list.clear()

        for sam in get_project_samples(
            self.current_database
        ):
            self.workspace.sam_list.addItem(
                f"SAM {sam}"
            )

        # Refresh selected SAM
        if self.current_sam is None:
            return

        for index in range(
            self.workspace.sam_list.count()
        ):

            item = self.workspace.sam_list.item(
                index
            )

            sam = int(
                item.text().replace(
                    "SAM ",
                    "",
                )
            )

            if sam == self.current_sam:

                self.workspace.sam_list.setCurrentItem(
                    item
                )

                self.select_sample(item)

                break


    def select_sample(self, item):
        """Display sample information."""

        sam = int(
            item.text().replace(
                "SAM ",
                "",
            )
        )

        self.current_sam = sam

        effort = get_sample_details(
            self.current_database,
            self.current_project.prj_cd,
            sam,
        )

        if effort is None:
            return

        self.workspace.set_sample_details(
            
                f"Sample: {effort.sam}\n\n"
                f"GR: {effort.gr}\n"
                f"Area: {effort.area}\n"
                f"Set Date: {effort.effdt0}\n"
                f"Set Time: {effort.efftm0}\n"
                f"Secchi: {effort.secchi}\n"
                f"Crew: {effort.crew}"
            
        )

        summaries = get_sample_catch_summaries(
            self.current_database,
            sam,
        )

        self.workspace.catch_table.setRowCount(
            len(summaries)
        )

        for row, (
            spc,
            catcnt,
            biocnt,
        ) in enumerate(summaries):

            self.workspace.catch_table.setItem(
                row,
                0,
                QTableWidgetItem(str(spc)),
            )

            self.workspace.catch_table.setItem(
                row,
                1,
                QTableWidgetItem(str(catcnt)),
            )

            self.workspace.catch_table.setItem(
                row,
                2,
                QTableWidgetItem(str(biocnt)),
            )

        fish_records = get_sample_fish(
            self.current_database,
            sam,
        )

        self.workspace.fish_table.setRowCount(
            len(fish_records)
        )

        for row, (
            fish,
            spc,
            flen,
            tlen,
            rwt,
        ) in enumerate(fish_records):

            self.workspace.fish_table.setItem(
                row,
                0,
                QTableWidgetItem(str(fish)),
            )

            self.workspace.fish_table.setItem(
                row,
                1,
                QTableWidgetItem(str(spc)),
            )

            self.workspace.fish_table.setItem(
                row,
                2,
                QTableWidgetItem(str(flen)),
            )

            self.workspace.fish_table.setItem(
                row,
                3,
                QTableWidgetItem(str(tlen)),
            )

            self.workspace.fish_table.setItem(
                row,
                4,
                QTableWidgetItem(str(rwt)),
            )    
    
    def catch_selection_changed(self):
        """Enable FN123 actions."""

        enabled = (
            self.workspace.catch_table.currentRow()
            >= 0
        )

        self.workspace.edit_catch_button.setEnabled(
            enabled
        )

        self.workspace.delete_catch_button.setEnabled(
            enabled
        )


    def fish_selection_changed(self):
        """Enable FN125 actions."""

        row = (
            self.workspace.fish_table.currentRow()
        )

        enabled = row >= 0

        self.workspace.edit_fish_button.setEnabled(
            enabled
        )

        self.workspace.delete_fish_button.setEnabled(
            enabled
        )

        if enabled:

            fish = int(
                self.workspace.fish_table.item(
                    row,
                    0,
                ).text()
            )

            spc = int(
                self.workspace.fish_table.item(
                    row,
                    1,
                ).text()
            )

            self.selected_fish = (
                fish,
                spc,
            )
        else:

            self.selected_fish = None

    def edit_fish(self):
        """Edit selected fish."""

        if self.selected_fish is None:
            return

        fish_number, spc = self.selected_fish

        fish_sample = get_fish_sample(
            self.current_database,
            self.current_project.prj_cd,
            self.current_sam,
            999,
            spc,
            fish_number,
        )

        if fish_sample is None:
            return

        dialog = FishSampleDialog()

        dialog.load_fish(
            fish_sample
        )

        if not dialog.exec():
            return

        data = dialog.get_data()

        updated_fish = FishSample(
            prj_cd=fish_sample.prj_cd,
            sam=fish_sample.sam,
            eff=fish_sample.eff,
            spc=fish_sample.spc,
            fish=fish_sample.fish,
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

        update_fish_sample(
            self.current_database,
            updated_fish,
        )

        self.refresh_workspace()