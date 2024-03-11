import time
import numpy as np
try:
    import win32api
    from mytools.common.DpiAwareness import aware
    aware()
except:
    pass


class Mouse:

    def __init__(self):
        self.buttons = {'VK_Left': 0x01, 'VK_Right': 0x02, 'VK_Middle': 0x04, }

    def is_pressed(self, _button: str = None):
        if _button is not None:
            for x in self.buttons.keys():
                if _button.lower() in x.lower():
                    if win32api.GetKeyState(self.buttons[x]) < 0:
                        return True
        else:
            for b in self.buttons.keys():
                if win32api.GetKeyState(self.buttons[b]) < 0:
                    return True

    def not_pressed(self, _button):
        for x in self.buttons.keys():
            if _button.lower() in x.lower():
                if win32api.GetKeyState(self.buttons[x]) >= 0:
                    return True

    def whichPressed(self):
        while True:
            for x in self.buttons.keys():
                if win32api.GetKeyState(self.buttons[x]) < 0:
                    return x.removeprefix("VK_").lower().removeprefix("oem_")

    def get_location(self):
        return win32api.GetCursorPos()


def wind_mouse(start_x, start_y, dst_x, dst_y, G_0=9, W_0=3, M_0=15, D_0=12):
    """
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational force
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    """
    MOUSE_MOVEMENTS = []
    sqrt3 = np.sqrt(3)
    sqrt5 = np.sqrt(5)
    current_x, current_y = start_x, start_y
    v_x = v_y = W_x = W_y = 0
    while (dist := np.hypot(dst_x - start_x, dst_y - start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
            W_y = W_y / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random() * 3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0 * (dst_x - start_x) / dist
        v_y += W_y + G_0 * (dst_y - start_y) / dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0 / 2 + np.random.random() * M_0 / 2
            v_x = (v_x / v_mag) * v_clip
            v_y = (v_y / v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            MOUSE_MOVEMENTS.append([current_x := move_x, current_y := move_y])
    return MOUSE_MOVEMENTS


if __name__ == '__main__':
    while True:
        print(Mouse().get_location())