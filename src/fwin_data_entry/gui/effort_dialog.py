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

    def __init__(
            self,
            sam: int | None = None,
            edit_mode: bool = False,
        ):

        super().__init__()
        self.edit_mode = edit_mode
        self.result_action = None
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

        if edit_mode:

            self.save_close_button = QPushButton(
                "Save Changes"
            )

            self.save_add_button = None

        else:

            self.save_add_button = QPushButton(
                "Save & Add Another SAM"
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

        if self.save_add_button is not None:

            self.save_add_button.clicked.connect(
                self.save_add
            )

        self.save_close_button.clicked.connect(
            self.save_close
        )
        layout = QVBoxLayout()

        layout.addLayout(form)
        if self.save_add_button is not None:

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

    def load_effort(
        self,
        effort,
    ):
        """Populate dialog with existing values."""

        self.sam.setText(str(effort.sam))

        self.gr.setText(effort.gr)
        self.area.setText(effort.area)

        self.effdt0.setText(effort.effdt0)
        self.efftm0.setText(effort.efftm0)

        self.dd_lat0.setText(
            "" if effort.dd_lat0 is None
            else str(effort.dd_lat0)
        )

        self.dd_lon0.setText(
            "" if effort.dd_lon0 is None
            else str(effort.dd_lon0)
        )

        self.secchi.setText(
            "" if effort.secchi is None
            else str(effort.secchi)
        )

        self.crew.setText(effort.crew)

        self.comment.setPlainText(
            effort.comment
        )

    def save_add(self):
        """Save and continue."""

        self.result_action = "add"

        self.accept()


    def save_close(self):
        """Save and close."""

        self.result_action = "close"

        self.accept()

    def clear_sam_fields(self):
        """Prepare for next SAM."""

        self.area.clear()

        self.effdt0.clear()
        self.efftm0.clear()

        self.dd_lat0.clear()
        self.dd_lon0.clear()

        self.secchi.clear()

        self.comment.clear()

        self.gr.setFocus()