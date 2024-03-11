import colorlog
import logging


class Handlers:
    def __init__(self, format='%(log_color)s[%(asctime)s] %(name)s:%(levelname)s %(message)s%(reset)s'):
        self.colors = {
        'DEBUG': 'cyan',
        'INFO': 'bold_white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
        self.fmt = format

    @property
    def format(self):
        return self.fmt

    def colored_stream(self):
        color_formatter = colorlog.ColoredFormatter(self.fmt, log_colors=self.colors)
        logger = colorlog.getLogger()
        handler = logging.StreamHandler()
        handler.setFormatter(color_formatter)
        return handler
