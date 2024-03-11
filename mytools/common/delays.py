import logging
import random
import sys
import time

from mytools.common.functools import get_func_name

from multiprocessing.context import TimeoutError
from multiprocessing.pool import ThreadPool
import concurrent.futures
import functools
logger = logging.getLogger(__name__)

if sys.platform == 'win32':
    import win32api


class TimeoutException(Exception):
    pass


class Delay:

    def __init__(self):
        self.keycodes = {'VK_BACK': 0x08, 'VK_TAB': 0x09, 'VK_CLEAR': 0x0C, 'VK_RETURN': 0x0D, 'VK_SHIFT': 0x10,
                         'VK_CONTROL': 0x11,
                         'VK_ALT': 0x12, 'VK_PAUSE': 0x13, 'VK_CAPITAL': 0x14, 'VK_KANA': 0x15, 'VK_HANGUEL': 0x15,
                         'VK_HANGUL': 0x15,
                         'VK_IME_ON': 0x16, 'VK_JUNJA': 0x17, 'VK_FINAL': 0x18, 'VK_HANJA': 0x19, 'VK_KANJI': 0x19,
                         'VK_IME_OFF': 0x1A,
                         'VK_ESCAPE': 0x1B, 'VK_CONVERT': 0x1C, 'VK_NONCONVERT': 0x1D, 'VK_ACCEPT': 0x1E,
                         'VK_MODECHANGE': 0x1F,
                         'VK_SPACE': 0x20, 'VK_PRIOR': 0x21, 'VK_NEXT': 0x22, 'VK_END': 0x23, 'VK_HOME': 0x24,
                         'VK_LEFT': 0x25,
                         'VK_UP': 0x26, 'VK_RIGHT': 0x27, 'VK_DOWN': 0x28, 'VK_SELECT': 0x29, 'VK_PRINT': 0x2A,
                         'VK_EXECUTE': 0x2B,
                         'VK_SNAPSHOT': 0x2C, 'VK_INSERT': 0x2D, 'VK_DELETE': 0x2E, 'VK_HELP': 0x2F, 'VK_0': 0x30,
                         'VK_1': 0x31,
                         'VK_2': 0x32, 'VK_3': 0x33, 'VK_4': 0x34, 'VK_5': 0x35, 'VK_6': 0x36, 'VK_7': 0x37,
                         'VK_8': 0x38,
                         'VK_9': 0x39,
                         'VK_A': 0x41, 'VK_B': 0x42, 'VK_C': 0x43, 'VK_D': 0x44, 'VK_E': 0x45, 'VK_F': 0x46,
                         'VK_G': 0x47,
                         'VK_H': 0x48,
                         'VK_I': 0x49, 'VK_J': 0x4A, 'VK_K': 0x4B, 'VK_L': 0x4C, 'VK_M': 0x4D, 'VK_N': 0x4E,
                         'VK_O': 0x4F,
                         'VK_P': 0x50,
                         'VK_Q': 0x51, 'VK_R': 0x52, 'VK_S': 0x53, 'VK_T': 0x54, 'VK_U': 0x55, 'VK_V': 0x56,
                         'VK_W': 0x57,
                         'VK_X': 0x58,
                         'VK_Y': 0x59, 'VK_Z': 0x5A, 'VK_LWIN': 0x5B, 'VK_RWIN': 0x5C, 'VK_APPS': 0x5D,
                         'VK_SLEEP': 0x5F,
                         'VK_NUM0': 0x60, 'VK_NUM1': 0x61, 'VK_NUM2': 0x62, 'VK_NUM3': 0x63, 'VK_NUM4': 0x64,
                         'VK_NUM5': 0x65, 'VK_NUM6': 0x66, 'VK_NUM7': 0x67, 'VK_NUM8': 0x68, 'VK_NUM9': 0x69,
                         'VK_MULTIPLY': 0x6A, 'VK_ADD': 0x6B, 'VK_SEPARATOR': 0x6C, 'VK_SUBTRACT': 0x6D,
                         'VK_DECIMAL': 0x6E,
                         'VK_DIVIDE': 0x6F, 'VK_F1': 0x70, 'VK_F2': 0x71, 'VK_F3': 0x72, 'VK_F4': 0x73, 'VK_F5': 0x74,
                         'VK_F6': 0x75,
                         'VK_F7': 0x76, 'VK_F8': 0x77, 'VK_F9': 0x78, 'VK_F10': 0x79, 'VK_F11': 0x7A, 'VK_F12': 0x7B,
                         'VK_F13': 0x7C,
                         'VK_F14': 0x7D, 'VK_F15': 0x7E, 'VK_F16': 0x7F, 'VK_F17': 0x80, 'VK_F18': 0x81, 'VK_F19': 0x82,
                         'VK_F20': 0x83,
                         'VK_F21': 0x84, 'VK_F22': 0x85, 'VK_F23': 0x86, 'VK_F24': 0x87, 'VK_NUMLOCK': 0x90,
                         'VK_SCROLL': 0x91,
                         'VK_LSHIFT': 0xA0, 'VK_RSHIFT': 0xA1, 'VK_LCONTROL': 0xA2, 'VK_RCONTROL': 0xA3,
                         'VK_LALT': 0xA4,
                         'VK_RALT': 0xA5, 'VK_BROWSER_BACK': 0xA6, 'VK_BROWSER_FORWARD': 0xA7,
                         'VK_BROWSER_REFRESH': 0xA8,
                         'VK_BROWSER_STOP': 0xA9, 'VK_BROWSER_SEARCH': 0xAA, 'VK_BROWSER_FAVORITES': 0xAB,
                         'VK_BROWSER_HOME': 0xAC,
                         'VK_VOLUME_MUTE': 0xAD, 'VK_VOLUME_DOWN': 0xAE, 'VK_VOLUME_UP': 0xAF,
                         'VK_MEDIA_NEXT_TRACK': 0xB0,
                         'VK_MEDIA_PREV_TRACK': 0xB1, 'VK_MEDIA_STOP': 0xB2, 'VK_MEDIA_PLAY_PAUSE': 0xB3,
                         'VK_LAUNCH_MAIL': 0xB4,
                         'VK_LAUNCH_MEDIA_SELECT': 0xB5, 'VK_LAUNCH_APP1': 0xB6, 'VK_LAUNCH_APP2': 0xB7,
                         'VK_OEM_1': 0xBA,
                         'VK_OEM_PLUS': 0xBB, 'VK_OEM_COMMA': 0xBC, 'VK_OEM_MINUS': 0xBD, 'VK_OEM_PERIOD': 0xBE,
                         'VK_OEM_2': 0xBF,
                         'VK_OEM_3': 0xC0, 'VK_OEM_4': 0xDB, 'VK_OEM_5': 0xDC, 'VK_OEM_6': 0xDD, 'VK_OEM_7': 0xDE,
                         'VK_OEM_8': 0xDF,
                         '0xE1': 0xE1, 'VK_OEM_102': 0xE2, 'VK_PROCESSKEY': 0xE5, '0xE6': 0xE6, 'VK_ATTN': 0xF6,
                         'VK_CRSEL': 0xF7,
                         'VK_EXSEL': 0xF8, 'VK_EREOF': 0xF9, 'VK_PLAY': 0xFA, 'VK_ZOOM': 0xFB, 'VK_NONAME': 0xFC,
                         'VK_PA1': 0xFD,
                         'VK_OEM_CLEAR': 0xFE, }
        self.very_small_delay = self.one100_one1000
        self.small_delay = self.one10_one
        self.medium_delay = self.one_3
        self.long_delay = self.five_10
        self.very_long_delay = self.ten_15

    @staticmethod
    def _sleep(secs):
        logger.info(f"[Delay] Sleeping for {secs} seconds")
        time.sleep(secs)

    def one100_one1000(self):
        """Sleep Program for Random Between 0.001 - 0.01 seconds"""
        self._sleep(random.randint(1, 10)/1000)

    def random_delay(self):
        """Sleep program for either very small delay or small delay or medium delay"""
        x = random.choice([1, 2, 3])
        self.very_small_delay() if x == 1 else self.small_delay() if x == 2 else self.medium_delay()

    def one10_one(self):
        """Sleep Program for Random Between 0.1 - 1 seconds"""
        self._sleep(random.randint(100, 1000)/1000)

    def one_3(self):
        """Sleep Program for Random Between 1 - 3 seconds"""
        self._sleep(random.randint(1000, 3000)/1000)

    def five_10(self):
        """Sleep Program for Random Between 5 - 10 seconds"""
        self._sleep(random.randint(5000, 1000)/1000)

    def ten_15(self):
        """Sleep Program for Random Between 10 - 15 seconds"""
        self._sleep(random.randint(10000, 15000)/1000)

    def btw(self, _min, _max):
        """Sleep Program for Random Between min - max seconds"""
        self._sleep(random.randint(_min*100, _max*100) / 100)

    def custom(self, secs):
        """Sleep program for time 't'"""
        self._sleep(secs)

    def escape_pressed(self):
        """Sleep until escape pressed"""
        logger.info("[Delay] Sleeping until `Escape` pressed")
        while True:
            if win32api.GetKeyState(self.keycodes["VK_ESCAPE"]) < 0:
                break
            time.sleep(0.01)

    def key_pressed(self, key=None):
        """Sleep until key pressed, If key is None it waits for any key to be pressed"""

        logger.info(f"[Delay] Sleeping until `{'Any-Key' if key is None else key}` pressed")
        sorted_keys = list(self.keycodes.keys())
        sorted_keys.sort(key=len)
        if key is not None:
            for x in sorted_keys:
                if key.lower() in x.lower():
                    key = x
                    break
        while True:
            if key is None:
                for key_value in self.keycodes.values():
                    if win32api.GetKeyState(key_value) < 0:
                        return
            else:
                if win32api.GetKeyState(self.keycodes[key]) < 0:
                    return
            time.sleep(0.1)


