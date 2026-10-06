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