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

    def __init__(
        self,
        sam: int | None = None,
        ):
        super().__init__()
        self.result_action = None
        self.setWindowTitle(
            "New Catch Summary"
        )

        self.sam = QLineEdit()
        if sam is not None:
            self.sam.setText(str(sam))
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

        self.save_add_button = QPushButton(
            "Save & Add Another Species"
        )

        self.save_close_button = QPushButton(
            "Save & Close"
        )

        cancel_button = QPushButton(
            "Cancel"
        )

        cancel_button.clicked.connect(
            self.reject
        )
        self.save_add_button.clicked.connect(
            self.save_add
        )

        self.save_close_button.clicked.connect(
            self.save_close
        )
        
        layout = QVBoxLayout()

        layout.addLayout(form)
        
        layout.addWidget(
            self.save_add_button
        )

        layout.addWidget(
            self.save_close_button
        )

        layout.addWidget(
            cancel_button
        )

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

    def clear_species_fields(self):
        """Clear species entry fields."""

        self.spc.clear()
        self.catcnt.clear()
        self.biocnt.clear()

        self.spc.setFocus()

    def save_add(self):
        """Save and continue."""

        self.result_action = "add"

        self.accept()


    def save_close(self):
        """Save and close."""

        self.result_action = "close"

        self.accept()