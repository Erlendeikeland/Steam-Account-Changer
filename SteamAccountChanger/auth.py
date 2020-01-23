import time
import os

from hashlib import sha1
import base64
import struct
import hmac

from PIL import ImageGrab, Image
import numpy as np
import cv2

import subprocess
import win32api, win32con
import win32com.client


class SteamAUTH:
    def __init__(self, username, password, shared_secret, silent_login, remember_me):
        self.username = username
        self.password = password
        self.shared_secret = shared_secret
        self.silent_login = silent_login
        self.remember_me = remember_me
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
        template = cv2.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"ui/steam_{file}.png"), 0)
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.95)
        return loc

    def enter_2fa(self):
        self.shell.SendKeys(self.generate_one_time_code())
        self.shell.SendKeys("{ENTER}")

    def close_steam(self):
        os.system("taskkill /F /IM steam.exe")

    def open_steam(self):
        if self.silent_login == True:
            if self.remember_me == True:
                process = subprocess.Popen(f'"C:\Program Files (x86)\Steam\Steam.exe" -silent')
            elif self.remember_me == False:
                process = subprocess.Popen(f'"C:\Program Files (x86)\Steam\Steam.exe" -login {self.username} {self.password} -silent')
        elif self.silent_login == False:
            if self.remember_me == True:
                process = subprocess.Popen(f'"C:\Program Files (x86)\Steam\Steam.exe"')
            elif self.remember_me == False:
                process = subprocess.Popen(f'"C:\Program Files (x86)\Steam\Steam.exe" -login {self.username} {self.password}')

    def login(self, x, y):
        for _ in range(2):
            self.mouse_click(x, y)
        self.shell.SendKeys("{DELETE}")
        win32api.Sleep(50)
        self.shell.SendKeys(f"{self.username}")
        win32api.Sleep(50)
        self.shell.SendKeys("{TAB}")
        win32api.Sleep(50)
        self.shell.SendKeys(f"{self.password}")
        win32api.Sleep(50)
        self.shell.SendKeys("{TAB}")
        win32api.Sleep(50)
        self.shell.SendKeys(" ")
        win32api.Sleep(50)
        self.shell.SendKeys("{TAB}")
        win32api.Sleep(50)
        self.shell.SendKeys("{ENTER}")

    def mouse_click(self, posx, posy):
        click_x = posx + 130
        click_y = posy + 100
        win32api.SetCursorPos((click_x, click_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, click_x, click_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, click_x, click_y, 0, 0)

    def run(self):
        self.close_steam()
        self.open_steam()
        if self.remember_me == True:
            while True:
                y, x = self.image_match("login")
                if len(x) or len(y) > 0:
                    self.login(x, y)
                    break
        if self.shared_secret:
            while True:
                z, j = self.image_match("wrong")
                if len(z) or len(j) > 0:
                    self.close_steam()
                    return "Wrong username or password"
                x, y = self.image_match("guard")
                if len(x) or len(y) > 0:
                    self.enter_2fa()
                    return True
        return True
