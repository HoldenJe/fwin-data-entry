"""Catch summary entry dialog."""

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class CatchSummaryDialog(QDialog):
    """FN123 entry dialog."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "New Catch Summary"
        )

        self.sam = QLineEdit()
        self.eff = QLineEdit("999")

        self.spc = QLineEdit()

        self.catcnt = QLineEdit()
        self.biocnt = QLineEdit()

        form = QFormLayout()

        form.addRow("SAM", self.sam)
        form.addRow("EFF", self.eff)
        form.addRow("SPC", self.spc)
        form.addRow("Catch Count", self.catcnt)
        form.addRow("Bio Count", self.biocnt)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()

        layout.addLayout(form)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def get_data(self):
        """Return dialog values."""

        return {
            "sam": self.sam.text(),
            "eff": self.eff.text(),
            "spc": self.spc.text(),
            "catcnt": self.catcnt.text(),
            "biocnt": self.biocnt.text(),
        }