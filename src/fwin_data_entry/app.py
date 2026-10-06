"""Application entry point."""

import sys

from PySide6.QtWidgets import QApplication

from fwin_data_entry.gui.main_window import MainWindow


def main():
    """Run application."""

    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(1000, 700)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
