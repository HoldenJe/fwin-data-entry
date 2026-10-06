"""Main application window."""

from PySide6.QtWidgets import QLabel, QMainWindow


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FWIN Data Entry")

        label = QLabel("FWIN Data Entry")
        label.setMargin(20)

        self.setCentralWidget(label)