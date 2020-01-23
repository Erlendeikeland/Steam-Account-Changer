import json
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import QPoint

from calls import SteamCalls

def create_font(family, size):
    font = QtGui.QFont()
    font.setFamily(family)
    font.setPointSize(size)
    return font

def str_bool(boolean):
    return boolean in ("True")

def get_path(file):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"ui/{file}.png").replace("\\", "/")

SMALL_FONT = create_font("Microsoft YaHei", 10)
MEDIUM_FONT = create_font("Microsoft YaHei", 12)

BG_COLOR = (49, 67, 79)
DARK_BG_COLOR = (39, 53, 64)
BUTTON_COLOR = (26, 115, 169)
BUTTON_PRESSED_COLOR = (17, 77, 112)
TEXT_COLOR = (255, 255, 255)


class MainWindow(object):
    def setup_ui(self, main):
        self.main = main
        self.centralwidget = QWidget(self.main)

        #Account label
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setGeometry(QtCore.QRect(40, 80, 151, 20))
        self.label_0.setFont(MEDIUM_FONT)
        self.label_0.setStyleSheet(f"color: rgb{TEXT_COLOR};")

        #Combobox
        self.combo_box_0 = QtWidgets.QComboBox(self.centralwidget)
        self.combo_box_0.setGeometry(QtCore.QRect(40, 110, 246, 40))
        self.combo_box_0.setFont(SMALL_FONT)

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")
        with open(path, "r") as f:
            data = json.load(f)
        checkbox_state_0 = str_bool(data["settings"]["0"])
        checkbox_state_1 = str_bool(data["settings"]["1"])

        #Checkbox
        self.check_box_0 = QtWidgets.QCheckBox(self.centralwidget)
        self.check_box_0.setGeometry(QtCore.QRect(80, 207, 161, 20))
        self.check_box_0.setFont(SMALL_FONT)
        self.check_box_0.setChecked(checkbox_state_0)
        self.check_box_0.stateChanged.connect(lambda: self.update_checkbox("0"))

        #Checkbox
        self.check_box_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.check_box_1.setGeometry(QtCore.QRect(80, 231, 161, 20))
        self.check_box_1.setFont(SMALL_FONT)
        self.check_box_1.setChecked(checkbox_state_1)
        self.check_box_1.stateChanged.connect(lambda: self.update_checkbox("1"))

        #Log-in button
        self.push_button_0 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_0.setGeometry(QtCore.QRect(60, 270, 206, 31))
        self.push_button_0.setFont(SMALL_FONT)
        self.push_button_0.clicked.connect(self.main.calls.login_user)

        #Add user button
        self.push_button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_1.setGeometry(QtCore.QRect(60, 310, 99, 31))
        self.push_button_1.setFont(SMALL_FONT)

        #remove user button
        self.push_button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_2.setGeometry(QtCore.QRect(168, 310, 98, 31))
        self.push_button_2.setFont(SMALL_FONT)
        self.push_button_2.clicked.connect(self.main.calls.remove_user)

        #Window titlebar Frame
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-40, -20, 391, 41))
        self.frame.setStyleSheet(f"background-color: rgb{DARK_BG_COLOR};")

        #Window exit button
        self.push_button_3 = QtWidgets.QPushButton(self.frame)
        self.push_button_3.setGeometry(QtCore.QRect(310, 20, 21, 21))
        self.push_button_3.clicked.connect(self.main.calls.btn_min_clicked)
        self.push_button_3.setStyleSheet(f"image: url({get_path('minimize_button')});")

        #Window minimize button
        self.push_button_4 = QtWidgets.QPushButton(self.frame)
        self.push_button_4.setGeometry(QtCore.QRect(340, 20, 21, 21))
        self.push_button_4.clicked.connect(self.main.calls.btn_close_clicked)
        self.push_button_4.setStyleSheet(f"image: url({get_path('close_button')});")

        self.retranslate_ui()
        self.main.setCentralWidget(self.centralwidget)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.main.calls.update_json(_translate)

        self.label_0.setText(_translate("Main", "Account"))
        self.check_box_0.setText(_translate("Main", "Launch to system tray"))
        self.check_box_1.setText(_translate("Main", "Remember me"))
        self.push_button_0.setText(_translate("Main", "Log in"))
        self.push_button_1.setText(_translate("Main", "Add user"))
        self.push_button_2.setText(_translate("Main", "Remove user"))

    def update_checkbox(self, num):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")
        with open(path, "r") as f:
            data = json.load(f)
        data["settings"][num] = str(not str_bool(data["settings"][num]))
        with open(path, "w") as f:
            data = json.dump(data, f, indent=4)


