from .lambda_ import Lambda, MaxRetriesExceededException


class EmailValidator(Lambda):
    def __init__(self, email, retries=3):
        self.email = email
        payload = {'email': email}
        super().__init__(
            function_url='https://sdbhzaxb2vfgxvb763osi6ty3m0dvqbj.lambda-url.us-east-1.on.aws/',
            payload=payload,
            retries=retries
        )
        self._is_success = False

    def log_before(self):
        logger.info(f"[VALIDATOR] Email: {self.email} {f'| Retries: {self._count}' if self._count != 0 else ''}")

    def log_after(self):
        logger.info(f"[VALIDATOR] Response: {self._is_success} | Email: {self.email}")

    def request(self):
        for _ in range(self.retries):
            r = self._request()
            if r:
                return r
