import random
import time
import warnings
from mytools.common.files import CSV
from mytools.common.keyboard import Keyboard
from threading import Thread

import PySimpleGUI as sg
import numpy as np
import pandas as pd
import pyautogui

keyboard = Keyboard()


class Switch:
    """Start switching windows with ease"""

    def __init__(self, no_of_windows, _timer=5.0, _no_of_times=0, hotkey=['Control', 'F']):
        """
        All constructors defined here
        :param no_of_windows: current number of windows opened
        :param _timer: time between each swap
        :param _no_of_times: number of times the swap occur
        :param hotkey: Force quit using these keys
        """
        self.windows = no_of_windows
        self.timer = _timer
        self.no_of_times = _no_of_times
        self.hotkey = hotkey

    def __switch_windows(self):
        for x in range(1, self.windows + 1):
            pyautogui.keyDown("ALT")
            for _ in range(x):
                pyautogui.typewrite(['TAB'])
            pyautogui.keyUp("ALT")
            t = 0.0
            while t <= self.timer:
                t += 0.1
                time.sleep(0.1)
                if self.__poll():
                    return True

    def start_switching(self):
        """Start switching windows"""
        if self.no_of_times == 0:
            while True:
                if self.__switch_windows():
                    break
        else:
            for s in range(self.no_of_times):
                if self.__switch_windows():
                    break
        return True

    def __poll(self):
        for key in self.hotkey:
            if keyboard.is_pressed(key):
                pass
            else:
                return False
        return True


class KeepOnTopWindow:
    """Instantly creates window that stay over all other apps"""

    def __init__(self):
        pass

    def __mouse_action(self, action):
        import win32api
        def _down():
            mouse_click = win32api.GetKeyState(0x01)
            if mouse_click < 0:
                return True

        def _up():
            mouse_click = win32api.GetKeyState(0x01)
            if mouse_click >= 0:
                return True

        def _location():
            return win32api.GetCursorPos()

        return locals()[f"_{action}"]()

    def create_window(self, __rect):
        """Pass rectangle to make window"""
        _size = __rect[2] - __rect[0], __rect[3] - __rect[1]
        layout = [
            [sg.B("Exit", size=(10, 2))],
        ]
        window = sg.Window("", layout=layout, keep_on_top=True, grab_anywhere=True,
                           finalize=True, no_titlebar=True, size=_size)
        window.move(__rect[0], __rect[1])
        while True:
            event, _ = window.read()
            if event == 'Exit':
                break
        window.close()

    def get_location(self):
        """
        Get rectangle to create window,
        :returns: rectangle, [x, y, x+w, y+h]
        """
        layout = [[sg.Graph((1920, 1080), (0, 1080), (1920, 0), background_color="white", key="graph")]]
        window = sg.Window("", layout=layout, keep_on_top=True,
                           finalize=True, no_titlebar=True, background_color="white", alpha_channel=0.2)
        window.maximize()
        check = False
        while True:
            event, values = window.read(timeout=10)
            graph = window["graph"]
            if event == sg.WINDOW_CLOSED or keyboard.is_pressed("escape"):
                window.close()
                return False
            elif self.__mouse_action('down') and not check:
                check = True
                starting_pos = (self.__mouse_action('location')[0] - 14, self.__mouse_action('location')[1] - 7)
            elif self.__mouse_action('down'):
                current_pos = self.__mouse_action('location')
                graph.erase()
                graph.draw_rectangle(starting_pos, current_pos, line_color="#FF0000", line_width=3)
            elif self.__mouse_action('up') and check:
                break
        window.close()
        rect = starting_pos[0] + 15, starting_pos[1] + 5, current_pos[0] + 12, current_pos[1] + 8
        return rect


class Freeze:
    """
    Freeze the window for certain key_sequence to be pressed or for timer
    Do not use timer and key_sequence at the same time to avoid crash!
    """

    def __init__(self, _timer: float = None, _key_seq: list = None, _transparent: bool = False):
        assert _timer is not None or _key_seq is not None
        self.timer = _timer
        self.password = _key_seq
        self.enforce = ['Control', 'Alt', 'D']
        self._alpha = 0.1 if _transparent else 1

    def __freeze(self):
        if self.timer is not None and self.password is not None:
            warnings.warn("Do not use timer and key sequence simultaneously to avoid crash", FutureWarning,
                          stacklevel=2)
        window = sg.Window("", layout=[[]], finalize=True, keep_on_top=True, no_titlebar=True,
                           alpha_channel=self._alpha)
        window.maximize()
        while True:
            window.read(timeout=100)
            if self.password:
                check = True
                for char in self.password:
                    if keyboard.is_pressed(char):
                        pass
                    else:
                        check = False
                        break
                if check or self.__poll():
                    break
            elif self.timer:
                self.timer -= 0.1
                if self.timer <= 0 or self.__poll():
                    break
        window.close()

    def __poll(self):
        for char in self.enforce:
            if keyboard.is_pressed(char):
                pass
            else:
                return False
        return True

    def now(self):
        """Freeze window now"""
        self.__freeze()

    def after(self, __t=None, key_seq=None):
        """Freeze window after time 't' or key_seq pressed"""
        if __t is not None:
            time.sleep(__t)
        elif key_seq is not None:
            while True:
                check = True
                for char in self.password:
                    if keyboard.is_pressed(char):
                        pass
                    else:
                        check = False
                        break
                if check:
                    break
        self.__freeze()


class MultiInstances:
    """Run your function 'n' no of times"""

    def __init__(self, target, no_of_threads, args=None, start_after=5):
        """
        Constructors
        :param target: target function, remember not use func() rather use func
        :param no_of_threads: number of threads to spawn
        :param args: function arguments
        :param start_after: start new thread after time 't'
        """
        self.threads = no_of_threads
        self.timer = start_after
        self.target = target
        self.args = args if args is not None else []

    def run(self):
        """Start multi-instances"""
        for t in range(self.threads):
            Thread(target=self.target, args=self.args).start()
            time.sleep(self.timer)

