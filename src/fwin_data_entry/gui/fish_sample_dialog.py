"""Fish sample entry dialog."""

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class FishSampleDialog(QDialog):
    """FN125 entry dialog."""

    def __init__(
        self,
        sam: int | None = None,
        fish: int | None = None,
    ):
        super().__init__()
        self.result_action = None
        self.setWindowTitle(
            "New Fish Sample"
        )

        self.sam = QLineEdit()
        if sam is not None:
            self.sam.setText(str(sam))
        self.spc = QLineEdit()
        self.fish = QLineEdit()
        if fish is not None:
            self.fish.setText(str(fish))
        self.flen = QLineEdit()
        self.tlen = QLineEdit()
        self.rwt = QLineEdit()

        self.sex = QLineEdit()
        self.mat = QLineEdit()

        self.agest = QLineEdit()
        self.stom = QLineEdit()
        self.taxon = QLineEdit()

        self.gonwt = QLineEdit()
        self.eviswt = QLineEdit()

        self.tissue = QLineEdit()

        form = QFormLayout()

        form.addRow("SAM", self.sam)
        form.addRow("SPC", self.spc)
        form.addRow("FISH", self.fish)

        form.addRow("FLEN", self.flen)
        form.addRow("TLEN", self.tlen)
        form.addRow("RWT", self.rwt)

        form.addRow("SEX", self.sex)
        form.addRow("MAT", self.mat)

        form.addRow("AGEST", self.agest)
        form.addRow("STOM", self.stom)
        form.addRow("TAXON", self.taxon)

        form.addRow("GONWT", self.gonwt)
        form.addRow("EVISWT", self.eviswt)

        form.addRow("TISSUE", self.tissue)

        self.save_add_button = QPushButton(
            "Save & Add Another Fish"
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
        """Return form data."""

        return {
            "sam": self.sam.text(),
            "spc": self.spc.text(),
            "fish": self.fish.text(),
            "flen": self.flen.text(),
            "tlen": self.tlen.text(),
            "rwt": self.rwt.text(),
            "sex": self.sex.text(),
            "mat": self.mat.text(),
            "agest": self.agest.text(),
            "stom": self.stom.text(),
            "taxon": self.taxon.text(),
            "gonwt": self.gonwt.text(),
            "eviswt": self.eviswt.text(),
            "tissue": self.tissue.text(),
        }

    def save_add(self):
        """Save and continue."""

        self.result_action = "add"

        self.accept()


    def save_close(self):
        """Save and close."""

        self.result_action = "close"

        self.accept()

    def clear_fish_fields(self):
        """Prepare for next fish."""

        self.flen.clear()
        self.tlen.clear()
        self.rwt.clear()

        self.sex.clear()
        self.mat.clear()

        self.agest.clear()
        self.stom.clear()

        self.taxon.clear()

        self.gonwt.clear()
        self.eviswt.clear()

        self.tissue.clear()

        self.flen.setFocus()