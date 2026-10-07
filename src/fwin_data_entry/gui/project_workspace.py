"""Project workspace."""

from PySide6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QLabel,
    QListWidget,
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

        self.sam_list = QListWidget()

        self.sample_details = QLabel(
            "No sample selected"
        )
        self.catch_summary_label = QLabel(
            "No catch summaries"
        )
        self.fish_label = QLabel(
            "No fish samples"
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

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.project_label)
        right_layout.addWidget(self.sample_details)
        right_layout.addWidget(self.catch_summary_label)
        right_layout.addWidget(self.fish_label)
        right_layout.addWidget(
            self.add_catch_button
        )

        right_layout.addWidget(
            self.add_fish_button
        )

        layout = QHBoxLayout()

        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 3)

        self.setLayout(layout)

    def set_sample_details(
        self,
        text: str,
    ):
        """Display sample details."""

        self.sample_details.setText(text)