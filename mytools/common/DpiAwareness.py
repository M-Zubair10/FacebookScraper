import ctypes
import inspect
import tkinter
import sys
import copy


def aware():
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


def DPI():
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = tkinter.Tk()
    dpi = ctypes.windll.user32.GetDpiForWindow(root.winfo_id())
    root.destroy()
    return dpi


def scaling():
    return DPI() / 96


def true_point(point):
    """
    Return coordinates[x, y] according to exact dpi value
    :param point: coordinates to be corrected
    :type point: tuple[x, y] or list[x, y]
    :return: True points
    """
    return int(point[0] / scaling()), int(point[1] / scaling())


def chrome_distance():
    return true_point((0, 152))[1]

