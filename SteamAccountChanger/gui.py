import os

from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint

from calls import SteamCalls


def create_font(family, size):
    font = QtGui.QFont()
    font.setFamily(family)
    font.setPointSize(size)
    return font

SMALL_FONT = create_font("Microsoft YaHei", 10)
MEDIUM_FONT = create_font("Microsoft YaHei", 12)

BG_COLOR = (49, 67, 79)
DARK_BG_COLOR = (39, 53, 64)
BUTTON_COLOR = (26, 115, 169)
BUTTON_PRESSED_COLOR = (17, 77, 112)
TEXT_COLOR = (255, 255, 255)

def get_path(file):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"ui/{file}.png").replace("\\", "/")


class SteamGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calls = SteamCalls(self)

    def create_font(self, family, size):
        font = QtGui.QFont()
        font.setFamily(family)
        font.setPointSize(size)
        return font

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
                image: url({get_path("check_box_marked")});
                height: 16px;
                width: 16px;
            }}
            QCheckBox::indicator:checked {{
                image: url({get_path("check_box_unmarked")});
                height: 16px;
                width: 16px;
            }}
        """)
        #Window titlebar Frame
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-40, -20, 391, 41))
        self.frame.setStyleSheet(f"background-color: rgb{DARK_BG_COLOR};")

        #Window exit button
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(310, 20, 21, 21))
        self.pushButton_5.clicked.connect(self.calls.btn_min_clicked)
        self.pushButton_5.setStyleSheet(f"""
            image: url({get_path("minimize_button")});
            height: 16px;
            width: 16px;
        """)

        #Window minimize button
        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(340, 20, 21, 21))
        self.pushButton_6.clicked.connect(self.calls.btn_close_clicked)
        self.pushButton_6.setStyleSheet(f"""
            image: url({get_path("close_button")});
            height: 16px;
            width: 16px;
        """)

        #Account label
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setGeometry(QtCore.QRect(40, 90, 71, 20))
        self.label_0.setFont(MEDIUM_FONT)
        self.label_0.setStyleSheet(f"color: rgb{TEXT_COLOR};")

        #Combobox
        self.combo_box_0 = QtWidgets.QComboBox(self.centralwidget)
        self.combo_box_0.setGeometry(QtCore.QRect(40, 120, 246, 41))
        self.combo_box_0.setFont(SMALL_FONT)

        #Checkbox
        self.check_box_0 = QtWidgets.QCheckBox(self.centralwidget)
        self.check_box_0.setGeometry(QtCore.QRect(80, 170, 161, 20))
        self.check_box_0.setFont(SMALL_FONT)

        #Log-in button
        self.push_button_0 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_0.setGeometry(QtCore.QRect(60, 270, 206, 31))
        self.push_button_0.setFont(SMALL_FONT)
        self.push_button_0.clicked.connect(self.calls.login_user)

        #Add user button
        self.push_button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_1.setGeometry(QtCore.QRect(60, 310, 99, 31))
        self.push_button_1.setFont(SMALL_FONT)
        self.push_button_1.clicked.connect(self.show_add_user_form)

        #remove user button
        self.push_button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_2.setGeometry(QtCore.QRect(168, 310, 98, 31))
        self.push_button_2.setFont(SMALL_FONT)
        self.push_button_2.clicked.connect(self.calls.remove_user)

        self.setCentralWidget(self.centralwidget)
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.oldPos = self.pos()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.calls.update_json(_translate)
        self.setWindowTitle(_translate("Main", "Steam Account Changer"))

        self.check_box_0.setText(_translate("Main", "Launch to system tray"))
        self.label_0.setText(_translate("Main", "Account"))
        self.push_button_0.setText(_translate("Main", "Log in"))
        self.push_button_1.setText(_translate("Main", "Add user"))
        self.push_button_2.setText(_translate("Main", "Remove user"))

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.pos().y() <= 20:
            if event.pos().x() <= 270:
                delta = QPoint(event.globalPos() - self.old_pos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()

    def show_add_user_form(self):
        self.add_user_form = SteamGUIForm(self.combo_box_0)
        self.add_user_form.setup_ui()
        self.add_user_form.show()


class SteamGUIForm(QWidget):
    def __init__(self, combo_box):
        super().__init__()
        self.calls = SteamCalls(self)
        self.combo_box = combo_box

    def setup_ui(self):
        self.setMinimumSize(QtCore.QSize(295, 295))
        self.setMaximumSize(QtCore.QSize(295, 295))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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
            QLineEdit {{
                color: rgb{TEXT_COLOR};
                background-color: rgb{DARK_BG_COLOR};
                border-radius: 7px;
            }}
        """)
        #Window titlebar frame
        self.frame_0 = QtWidgets.QFrame(self)
        self.frame_0.setGeometry(QtCore.QRect(-70, -20, 391, 41))
        self.frame_0.setStyleSheet(f"background-color: rgb{DARK_BG_COLOR};")

        #Window exit button
        self.push_button_0 = QtWidgets.QPushButton(self.frame_0)
        self.push_button_0.setGeometry(QtCore.QRect(340, 20, 21, 21))
        self.push_button_0.clicked.connect(self.calls.btn_close_clicked)
        self.push_button_0.setStyleSheet(f"""
            image: url({get_path("close_button")});
            height: 16px;
            width: 16px;
        """)

        #Window minimize button
        self.push_button_1 = QtWidgets.QPushButton(self.frame_0)
        self.push_button_1.setGeometry(QtCore.QRect(310, 20, 21, 21))
        self.push_button_1.clicked.connect(self.calls.btn_min_clicked)
        self.push_button_1.setStyleSheet(f"""
            image: url({get_path("minimize_button")});
            height: 16px;
            width: 16px;
        """)

        #Add new account label
        self.label_0 = QtWidgets.QLabel(self)
        self.label_0.setGeometry(QtCore.QRect(20, 40, 151, 20))
        self.label_0.setFont(MEDIUM_FONT)
        self.label_0.setStyleSheet(f"color: rgb{TEXT_COLOR};")

        #Username label
        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(20, 80, 71, 20))
        self.label_1.setFont(SMALL_FONT)
        self.label_1.setStyleSheet(f"color: rgb{TEXT_COLOR};")

        #Username lineedit
        self.line_edit_0 = QtWidgets.QLineEdit(self)
        self.line_edit_0.setGeometry(QtCore.QRect(20, 100, 241, 25))

        #Password label
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 130, 71, 20))
        self.label_2.setFont(SMALL_FONT)
        self.label_2.setStyleSheet(f"color: rgb{TEXT_COLOR};")

        #Password lineedit
        self.line_edit_1 = QtWidgets.QLineEdit(self)
        self.line_edit_1.setGeometry(QtCore.QRect(20, 150, 241, 25))

        #Secret id label
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 180, 71, 20))
        self.label_3.setFont(SMALL_FONT)
        self.label_3.setStyleSheet(f"color: rgb{TEXT_COLOR};")

        #Secret id lineedit
        self.line_edit_2 = QtWidgets.QLineEdit(self)
        self.line_edit_2.setGeometry(QtCore.QRect(20, 200, 241, 25))

        #Add new account button
        self.push_button_2 = QtWidgets.QPushButton(self)
        self.push_button_2.setGeometry(QtCore.QRect(20, 240, 241, 31))
        self.push_button_2.setFont(SMALL_FONT)
        self.push_button_2.clicked.connect(lambda: self.calls.add_user(self.combo_box))

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.oldPos = self.pos()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))

        self.label_0.setText(_translate("Form", "Add new account"))
        self.label_1.setText(_translate("Form", "Username:"))
        self.label_2.setText(_translate("Form", "Password:"))
        self.label_3.setText(_translate("Form", "Secret ID:"))
        self.push_button_2.setText(_translate("Form", "Add new account"))

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.pos().y() <= 20:
            if event.pos().x() <= 240:
                delta = QPoint(event.globalPos() - self.old_pos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()
