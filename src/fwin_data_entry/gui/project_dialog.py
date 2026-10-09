"""Project creation dialog."""

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QFileDialog,
)


class ProjectDialog(QDialog):
    """Project creation dialog."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Project")

        self.prj_cd = QLineEdit()
        self.prj_nm = QLineEdit()
        self.wby_nm = QLineEdit()
        self.start_date = QLineEdit()
        self.end_date = QLineEdit()
        self.comment = QTextEdit()
        self.db_location = QLineEdit()
        self.browse_button = QPushButton(
            "Browse..."
        )

        form = QFormLayout()

        form.addRow("Project Code", self.prj_cd)
        form.addRow("Project Name", self.prj_nm)
        form.addRow("Waterbody", self.wby_nm)
        form.addRow("Start Date", self.start_date)
        form.addRow("End Date", self.end_date)
        form.addRow(
            "Database Location",
            self.db_location,
        )

        form.addRow(
            "",
            self.browse_button,
        )
        form.addRow("Comment", self.comment)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)
        self.browse_button.clicked.connect(
            self.select_location
        )

    def get_data(self) -> dict:
        """Return dialog values."""

        return {
            "prj_cd": self.prj_cd.text(),
            "prj_nm": self.prj_nm.text(),
            "wby_nm": self.wby_nm.text(),
            "prj_date0": self.start_date.text(),
            "prj_date1": self.end_date.text(),
            "comment": self.comment.toPlainText(),
            "db_location": self.db_location.text(),
        }

    def select_location(self):
        """Select project location."""

        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Project Location",
        )

        if directory:

            self.db_location.setText(
                directory
            )