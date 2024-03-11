import os.path
import queue
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from mytools.templates.selenium_ import Selenium

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import threading
semaphore = threading.Semaphore(1)


class DriverPool:
    def __init__(self, pool_size=5, timeout=3600, launching_speed=5):
        self.pool_size = pool_size
        self.driver_pool = queue.Queue(maxsize=pool_size)
        self.timeout = timeout
        self.counter = 0
        self.ls = launching_speed
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
        try:
            # print(p)
            # p = "http://vip7ustj:cdv76rvd@tmobile.targetedproxies.com:30000"
            # p = 'http://dea82ef8f880897b:RNW78Fm5@185.130.105.109:10000'
            # p = 'http://43.159.18.198:22701'
            p = None
            extension_dir = f"extension/{uuid.uuid4()}"
            # data_dir = os.path.abspath(f'chrome-cache{self.counter+1}')
            # print(data_dir)
            data_dir = None

            sel = Selenium(
                "chrome",
                timeout=30,
                proxy_server=p,
                extension_dir=extension_dir,
                headless2=False,
                start=True,
                user_data_dir=data_dir,
                # extension_dir=f"extensions/{uuid.uuid4()}"
            )
            semaphore.acquire()
            self.login(sel, sel.driver, 'amandabeamon935@gmail.com', 'Felicit@beamon321')
            semaphore.release()
            return sel.driver
        except Exception as e:
            print(f"Error creating a WebDriver instance: {e}")
            return None
        finally:
            self.counter += 1
            print(f"{self.counter}. Driver launched.")

    def _is_login_page(self, driver) -> bool:
        try:
            driver.find_element(By.ID, 'email')
            return True
        except NoSuchElementException:
            return False

    def _is_home_page(self, driver) -> bool:
        try:
            driver.find_element(By.XPATH, '//*[@aria-label="Home"]')
            return True
        except NoSuchElementException:
            return False

    def login(self, sel, driver, email, password):
        driver.get("https://web.facebook.com/login.php/?_rdc=1&_rdr")

        if self._is_login_page(driver):
            print("Already logged in!")
            return True

        sel.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        email_elm = driver.find_element(By.ID, 'email')
        print("Typing email...")
        email_elm.send_keys(email)
        password_elm = driver.find_element(By.ID, 'pass')
        print("Typing password...")
        password_elm.send_keys(password)

        login_btn = driver.find_element(By.ID, 'loginbutton')
        print("Clicked login button")
        login_btn.click()

        time.sleep(10)  # Import time module if not already imported
        if not self._is_home_page(driver):
            print("Can't login, retrying...")
            return self.login(sel, driver, email, password)
        return True

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
