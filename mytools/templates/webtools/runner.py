import logging
from concurrent.futures import ThreadPoolExecutor
from mytools.templates.driver_pool import DriverPool
from queue import Queue
import time

from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


class Runner:
    """
    A class for managing and running threaded web crawlers and scrapers.

    Attributes:
    - worker_cls (class): The class of the web worker (crawler or scraper) to be instantiated.
    - input_list (list): The list of input data for the web worker to start its work.
      If a list of lists, each inner list is treated as input for a single worker thread.
      If a list of strings, each string is treated as the starting URL for a crawler.
    - worker_params (dict, optional): Additional parameters for the web worker class.
    - concurrency (int, optional): The number of threads to use. Default is 1.
    - launching_speed (int, optional): The speed at which to launch new threads. Default is 1.
    - debug (bool, optional): If True, run in debug mode. Default is False.
    - driver_pool_cls (class, optional): The class for managing the driver pool. Default is DriverPool.

    Methods:
    - run_threaded(): Run the web worker concurrently on multiple threads.

    Example:
    ```
    my_runner = Runner(worker_cls=Crawler, input_list=['https://example.com', 'https://example2.com'], concurrency=3, launching_speed=1, debug=False)
    my_runner.run_threaded()
    ```

    Note:
    - The behavior of the web worker depends on its implementation, whether it's a crawler or a scraper.
    """

    def __init__(self, worker_cls, input_list, worker_params=None, concurrency=1, launching_speed=1, debug=False,
                 driver_pool_cls=None):
        self.worker_cls = worker_cls
        self.input_list = input_list
        self.worker_params = worker_params or {}
        if 'start' in self.worker_params and self.worker_params['start'] is True:
            self.worker_params['start'] = False
            logger.warning("'start' parameter in worker_params set to False.")

        self.debug = debug
        self.concurrency = concurrency
        self.launching_speed = launching_speed
        self.executor = ThreadPoolExecutor(max_workers=self.concurrency * 2)
        self.driver_pool_cls = driver_pool_cls or DriverPool
        self.dpool = self.driver_pool_cls(pool_size=concurrency, launching_speed=launching_speed)
        self.input_queue = self._convert_to_queue(input_list)

    @staticmethod
    def _convert_to_queue(input_list):
        """
        Convert the input list to a queue.

        Parameters:
        - input_list (list): The list of input data.

        Returns:
        - Queue: A queue containing the input data.
        """
        input_queue = Queue()
        for item in input_list:
            input_queue.put(item)
        return input_queue

    def run_threaded(self):
        """
        Run the web worker concurrently on multiple threads.

        Example:
        ```
        my_runner = Runner(worker_cls=Crawler, input_list=['https://example.com', 'https://example2.com'], concurrency=3, launching_speed=1, debug=False)
        my_runner.run_threaded()
        ```

        Note:
        - The behavior of the web worker depends on its implementation, whether it's a crawler or a scraper.
        """
        start_time = time.time()
        if self.debug:
            self._run_single_thread()
        else:
            futures = [self.executor.submit(self._run_single_thread) for _ in range(self.concurrency)]
            [future.result() for future in futures]

        logger.info("All done. Cleaning up resources.")
        end_time = time.time()
        logger.info(f"Execution time: {end_time - start_time:.3f}s")
        self.dpool.close_all_drivers()
        self.executor.shutdown()

    def _run_single_thread(self):
        """
        Run the web worker on a single thread.

        Note:
        - This method is intended for internal use.
        """
        if self.input_queue.empty():
            return False

        start_time = time.time()
        instance = self.worker_cls(**self.worker_params)
        driver = self.dpool.get_driver()
        input_ = self.input_queue.get()

        try:
            instance.driver = driver
            instance.wait = WebDriverWait(driver, instance.timeout)
            instance.work(input_)
        except RecursionError:
            logger.error("RecursionError in _run_single_thread. Stopping further recursion.")
            return False
        except Exception as e:
            logger.error(f"Exception in _run_single_thread\nInputs: {input_}\n{e}")
            if self.debug:
                raise e
        finally:
            self.dpool.release_driver(driver)

        end_time = time.time()
        logger.info(f"Job finished. Execution time: {end_time - start_time:.2f}s")
        return self._run_single_thread()
