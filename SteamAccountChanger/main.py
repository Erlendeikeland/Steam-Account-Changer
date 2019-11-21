import sys
from PyQt5.QtWidgets import QApplication

from gui import SteamGUI


def run():
    try:
        app = QApplication(sys.argv)
        gui = SteamGUI()
        gui.setupUi()
        gui.show()
    except Exception as E:
        print(E)
    finally:
        sys.exit(app.exec_())


if __name__ == "__main__":
    run()
