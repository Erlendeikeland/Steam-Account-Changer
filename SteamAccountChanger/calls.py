from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore

import threading
import json
import os

from hashlib import sha1
import base64
import struct
import hmac

from auth import SteamAUTH


class SteamCalls:
    def __init__(self, client):
        self.client = client

    def get_path(self, file):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{file}")

    def btn_close_clicked(self):
        self.client.close()

    def btn_min_clicked(self):
        self.client.showMinimized()

    def add_user(self, window):
        username = window.line_edit_0.text()
        password = window.line_edit_1.text()
        secret_id = window.line_edit_2.text()
        path = self.get_path("users.json")
        if not username:
            QMessageBox.about(self.client, "Error", "Cant add user without username")
            return False
        if not password:
            QMessageBox.about(self.client, "Error", "Cant add user without password")
            return False
        else:
            window.line_edit_0.setText("")
            window.line_edit_1.setText("")
            window.line_edit_2.setText("")
            with open(path, "r") as f:
                data = json.load(f)
            data[f"user{len(data)}"] = {"username": f"{username}", "password": f"{password}", "shared_secret": f"{secret_id}"}
            with open(path, "w") as f:
                data = json.dump(data, f, indent=4)
        self.client.show_main_window()

    def remove_user(self):
        path = self.get_path("users.json")
        pos = self.client.main_window.combo_box_0.currentText()
        with open(path, "r") as f:
            data = json.load(f)
        for i, item in enumerate(data):
            if pos == data[item].get("username"):
                del data[f"user{i}"]
                new_data = {}
                for i, item in enumerate(data):
                    if item == "settings":
                        new_data[f"settings"] = data[item]
                    else:
                        new_data[f"user{i}"] = data[item]
                self.client.main_window.combo_box_0.clear()
                for i, item in enumerate(new_data):
                    if item != "settings":
                        self.client.main_window.combo_box_0.addItem(new_data[item].get("username"))
                with open(path, "w") as f:
                    data = json.dump(new_data, f, indent=4)
                return True
        QMessageBox.about(self.client, "Error", "No users to remove")
        return False

    def login_user(self):
        path = self.get_path("users.json")
        pos = self.client.main_window.combo_box_0.currentText()
        check_box_0 = self.client.main_window.check_box_0.isChecked()
        check_box_1 = self.client.main_window.check_box_1.isChecked()
        with open(path, "r") as f:
            data = json.load(f)
        for i in data:
            if pos == data[i].get("username"):
                steam = SteamAUTH(data[i].get("username"), data[i].get("password"), data[i].get("shared_secret"), check_box_0, check_box_1)
                status = steam.run()
                if status != True:
                    QMessageBox.about(self.client, "Error", status)
                    return False
                else:
                    return True
        QMessageBox.about(self.client, "Error", "No users to login")
        return False

    def update_json(self, translate):
        path = self.get_path("users.json")
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {}
        new_data = {}
        for i, item in enumerate(data):
            if item == "settings":
                new_data[f"settings"] = data[item]
            else:
                new_data[f"user{i}"] = data[item]
        with open(path, "w") as f:
            json.dump(new_data, f, indent=4)
        if len(new_data) > 0:
            self.client.main_window.combo_box_0.clear()
            for i, item in enumerate(new_data):
                if item != "settings":
                    self.client.main_window.combo_box_0.addItem(new_data[item].get("username"))
