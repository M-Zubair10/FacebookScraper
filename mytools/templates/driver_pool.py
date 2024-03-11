import queue
import uuid
from concurrent.futures import ThreadPoolExecutor

from mytools.templates.selenium_ import Selenium


class DriverPool:
    def __init__(self, pool_size=5, timeout=3600, launching_speed=5, proxies=[]):
        self.pool_size = pool_size
        self.driver_pool = queue.Queue(maxsize=pool_size)
        self.timeout = timeout
        self.counter = 0
        self.ls = launching_speed
        self.proxies = proxies
        self._create_drivers()

    def _create_drivers(self):
        with ThreadPoolExecutor(max_workers=self.ls) as executor:
            futures = [executor.submit(self._create_driver_and_add_to_queue) for _ in range(self.pool_size)]
            [future.result() for future in futures]

    def _create_driver_and_add_to_queue(self):
        driver = self._create_driver()
        if driver:
            self.driver_pool.put(driver)
        return 0

    def _create_driver(self):
        if len(self.proxies) > self.counter:
            p = self.proxies[self.counter]
        else:
            p = None
        extension_dir = f"extension/{uuid.uuid4()}"

        try:
            return Selenium(
                "chrome",
                timeout=300,
                proxy_server=p,
                extension_dir=extension_dir,
                headless2=False,
                load_full=False,
                start=True,
                # extension_dir=f"extensions/{uuid.uuid4()}"
            ).driver
        except Exception as e:
            print(f"Error creating a WebDriver instance: {e}")
            return None
        finally:
            self.counter += 1
            print(f"{self.counter}. Driver launched.")

    def refresh_driver(self, driver):
        driver.quit()
        d = self._create_driver()
        self.driver_pool.put(d)

    def get_driver(self):
        try:
            driver = self.driver_pool.get(timeout=self.timeout)
            return driver
        except queue.Empty:
            raise TimeoutError("Driver pool is empty. No available drivers.")

    def release_driver(self, driver):
        if driver:
            try:
                self.driver_pool.put(driver)
            except queue.Full:
                print("Driver pool is full. Cannot release the driver.")

    def close_all_drivers(self):
        while not self.driver_pool.empty():
            driver = self.driver_pool.get()
            driver.quit()
            print("Closed a driver.")
