"""Project workspace."""

from PySide6.QtWidgets import (
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
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Samples"))
        left_layout.addWidget(self.sam_list)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.project_label)
        right_layout.addWidget(self.sample_details)
        right_layout.addWidget(self.catch_summary_label)

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