def wait_till_true(func, timeout=None):
    """
    Wait till function returns true
    :param func: function to be called
    :param timeout: maximium time allowed to func call
    :return: None
    """

    logger.debug(f"Wait till {get_func_name(func)} returns true in {timeout if timeout is not None else 'infinite'} seconds")
    if timeout is None:
        while not func():
            time.sleep(1)
    else:
        for i in range(timeout):
            if func():
                return True
            else:
                time.sleep(1)
        return False


def wait_till_false(func, timeout=None):
    """
    Wait till function returns true
    :param func: function to be called
    :param timeout: maximium time allowed to func call
    :return: None
    """

    logger.debug(f"Wait till {get_func_name(func)} returns false in {timeout if timeout is not None else 'infinite'} seconds")
    if timeout is None:
        while func():
            time.sleep(1)
    else:
        for i in range(timeout):
            if not func():
                return True
            else:
                time.sleep(1)
        return False


def show_timer(n, show_every_sec=1):
    """
    Wait n seconds also show live timer
    :param n: float time in seconds
    :param show_every_sec: show every n seconds
    :return: None
    """

    logger.info(f'Timer started: {n} seconds -> {n/60} minutes -> {n/(60*60)} hours')
    for i in range(round(n / show_every_sec)):
        logger.info(f'Time left: {n - i*show_every_sec} seconds -> {round((n-(i*show_every_sec))/60, 3)} minutes')
        time.sleep(show_every_sec)


