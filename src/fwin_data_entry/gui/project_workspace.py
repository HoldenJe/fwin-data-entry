"""Project workspace."""

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)


class ProjectWorkspace(QWidget):
    """Project workspace."""

    def __init__(self):
        super().__init__()

        self.project_label = QLabel(
            "No project loaded"
        )

        banner_font = QFont()
        banner_font.setPointSize(16)
        banner_font.setBold(True)
        
        self.project_label.setFont(
            banner_font
        )

        self.sam_list = QListWidget()
        self.add_sam_button = QPushButton(
            "Add SAM"
        )
        self.add_sam_button.setAutoDefault(True)
                
        self.sample_heading = QLabel(
            "FN121"
        )

        self.catch_heading = QLabel(
            "FN123"
        )

        self.fish_heading = QLabel(
            "FN125"
        )
        heading_font = QFont()
        heading_font.setBold(True)
        self.sample_heading.setFont(
            heading_font
        )

        self.catch_heading.setFont(
            heading_font
        )

        self.fish_heading.setFont(
            heading_font
        )

        self.sample_details = QLabel(
            "No sample selected"
        )
        self.edit_sample_button = QPushButton(
            "Edit Sample"
        )
        self.edit_sample_button.setAutoDefault(True)
        
        self.delete_sample_button = QPushButton(
            "Delete Sample"
        )
        self.delete_sample_button.setAutoDefault(True)
        self.catch_table = QTableWidget()

        self.catch_table.setColumnCount(3)

        self.catch_table.setHorizontalHeaderLabels(
            [
                "SPC",
                "CATCNT",
                "BIOCNT",
            ]
        )
        self.edit_catch_button = QPushButton(
            "Edit Catch Summary"
        )
        self.edit_catch_button.setAutoDefault(True)

        self.delete_catch_button = QPushButton(
            "Delete Catch Summary"
        )
        self.delete_catch_button.setAutoDefault(True)
        
        self.fish_table = QTableWidget()

        self.fish_table.setColumnCount(5)

        self.fish_table.setHorizontalHeaderLabels(
            [
                "FISH",
                "SPC",
                "FLEN",
                "TLEN",
                "RWT",
            ]
        )
        self.edit_fish_button = QPushButton(
            "Edit Fish"
        )
        self.edit_fish_button.setAutoDefault(True)

        self.delete_fish_button = QPushButton(
            "Delete Fish"
        )
        self.delete_fish_button.setAutoDefault(True)

        self.add_catch_button = QPushButton(
            "Add Catch Summary"
        )
        self.add_catch_button.setAutoDefault(True)

        self.add_fish_button = QPushButton(
            "Add Fish Sample"
        )
        self.add_fish_button.setAutoDefault(True)
        self.add_age_button = QPushButton(
            "Add Age Data"
        )

        self.add_age_button.setEnabled(
            False
        )
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Samples"))
        left_layout.addWidget(self.sam_list)
        left_layout.addWidget(self.add_sam_button)

        right_layout = QVBoxLayout()
        
        sample_section = QHBoxLayout()

        sample_info = QVBoxLayout()
        sample_info.addWidget(self.sample_details)

        sample_buttons = QVBoxLayout()
        sample_buttons.addWidget(self.edit_sample_button)
        sample_buttons.addWidget(self.delete_sample_button)
        sample_buttons.addStretch()

        sample_section.addLayout(sample_info, 4)
        sample_section.addLayout(sample_buttons, 1)

        right_layout.addLayout(sample_section)

        catch_section = QHBoxLayout()
        
        catch_buttons = QVBoxLayout()
        catch_buttons.addWidget(self.add_catch_button)
        catch_buttons.addWidget(self.edit_catch_button)
        catch_buttons.addWidget(self.delete_catch_button)
        catch_buttons.addStretch()

        catch_section.addWidget(self.catch_table, 4)
        catch_section.addLayout(catch_buttons, 1)

        right_layout.addLayout(catch_section)
        
        right_layout.addWidget(
            self.fish_heading
        )

        fish_section = QHBoxLayout()

        fish_buttons = QVBoxLayout()
        fish_buttons.addWidget(self.add_fish_button)
        fish_buttons.addWidget(self.add_age_button)
        fish_buttons.addWidget(self.edit_fish_button)
        fish_buttons.addWidget(self.delete_fish_button)
        fish_buttons.addStretch()

        fish_section.addWidget(self.fish_table, 4)
        fish_section.addLayout(fish_buttons, 1)

        right_layout.addLayout(fish_section)
        
        layout = QHBoxLayout()

        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 3)

        self.setLayout(layout)
        
        self.edit_sample_button.setEnabled(False)
        self.delete_sample_button.setEnabled(False)
        self.edit_catch_button.setEnabled(False)
        self.delete_catch_button.setEnabled(False)

        self.edit_fish_button.setEnabled(False)
        self.delete_fish_button.setEnabled(False)

    def set_sample_details(
        self,
        text: str,
    ):
        """Display sample details."""

        self.sample_details.setText(text)