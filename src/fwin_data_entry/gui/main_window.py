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
    get_catch_summary,
    update_catch_summary,
)
from fwin_data_entry.services.effort_service import (
    create_effort,
    get_next_sam,
    get_effort,
    update_effort,
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
    catch_summary_exists,
    sample_exists,
    catch_summary_record_exists,
    effort_exists,
)

from fwin_data_entry.services.validation import (
    validate_required,
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
        self.selected_catch = None
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
        self.workspace.edit_catch_button.clicked.connect(
            self.edit_catch_summary
        )
        self.workspace.edit_sample_button.clicked.connect(
            self.edit_sample
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

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)


    def new_project(self):
        """Create a new project."""

        dialog = ProjectDialog()

        while True:

            if not dialog.exec():
                return

            data = dialog.get_data()
            
            project = Project(
                prj_cd=data["prj_cd"],
                prj_nm=data["prj_nm"],
                wby_nm=data["wby_nm"],
                prj_date0=data["prj_date0"],
                prj_date1=data["prj_date1"],
                comment=data["comment"],
            )
            try:

                validate_required(
                    project.prj_cd,
                    "PRJ_CD",
                )

                validate_required(
                    project.prj_nm,
                    "PRJ_NM",
                )

                validate_required(
                    project.wby_nm,
                    "WBY_NM",
                )

            except ValueError as e:

                QMessageBox.warning(
                    self,
                    "Validation Error",
                    str(e),
                )

                continue

            if not data["db_location"]:

                QMessageBox.warning(
                    self,
                    "Missing Location",
                    "Select a database location.",
                )

                continue

            db_path = (
                Path(data["db_location"])
                / f"{data['prj_cd']}.sqlite"
            )

            if db_path.exists():

                QMessageBox.warning(
                    self,
                    "Project Exists",
                    (
                        f"{db_path.name} already "
                        "exists.\n\n"
                        "Choose a different "
                        "project code or location."
                    ),
                )

                continue
            
            initialize_database(str(db_path))

            try:

                create_project(
                    str(db_path),
                    project,
                )

            except ValueError as e:

                QMessageBox.warning(
                    self,
                    "Validation Error",
                    str(e),
                )

                continue

            self.current_project = project
            self.current_database = str(db_path)
            self.clear_workspace()

            self.workspace.project_label.setText(
                (
                    f"PROJECT: {project.prj_cd}    "
                    f"{project.prj_nm}    "
                    f"{project.wby_nm}"
                )
            )

            self.current_sam = None

            self.workspace.sam_list.clear()

            for sam in get_project_samples(
                self.current_database
            ):
                self.workspace.sam_list.addItem(
                    f"SAM {sam}"
                )
            
            break


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

        initialize_database(
            filename
        )
        
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
        self.clear_workspace()

        self.workspace.project_label.setText(
 
                f"PROJECT: {project.prj_cd}    "
                f"{project.prj_nm}    "
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
        """Create FN121 records."""

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

        while True:

            if not dialog.exec():
                return

            data = dialog.get_data()
            if effort_exists(
                self.current_database,
                int(data["sam"]),
            ):

                QMessageBox.warning(
                    self,
                    "Sample Exists",
                    (
                        f"SAM {data['sam']} already "
                        "exists.\n\n"
                        "Use Edit Sample to modify "
                        "the existing record."
                    ),
                )

                continue

            effort = Effort(
                prj_cd=self.current_project.prj_cd,
                sam=int(data["sam"]),
                gr=data["gr"],
                area=data["area"],
                effdt0=data["effdt0"],
                efftm0=data["efftm0"],

                sitem0=float(data["sitem0"])
                if data["sitem0"]
                else None,

                dd_lat0=float(data["dd_lat0"])
                if data["dd_lat0"]
                else None,

                dd_lon0=float(data["dd_lon0"])
                if data["dd_lon0"]
                else None,

                secchi=float(data["secchi"])
                if data["secchi"]
                else None,

                grdepmin=float(data["grdepmin"])
                if data["grdepmin"]
                else None,

                grdepmax=float(data["grdepmax"])
                if data["grdepmax"]
                else None,

                effdt1=data["effdt1"],
                efftm1=data["efftm1"],

                effst=int(data["effst"])
                if data["effst"]
                else None,

                crew=data["crew"],
                comment=data["comment"],
            )

            try:

                create_effort(
                    self.current_database,
                    effort,
                )

            except ValueError as e:

                QMessageBox.warning(
                    self,
                    "Validation Error",
                    str(e),
                )

                continue

            self.current_sam = effort.sam

            self.refresh_workspace()

            if dialog.result_action == "close":

                QMessageBox.information(
                    self,
                    "Success",
                    f"Saved SAM {effort.sam}",
                )

                return

            next_sam = get_next_sam(
                self.current_database,
                self.current_project.prj_cd,
            )

            dialog.sam.setText(
                str(next_sam)
            )

            dialog.clear_sam_fields()

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
            
            if catch_summary_record_exists(
                self.current_database,
                int(data["sam"]),
                str(data["spc"]),
            ):

                QMessageBox.warning(
                    self,
                    "Catch Summary Exists",
                    (
                        "A catch summary already "
                        "exists for this species.\n\n"
                        "Use Edit Catch Summary "
                        "to modify the record."
                    ),
                )

                continue
            
            if not sample_exists(
                self.current_database,
                int(data["sam"]),
            ):

                QMessageBox.warning(
                    self,
                    "Missing Sample",
                    (
                        "Create an FN121 sample "
                        "before entering catch "
                        "summaries."
                    ),
                )

                continue
            
            if not data["spc"]:

                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "SPC is required.",
                )

                continue

            if not data["catcnt"]:

                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "CATCNT is required.",
                )

                continue

            if not data["biocnt"]:

                QMessageBox.warning(
                    self,
                    "Validation Error",
                    "BIOCNT is required.",
                )

                continue

            record = CatchSummary(
                prj_cd=self.current_project.prj_cd,
                sam=int(data["sam"]),
                eff=int(data["eff"]),
                spc=data["spc"].zfill(3),
                catcnt=int(data["catcnt"]),
                biocnt=int(data["biocnt"]),
            )

            try:

                create_catch_summary(
                    self.current_database,
                    record,
                )

            except ValueError as e:

                QMessageBox.warning(
                    self,
                    "Validation Error",
                    str(e),
                )

                continue


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
            if not catch_summary_exists(
                self.current_database,
                int(data["sam"]),
                str(data["spc"]),
            ):

                QMessageBox.warning(
                    self,
                    "Missing Catch Summary",
                    (
                        "Create an FN123 catch summary "
                        "for this species before "
                        "adding fish records."
                    ),
                )

                continue

            next_fish = get_next_fish(
                self.current_database,
                self.current_project.prj_cd,
                int(data["sam"]),
                999,
                str(data["spc"]),
            )

            record = FishSample(
                prj_cd=self.current_project.prj_cd,
                sam=int(data["sam"]),
                eff=999,
                spc=data["spc"].zfill(3),
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
                comment=data["comment"],
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
        self.workspace.edit_sample_button.setEnabled(True)
        effort = get_sample_details(
            self.current_database,
            self.current_project.prj_cd,
            sam,
        )

        if effort is None:
            return

        self.workspace.set_sample_details(
        
            f"SAM: {effort.sam}    "
            f"GR: {effort.gr}    "
            f"Area: {effort.area}\n\n"
            f"Date: {effort.effdt0}    "
            f"Time: {effort.efftm0}\n\n"
            f"Secchi: "
            f"{'' if effort.secchi is None else effort.secchi}    "
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

        row = (
            self.workspace.catch_table.currentRow()
        )

        enabled = row >= 0

        self.workspace.edit_catch_button.setEnabled(
            enabled
        )

        self.workspace.delete_catch_button.setEnabled(
            enabled
        )

        if enabled:

            spc = self.workspace.catch_table.item(
                    row,
                    0,
                ).text()

            self.selected_catch = spc

        else:

            self.selected_catch = None


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

            spc = self.workspace.fish_table.item(
                    row,
                    1,
                ).text()
            

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

        dialog = FishSampleDialog(
            edit_mode=True
        )

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
            comment=data["comment"],
        )

        update_fish_sample(
            self.current_database,
            updated_fish,
        )

        self.refresh_workspace()

    def edit_catch_summary(self):
        """Edit selected catch summary."""

        if self.selected_catch is None:
            return

        catch_summary = get_catch_summary(
            self.current_database,
            self.current_project.prj_cd,
            self.current_sam,
            999,
            self.selected_catch,
        )

        if catch_summary is None:
            return

        dialog = CatchSummaryDialog(edit_mode=True)

        dialog.load_catch_summary(
            catch_summary
        )

        if not dialog.exec():
            return

        data = dialog.get_data()

        updated_summary = CatchSummary(
            prj_cd=catch_summary.prj_cd,
            sam=catch_summary.sam,
            eff=catch_summary.eff,
            spc=catch_summary.spc,
            catcnt=int(data["catcnt"]),
            biocnt=int(data["biocnt"]),
        )

        update_catch_summary(
            self.current_database,
            updated_summary,
        )

        self.refresh_workspace()

    def edit_sample(self):
        """Edit selected FN121 record."""

        effort = get_effort(
            self.current_database,
            self.current_project.prj_cd,
            self.current_sam,
        )

        if effort is None:
            return

        dialog = EffortDialog(edit_mode=True)

        dialog.load_effort(
            effort
        )

        while True:

            if not dialog.exec():
                return

            data = dialog.get_data()

            updated_effort = Effort(
                prj_cd=effort.prj_cd,
                sam=effort.sam,
                eff=effort.eff,
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
                sitem0=float(data["sitem0"])
                if data["sitem0"]
                else None,
                secchi=float(data["secchi"])
                if data["secchi"]
                else None,
                grdepmin=float(data["grdepmin"])
                if data["grdepmin"]
                else None,
                grdepmax=float(data["grdepmax"])
                if data["grdepmax"]
                else None,
                effdt1=data["effdt1"],
                efftm1=data["efftm1"],
                effst=int(data["effst"])
                if data["effst"]
                else None,
                crew=data["crew"],
                comment=data["comment"],
            )

            try:

                update_effort(
                    self.current_database,
                    updated_effort,
                )

            except ValueError as e:

                QMessageBox.warning(
                    self,
                    "Validation Error",
                    str(e),
                )

                continue

            break

        self.refresh_workspace()

    def clear_workspace(self):
        """Clear sample-specific workspace data."""

        self.current_sam = None

        self.workspace.sample_details.setText(
            "No sample selected"
        )

        self.workspace.catch_table.setRowCount(0)

        self.workspace.fish_table.setRowCount(0)

        self.workspace.edit_sample_button.setEnabled(
            False
        )

        self.workspace.edit_catch_button.setEnabled(
            False
        )

        self.workspace.delete_catch_button.setEnabled(
            False
        )

        self.workspace.edit_fish_button.setEnabled(
            False
        )

        self.workspace.delete_fish_button.setEnabled(
            False
        )
        self.workspace.sam_list.clearSelection()

        self.selected_fish = None
        self.selected_catch = None