#!/usr/bin/env python3

import sys
from PySide2.QtWidgets import QApplication

from gui.windows import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
    del app