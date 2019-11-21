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
import win32api
import win32com.client


class SteamAUTH:
    def __init__(self, username, password, shared_secret, silent_login):
        self.username = username
        self.password = password
        self.shared_secret = shared_secret
        self.silent_login = silent_login
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
        template = cv2.imread(f"ui/steam_{file}.png", 0)
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.95)
        return loc

    def enter_2fa(self):
        self.shell.SendKeys(self.generate_one_time_code())
        self.shell.SendKeys("{ENTER}")

    def close_steam(self):
        os.system("taskkill /F /IM steam.exe")

    def open_steam(self):
        if self.silent_login == False:
            process = subprocess.Popen(f'"C:\Program Files (x86)\Steam\Steam.exe" -login {self.username} {self.password} -silent')
        elif self.silent_login == True:
            process = subprocess.Popen(f'"C:\Program Files (x86)\Steam\Steam.exe" -login {self.username} {self.password}')

    def run(self):
        self.close_steam()
        self.open_steam()
        while True:
            z, j = self.image_match("wrong")
            if len(z) or len(j) > 0:
                self.close_steam()
                return "Wrong username or password"
            x, y = self.image_match("guard")
            if len(x) or len(y) > 0:
                self.enter_2fa()
                return True
