import sys
from PyQt5.QtWidgets import QApplication

from gui import SteamGUI


def run():
    app = QApplication(sys.argv)
    gui = SteamGUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
