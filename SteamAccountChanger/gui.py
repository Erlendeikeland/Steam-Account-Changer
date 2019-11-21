import os

from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint

from calls import SteamCalls

class SteamGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calls = SteamCalls(self)

    def setupUi(self):
        self.resize(326, 384)
        self.setMinimumSize(QtCore.QSize(326, 384))
        self.setMaximumSize(QtCore.QSize(326, 384))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setAutoFillBackground(False)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("""
            *{
                background-color: rgb(49, 67, 79);
            }
            QPushButton {
                color: rgb(255, 255, 255);
                background-color: rgb(26, 115, 169);
                border-radius: 7px;
            }
            QPushButton:pressed {
                background-color: rgb(17, 77, 112);
            }
            QComboBox {
                background-color: rgb(39, 53, 64);
                color: rgb(255, 255, 255);
                border-radius: 7px;
            }
            QComboBox:drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-style: solid;
            }
            QComboBox:down-arrow {
                image: url(ui/arrow_down.png);
            }
            QListView {
                color: rgb(255, 255, 255);
                background-color: rgb(39, 53, 64);
                border-radius: 0px;
            }
            QCheckBox {
                color: rgb(255, 255, 255);
            }
            QCheckBox::indicator:unchecked {
                image: url(ui/check_box_marked.png);
                height: 16px;
                width: 16px;
            }
            QCheckBox::indicator:checked {
                image: url(ui/check_box_unmarked.png);
                height: 16px;
                width: 16px;
            }
        """)
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(self)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(80, 170, 161, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 270, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.clicked.connect(self.calls.login_user)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(40, 120, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 310, 91, 31))
        self.pushButton_2.clicked.connect(self.show_add_user_form)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-40, -20, 391, 41))
        self.frame.setStyleSheet("background-color: rgb(39, 53, 64);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(310, 20, 21, 21))
        self.pushButton_5.setStyleSheet("""
            image: url(ui/minimize_button.png);
            height: 16px;
            width: 16px;
        """)
        self.pushButton_5.clicked.connect(self.calls.btn_min_clicked)
        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(340, 20, 21, 21))
        self.pushButton_6.setStyleSheet("""
            image: url(ui/close_button.png);
            height: 16px;
            width: 16px;
        """)
        self.pushButton_6.clicked.connect(self.calls.btn_close_clicked)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(170, 310, 91, 31))
        self.pushButton_3.clicked.connect(self.calls.remove_user)
        self.setCentralWidget(self.centralwidget)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.oldPos = self.pos()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.calls.update_json(_translate)
        self.setWindowTitle(_translate("Main", "Steam Account Changer"))
        self.checkBox.setText(_translate("Main", "Launch to system tray"))
        self.pushButton.setText(_translate("Main", "Log in"))
        self.label_2.setText(_translate("Main", "Account"))
        self.pushButton_2.setText(_translate("Main", "Add user"))
        self.pushButton_3.setText(_translate("Main", "Remove user"))

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.pos().y() <= 20:
            if event.pos().x() <= 270:
                delta = QPoint(event.globalPos() - self.old_pos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()

    def show_add_user_form(self):
        self.add_user_form = SteamGUIForm(self.comboBox)
        self.add_user_form.setupUi()
        self.add_user_form.show()


class SteamGUIForm(QWidget):
    def __init__(self, combo_box):
        super().__init__()
        self.calls = SteamCalls(self)
        self.combo_box = combo_box

    def setupUi(self):
        self.resize(295, 295)
        self.setMinimumSize(QtCore.QSize(295, 295))
        self.setMaximumSize(QtCore.QSize(295, 295))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("""
            *{
                background-color: rgb(49, 67, 79);
            }
            QPushButton {
                color: rgb(255, 255, 255);
                background-color: rgb(26, 115, 169);
                border-radius: 7px;z|
            }
            QPushButton:pressed {
                background-color: rgb(17, 77, 112);
            }
            QLineEdit {
                color: rgb(255, 255, 255);
                background-color:  rgb(39, 53, 64);
                border-radius: 7px;
            }
        """)
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(-70, -20, 391, 41))
        self.frame.setStyleSheet("background-color: rgb(39, 53, 64);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(310, 20, 21, 21))
        self.pushButton_5.setStyleSheet("""
            image: url(ui/minimize_button.png);
            height: 16px;
            width: 16px;
        """)
        self.pushButton_5.clicked.connect(self.calls.btn_min_clicked)
        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(340, 20, 21, 21))
        self.pushButton_6.setStyleSheet("""
            image: url(ui/close_button.png);
            height: 16px;
            width: 16px;
        """)
        self.pushButton_6.clicked.connect(self.calls.btn_close_clicked)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 151, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(20, 100, 241, 25))
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(20, 130, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 150, 241, 25))
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(20, 180, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 200, 241, 25))
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(20, 240, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.clicked.connect(lambda: self.calls.add_user(self.combo_box))

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.oldPos = self.pos()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Add new user"))
        self.label_2.setText(_translate("Form", "Add new account"))
        self.label_3.setText(_translate("Form", "Username:"))
        self.label_4.setText(_translate("Form", "Password:"))
        self.label_5.setText(_translate("Form", "Secret ID:"))
        self.pushButton.setText(_translate("Form", "Add new account"))

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.pos().y() <= 20:
            if event.pos().x() <= 240:
                delta = QPoint(event.globalPos() - self.old_pos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()
