"""Effort entry dialog."""

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class EffortDialog(QDialog):
    """FN121 effort entry dialog."""

    def __init__(self, sam: int | None = None):
        super().__init__()

        self.setWindowTitle("New Effort")

        self.sam = QLineEdit()
        if sam is not None:
            self.sam.setText(str(sam))
        self.gr = QLineEdit()
        self.area = QLineEdit()

        self.effdt0 = QLineEdit()
        self.efftm0 = QLineEdit()

        self.dd_lat0 = QLineEdit()
        self.dd_lon0 = QLineEdit()

        self.secchi = QLineEdit()

        self.crew = QLineEdit()

        self.comment = QTextEdit()

        form = QFormLayout()

        form.addRow("SAM", self.sam)
        form.addRow("GR", self.gr)
        form.addRow("AREA", self.area)
        form.addRow("Set Date", self.effdt0)
        form.addRow("Set Time", self.efftm0)
        form.addRow("Latitude", self.dd_lat0)
        form.addRow("Longitude", self.dd_lon0)
        form.addRow("Secchi", self.secchi)
        form.addRow("Crew", self.crew)
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

    def get_data(self) -> dict:
        """Return dialog values."""

        return {
            "sam": self.sam.text(),
            "gr": self.gr.text(),
            "area": self.area.text(),
            "effdt0": self.effdt0.text(),
            "efftm0": self.efftm0.text(),
            "dd_lat0": self.dd_lat0.text(),
            "dd_lon0": self.dd_lon0.text(),
            "secchi": self.secchi.text(),
            "crew": self.crew.text(),
            "comment": self.comment.toPlainText(),
        }