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
        self.effdt0.setInputMask(
            "0000-00-00"
        )

        self.efftm0.setInputMask(
            "00:00"
        )
        self.sitem0 = QLineEdit()

        self.grdepmin = QLineEdit()
        self.grdepmax = QLineEdit()

        self.effdt1 = QLineEdit()
        self.efftm1 = QLineEdit()
        self.effdt1.setInputMask(
            "0000-00-00"
        )

        self.efftm1.setInputMask(
            "00:00"
        )
        self.effst = QLineEdit()
        self.dd_lat0 = QLineEdit()
        self.dd_lon0 = QLineEdit()

        self.secchi = QLineEdit()

        self.crew = QLineEdit()

        self.comment = QTextEdit()

        form = QFormLayout()

        form.addRow("SAM", self.sam)
        form.addRow("GR", self.gr)
        form.addRow("AREA", self.area)
        form.addRow("Set Date  (yyyy-mm-dd)", self.effdt0)
        form.addRow("Set Time (hh:mm)", self.efftm0)
        form.addRow("Site Temp", self.sitem0)
        form.addRow("Latitude", self.dd_lat0)
        form.addRow("Longitude", self.dd_lon0)
        form.addRow("Secchi", self.secchi)
        form.addRow("Min Gear Depth", self.grdepmin)
        form.addRow("Max Gear Depth", self.grdepmax)
        form.addRow("Lift Date (yyyy-mm-dd)", self.effdt1)
        form.addRow("Lift Time (hh:mm)", self.efftm1)
        form.addRow("Effort Status", self.effst)
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

            "sitem0": self.sitem0.text(),

            "dd_lat0": self.dd_lat0.text(),
            "dd_lon0": self.dd_lon0.text(),

            "secchi": self.secchi.text(),

            "grdepmin": self.grdepmin.text(),
            "grdepmax": self.grdepmax.text(),

            "effdt1": self.effdt1.text(),
            "efftm1": self.efftm1.text(),

            "effst": self.effst.text(),

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
        self.sitem0.setText(
            "" if effort.sitem0 is None
            else str(effort.sitem0)
        )
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

        self.grdepmin.setText(
            "" if effort.grdepmin is None
            else str(effort.grdepmin)
        )

        self.grdepmax.setText(
            "" if effort.grdepmax is None
            else str(effort.grdepmax)
        )

        self.effdt1.setText(
            "" if effort.effdt1 is None
            else effort.effdt1
        )

        self.efftm1.setText(
            "" if effort.efftm1 is None
            else effort.efftm1
        )

        self.effst.setText(
            "" if effort.effst is None
            else str(effort.effst)
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
        self.sitem0.clear()

        self.grdepmin.clear()
        self.grdepmax.clear()

        self.effdt1.clear()
        self.efftm1.clear()

        self.effst.clear()
        self.comment.clear()

        # GR intentionally retained
        # Crew intentionally retained

        self.gr.setFocus()