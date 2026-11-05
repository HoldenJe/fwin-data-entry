"""Age record entry dialog."""

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class AgeRecordDialog(QDialog):
    """FN127 entry dialog."""

    def __init__(
        self,
        ageid: int | None = None,
        edit_mode: bool = False,
    ):
        super().__init__()

        self.edit_mode = edit_mode

        self.setWindowTitle(
            "Age Data"
        )

        self.ageid = QLineEdit()

        if ageid is not None:
            self.ageid.setText(
                str(ageid)
            )

        self.agemt = QLineEdit()
        self.agea = QLineEdit()
        self.nca = QLineEdit()
        self.edge = QLineEdit()
        self.conf = QLineEdit()

        form = QFormLayout()

        form.addRow(
            "AGEID",
            self.ageid,
        )

        form.addRow(
            "AGEMT",
            self.agemt,
        )

        form.addRow(
            "AGEA",
            self.agea,
        )

        form.addRow(
            "NCA",
            self.nca,
        )

        form.addRow(
            "EDGE",
            self.edge,
        )

        form.addRow(
            "CONF",
            self.conf,
        )

        save_button = QPushButton(
            "Save"
        )

        cancel_button = QPushButton(
            "Cancel"
        )

        save_button.clicked.connect(
            self.accept
        )

        cancel_button.clicked.connect(
            self.reject
        )

        layout = QVBoxLayout()

        layout.addLayout(form)
        layout.addWidget(save_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def get_data(self):
        """Return form data."""

        return {
            "ageid": self.ageid.text(),
            "agemt": self.agemt.text(),
            "agea": self.agea.text(),
            "nca": self.nca.text(),
            "edge": self.edge.text(),
            "conf": self.conf.text(),
        }