class AddUserWindow(object):
    def setup_ui(self, main):
        self.main = main
        self.centralwidget = QWidget(self.main)

        #Add new account label
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setGeometry(QtCore.QRect(40, 40, 151, 20))
        self.label_0.setFont(MEDIUM_FONT)
        self.label_0.setStyleSheet(f"color: rgb{TEXT_COLOR};")

        #Username label
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(40, 80, 71, 20))
        self.label_1.setFont(SMALL_FONT)
        self.label_1.setStyleSheet(f"color: rgb{TEXT_COLOR};")

        #Username lineedit
        self.line_edit_0 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_0.setGeometry(QtCore.QRect(40, 105, 246, 25))

        #Password label
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 140, 71, 20))
        self.label_2.setFont(SMALL_FONT)
        self.label_2.setStyleSheet(f"color: rgb{TEXT_COLOR};")

        #Password lineedit
        self.line_edit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_1.setGeometry(QtCore.QRect(40, 165, 246, 25))

        #Secret id label
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 200, 71, 20))
        self.label_3.setFont(SMALL_FONT)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")

        #Secret id lineedit
        self.line_edit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_2.setGeometry(QtCore.QRect(40, 225, 246, 25))

        #Add new account button
        self.push_button_0 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_0.setGeometry(QtCore.QRect(40, 280, 246, 31))
        self.push_button_0.setFont(SMALL_FONT)
        self.push_button_0.clicked.connect(lambda: self.main.calls.add_user(self))

        #Close window button
        self.push_button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_1.setGeometry(QtCore.QRect(230, 38, 55, 30))
        self.push_button_1.setStyleSheet(f"image: url({get_path('close_button')});")

        #Window titlebar Frame
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-40, -20, 391, 41))
        self.frame.setStyleSheet(f"background-color: rgb{DARK_BG_COLOR};")

        #Window exit button
        self.push_button_2 = QtWidgets.QPushButton(self.frame)
        self.push_button_2.setGeometry(QtCore.QRect(310, 20, 21, 21))
        self.push_button_2.clicked.connect(self.main.calls.btn_min_clicked)
        self.push_button_2.setStyleSheet(f"image: url({get_path('minimize_button')});")

        #Window minimize button
        self.push_button_3 = QtWidgets.QPushButton(self.frame)
        self.push_button_3.setGeometry(QtCore.QRect(340, 20, 21, 21))
        self.push_button_3.clicked.connect(self.main.calls.btn_close_clicked)
        self.push_button_3.setStyleSheet(f"image: url({get_path('close_button')});")

        self.retranslate_ui()
        self.main.setCentralWidget(self.centralwidget)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate

        self.label_0.setText(_translate("Form", "Add new account"))
        self.label_1.setText(_translate("Form", "Username:"))
        self.label_2.setText(_translate("Form", "Password:"))
        self.label_3.setText(_translate("Form", "Secret ID:"))
        self.push_button_0.setText(_translate("Form", "Add new account"))


class SteamGUI(QMainWindow):
    def __init__(self, parent=None):
        super(SteamGUI, self).__init__(parent)
        self.main_window = MainWindow()
        self.add_user_window = AddUserWindow()
        self.calls = SteamCalls(self)
        self.setup_ui()
        self.show_main_window()

    def setup_ui(self):
        self.setMinimumSize(QtCore.QSize(326, 384))
        self.setMaximumSize(QtCore.QSize(326, 384))
        self.setAutoFillBackground(False)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setStyleSheet(f"""
            *{{
                background-color: rgb{BG_COLOR};
            }}
            QPushButton {{
                color: rgb{TEXT_COLOR};
                background-color: rgb{BUTTON_COLOR};
                border-radius: 7px;
            }}
            QPushButton:pressed {{
                background-color: rgb{BUTTON_PRESSED_COLOR};
            }}
            QComboBox {{
                background-color: rgb{DARK_BG_COLOR};
                color: rgb{TEXT_COLOR};
                border-radius: 7px;
            }}
            QComboBox:drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-style: solid;
            }}
            QComboBox:down-arrow {{
                image: url({get_path("arrow_down")});
            }}
            QListView {{
                color: rgb{TEXT_COLOR};
                background-color: rgb{DARK_BG_COLOR};
                border-radius: 0px;
            }}
            QCheckBox {{
                color: rgb{TEXT_COLOR};
            }}
            QCheckBox::indicator:unchecked {{
                image: url({get_path("check_box_unmarked")});
                height: 16px;
                width: 16px;
            }}
            QCheckBox::indicator:checked {{
                image: url({get_path("check_box_marked")});
                height: 16px;
                width: 16px;
            }}
            QLineEdit {{
                color: rgb{TEXT_COLOR};
                background-color: rgb{DARK_BG_COLOR};
                border-radius: 7px;
            }}
        """)

        self.setCentralWidget(self.centralwidget)
        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Main", "Steam Account Changer"))

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        y = event.pos().y()
        x = event.pos().x()
        if y <= 20 and y >= 0:
            if x <= 270 and x >= 0:
                delta = QPoint(event.globalPos() - self.old_pos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()

    def show_main_window(self):
        self.main_window.setup_ui(self)
        self.main_window.push_button_1.clicked.connect(self.show_add_user_window)
        self.show()

    def show_add_user_window(self):
        self.add_user_window.setup_ui(self)
        self.add_user_window.push_button_1.clicked.connect(self.show_main_window)
        self.show()