def timeout_multiprocessing_func(func, time_: float, args: tuple or list = (), kwargs: dict = {}, default_resp=False):
    """
    Runs a function with time limit
    :param func: The function to run
    :param args: The functions args, given as tuple or list
    :param kwargs: The functions keywords, given as dict
    :param time_: The time limit in seconds
    :return: True if the function ended successfully. False if it was terminated.
    """

    logger.critical("This is not implemented correctly, this leak memory, you should use threading.event flage")
    pool = ThreadPool(processes=1)
    res = pool.apply_async(func, args=args, kwds=kwargs)
    try:
        return res.get(time_)
    except TimeoutError as e:
        return default_resp


def timeout_multiprocessing_decorator(time_: float):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.critical("This is not implemented correctly, this leak memory, you should use threading.event flage")
            pool = ThreadPool(processes=1)
            res = pool.apply_async(func, args=args, kwds=kwargs)
            try:
                return res.get(time_)
            except TimeoutError as e:
                raise TimeoutException
        return wrapper
    return decorator


def timeout_concurrent_func(func, args=(), kwargs={}, timeout_duration=1, default=None):
    """Run func with the given timeout. If func didn't finish running
    within the timeout, return default.
    """

    logger.critical("This is not implemented correctly, this leak memory, you should use threading.event flage")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(func, *args, **kwargs)
        try:
            return future.result(timeout=timeout_duration)
        except concurrent.futures.TimeoutError:
            return default


def timeout_concurrent_decorator(timeout_duration):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.critical("This is not implemented correctly, this leak memory, you should use threading.event flage")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=timeout_duration)
                except concurrent.futures.TimeoutError:
                    raise TimeoutException("Function execution exceeded the specified timeout")
        return wrapper
    return decorator


def handle_exception_func(func, ignore_exceptions: tuple or Exception = Exception, args=(), kwds={}, default=None):
    logger.info(f"[Handle-Exception-Func] Ignoring {ignore_exceptions}")
    try:
        return func(*args, **kwds)
    except ignore_exceptions as e:
        logger.info(f"[Handle-Exception-Func] Exception occur return {default}")
        return e if default == 'exception' else default


def handle_exception_decorator(ignore_exceptions: tuple or Exception = Exception, default='exception'):
    def decorating(func):
        @functools.wraps(func)
        def wrapper(*args, **kwds):
            return handle_exception_func(func, ignore_exceptions, args, kwds, default)
        return wrapper
    return decorating


timeout_after_decorator = timeout_multiprocessing_decorator
