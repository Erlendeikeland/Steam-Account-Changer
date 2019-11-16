import time
import json
import os

from hashlib import sha1
import base64
import struct
import hmac

from PIL import ImageGrab, Image
import numpy as np
import cv2

import subprocess
import win32api
import win32com.client

import tkinter as tk
from tkinter.ttk import *


class SteamAUTH:
    def __init__(self, username, password, shared_secret, silent_login):
        self.username = username
        self.password = password
        self.shared_secret = shared_secret
        self.silent_login = silent_login.get()
        self.shell = win32com.client.Dispatch("WScript.Shell")

    def generate_one_time_code(self):
        timestamp = int(time.time())
        time_buffer = struct.pack(">Q", timestamp // 30)
        time_hmac = hmac.new(base64.b64decode(self.shared_secret), time_buffer, digestmod=sha1).digest()
        begin = ord(time_hmac[19:20]) & 0xf
        full_code = struct.unpack(">I", time_hmac[begin:begin + 4])[0] & 0x7fffffff
        chars = "23456789BCDFGHJKMNPQRTVWXY"
        code = ""
        for _ in range(5):
            full_code, i = divmod(full_code, len(chars))
            code += chars[i]
        return code

    def image_match(self, file):
        img_grab = ImageGrab.grab(bbox=[0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)])
        img_rgb = np.array(img_grab, dtype="uint8")
        img = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"steam_{file}.png"), 0)
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.95)
        return loc

    def enter_2fa(self):
        self.shell.SendKeys(self.generate_one_time_code())
        self.shell.SendKeys("{ENTER}")

    def close_steam(self):
        os.system("taskkill /F /IM steam.exe")

    def open_steam(self):
        if self.silent_login == 1:
            process = subprocess.Popen(f'"C:\Program Files (x86)\Steam\Steam.exe" -login {self.username} {self.password} -silent')
        elif self.silent_login == 0:
            process = subprocess.Popen(f'"C:\Program Files (x86)\Steam\Steam.exe" -login {self.username} {self.password}')

    def run(self):
        self.close_steam()
        self.open_steam()
        while True:
            z, j = self.image_match("wrong")
            if len(z) or len(j) > 0:
                messagebox.showinfo("Error", "Wrong password or username")
                self.close_steam()
                return False
            if self.shared_secret == "":
                break
            x, y = self.image_match("guard")
            if len(x) or len(y) > 0:
                return self.enter_2fa()


class SteamGUI:
    def __init__(self):
        self.window = tk.Tk()

    def get_path(self, file):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{file}")

    def draw(self):
        path = self.get_path("users.json")
        self.window.title("Steam Account Changer")
        self.window.geometry("339x350")
        self.window.iconbitmap(self.get_path("icon.ico"))
        self.window.resizable(False, False)

        self.combo = Combobox(self.window, width=33, state="readonly")
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {}
        new_data = {}
        for i, item in enumerate(data):
            new_data[f"user{i}"] = data[item]
        with open(path, "w") as f:
            json.dump(new_data, f, indent=4)
        if len(new_data) < 1:
            self.combo["values"] = {}
        else:
            self.combo["values"] = [new_data[i].get("username") for i in new_data]
        self.combo.grid(column=1, row=2, columnspan=10, pady=(8, 3))
        self.combo.current(0)

        self.top1 = tk.Label(self.window, text="Account", font="Arial 15 bold")
        self.top1.grid(column=1, row=0, columnspan=2, sticky="W", pady=(10, 0))

        self.login_user_btn = tk.Button(self.window, text="Login", width=14, command=self.login_user)
        self.login_user_btn.grid(column=1, row=3, columnspan=1, pady=(1, 0), sticky="W")

        self.remove_user_btn = tk.Button(self.window, text="Remove user", width=14, command=self.remove_user)
        self.remove_user_btn.grid(column=1, row=3, columnspan=1, pady=(1, 0), sticky="E")

        self.silent_login = tk.IntVar(value=1)
        self.check_box = tk.Checkbutton(self.window, variable=self.silent_login, text="Launch steam to system tray")
        self.check_box.grid(column=1, row=4, sticky="W", pady=(0, 50))

        self.top2 = Label(self.window, text="Add new account", font="Arial 15 bold")
        self.top2.grid(column=1, row=9, columnspan=2, sticky="W")

        self.username_lbl = tk.Label(self.window, text="Username:")
        self.username_lbl.grid(column=0, row=10, pady=(10, 3), sticky="E")
        self.username_txt = tk.Entry(self.window, width=36)
        self.username_txt.grid(column=1, row=10, pady=(10, 3))

        self.password_lbl = tk.Label(self.window, text="Password:")
        self.password_lbl.grid(column=0, row=11, pady=3, sticky="E")
        self.password_txt = tk.Entry(self.window, width=36)
        self.password_txt.grid(column=1, row=11, pady=3)

        self.secret_lbl = tk.Label(self.window, text="Secret id:")
        self.secret_lbl.grid(column=0, row=12, pady=3, sticky="E")
        self.secret_txt = tk.Entry(self.window, width=36)
        self.secret_txt.grid(column=1, row=12, pady=3)

        self.add_user_btn = tk.Button(self.window, text="Add user", width=30, command=self.add_user)
        self.add_user_btn.grid(column=1, row=13, columnspan=1, pady=3)

    def add_user(self):
        username = self.username_txt.get()
        password = self.password_txt.get()
        secret_id = self.secret_txt.get()
        path = self.get_path("users.json")
        if not username:
            messagebox.showinfo("Error", "Cant add user without username")
            return False
        if not password:
            messagebox.showinfo("Error", "Cant add user without password")
            return False
        else:
            self.username_txt.delete(0, "end")
            self.password_txt.delete(0, "end")
            self.secret_txt.delete(0, "end")
            with open(path, "r") as f:
                data = json.load(f)
            data[f"user{len(data)}"] = {"username": f"{username}", "password": f"{password}", "shared_secret": f"{secret_id}"}
            self.combo["values"] = [data[i].get("username") for i in data]
            with open(path, "w") as f:
                data = json.dump(data, f, indent=4)

    def remove_user(self):
        pos = self.combo.current()
        path = self.get_path("users.json")
        with open(path, "r") as f:
            data = json.load(f)
        if not data:
            messagebox.showinfo("Error", "No users to remove")
            return False
        else:
            del data[f"user{pos}"]
            self.combo["values"] = [data[i].get("username") for i in data]
            self.combo.set("")
            new_data = {}
            for i, item in enumerate(data):
                new_data[f"user{i}"] = data[item]
            with open(path, "w") as f:
                data = json.dump(new_data, f, indent=4)

    def login_user(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")
        pos = self.combo.current()
        with open(path) as f:
            data = json.load(f).get(f"user{pos}")
        if not data:
            messagebox.showinfo("Error", "No users to login")
        else:
            steam = SteamAUTH(data.get("username"), data.get("password"), data.get("shared_secret"), self.silent_login)
            steam.run()

    def run(self):
        self.draw()
        self.window.mainloop()


if __name__ == "__main__":
    steam_gui = SteamGUI()
    steam_gui.run()
