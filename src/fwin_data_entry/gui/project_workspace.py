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
        self.delete_sample_button = QPushButton(
            "Delete Sample"
        )
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

        self.delete_catch_button = QPushButton(
            "Delete Catch Summary"
        )
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

        self.delete_fish_button = QPushButton(
            "Delete Fish"
        )
        self.add_catch_button = QPushButton(
            "Add Catch Summary"
        )

        self.add_fish_button = QPushButton(
            "Add Fish Sample"
        )
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Samples"))
        left_layout.addWidget(self.sam_list)
        left_layout.addWidget(self.add_sam_button)

        right_layout = QVBoxLayout()
        
        right_layout.addWidget(
            self.project_label
        )

        right_layout.addWidget(
            self.sample_heading
        )

        right_layout.addWidget(
            self.sample_details
        )
        right_layout.addWidget(
            self.edit_sample_button
        )
        right_layout.addWidget(
            self.delete_sample_button
        )
        right_layout.addWidget(
            self.catch_heading
        )

        right_layout.addWidget(
            self.catch_table
        )
        
        right_layout.addWidget(
            self.add_catch_button
        )
        right_layout.addWidget(
            self.edit_catch_button
        )
        right_layout.addWidget(
            self.delete_catch_button
        )
        
        right_layout.addWidget(
            self.fish_heading
        )

        right_layout.addWidget(
            self.fish_table
        )
        right_layout.addWidget(
            self.add_fish_button
        )

        right_layout.addWidget(
            self.edit_fish_button
        )

        right_layout.addWidget(
            self.delete_fish_button
        )
        
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