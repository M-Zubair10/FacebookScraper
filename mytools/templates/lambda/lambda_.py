import requests
import logging

logger = logging.getLogger(__name__)


__all__ = ['MaxRetriesExceededException', 'Lambda']


class MaxRetriesExceededException(Exception):
    pass


class Lambda:
    def __init__(self, function_url, payload, retries=3):
        self.function_url = function_url
        self.payload = payload
        self.retries = retries
        self._count = 0

    def log_before(self):
        logger.info(f"[LAMBDA] Function Requested {f'| Retries: {self._count}' if self._count != 0 else ''}")

    def log_after(self):
        logger.info(f"[LAMBDA] Function response 200.")

    def _request(self):
        self.log_before()
        self._count += 1
        r = requests.get(self.function_url, json=self.payload)
        if r.text == 'Internal Server Error':
            if self._count == self.retries:
                raise MaxRetriesExceededException(f"Maximum no of retries {self.retries} exceeded.")
            return False
        self.log_after()
        return r

    def request(self):
        return self._request()
