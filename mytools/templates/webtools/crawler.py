import csv
import logging
import os
import threading
from mytools.templates.selenium_ import Selenium, EC, By, WebDriverWait, TimeoutException

logger = logging.getLogger(__name__)
wlock = threading.Lock()
ROW_COUNTER = 0


class CrawlerBase(Selenium):
    """
    Base class for web crawlers.

    Attributes:
    - START_I (int): Starting index from which to crawl containers. Increase to skip first containers.
    - XQ (str): XPath expression template for container elements.
    - PAGE_LOAD_XP (str): XPath expression for identifying elements indicating page load completion.
    - COUNTER (int): Counter to keep track of processed rows.
    - FOCUS_ELEMENT (bool): If True, focus on the found container element.
    - MAX_RECORDS (int): Maximum number of records to process. Set to None for no limit.

    Methods:
    - get_row(xq, url): Abstract method to retrieve data from the current container.
    - handle_row(row): Abstract method to handle the processed row.
    - handle_container(xq, url): Abstract method to handle the container.
    - crawl(url): Main method to iterate through containers, retrieve rows, and handle them.
    - on_failed_callback(xq): Callback method invoked when a container is not found. Scrolls and retries.

    Example usage:
    ```
    class MyCrawler(CrawlerBase):
        START_I = 1
        XQ = '//div[@class="container"][%d]'
        PAGE_LOAD_XP = '//div[@class="page-loaded-indicator"]'

        def get_row(self, xq, url):
            # Implement logic to retrieve row data from the current container
            pass

        def handle_container(self, xq, url):
            # Implement logic to handle the processed row
            pass
    ```

    Note: This class is meant to be subclassed, and the `get_row` and `handle_container` methods need to be implemented in the subclasses.
    """
    COUNTER = 0
    HEADERS = []
    OUTPUT_FP = 'crawler-output.csv'

    START_I = 1
    XQ = ''
    PAGE_LOAD_XP = ''
    PAGE_LOAD_DELAY = 0
    FOCUS_ELEMENT = True
    MAX_RECORDS = None

    def get_row(self, xq, url):
        """
        Abstract method to retrieve data from the current row.

        Parameters:
        - url (str): The URL of the page being crawled.
        - xq (str): The current row

        Returns:
        - Any: The data extracted from the current container.
        """
        pass

    def handle_container(self, xq, url):
        """
        Abstract method to retrieve data from the current container.

        Parameters:
        - url (str): The URL of the page being crawled.
        - xq (str): The current container

        Returns:
        - Any: The data extracted from the current container.
        """
        row = self.get_row(xq, url)
        logger.info(f"Rows populated: {self.COUNTER}. Processing row #{self.COUNTER}")
        self.COUNTER += 1
        self.handle_row(row)

    def handle_row(self, row, header=None):
        """
        Abstract method to handle the processed row.

        Parameters:
        - row (Any): The data from the processed row.
        """
        global ROW_COUNTER

        header = header or self.HEADERS
        with wlock:
            with open(self.OUTPUT_FP, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                if header is not None:
                    if os.path.getsize(self.OUTPUT_FP) == 0:
                        writer.writerow(header)
                writer.writerow(row)
                logger.critical(f"Writing Row {ROW_COUNTER}. to {self.OUTPUT_FP}")
                ROW_COUNTER += 1

    def crawl(self, url):
        """
        Main method to iterate through containers, retrieve rows, and handle them.

        Parameters:
        - url (str): The URL of the page being crawled.
        """
        if self.XQ[0] != '(':
            self.XQ = f'({self.XQ})[%s]'

        max_records = self.MAX_RECORDS or -1
        i = self.START_I
        while True:
            xq = self.XQ % i
            container = self.find_element(By.XPATH, xq)
            if container is None:
                logger.info("Container not found. Returning on_failed_callback.")
                if not self.on_failed_callback(xq):
                    break
                i = self.START_I
                continue

            if self.FOCUS_ELEMENT:
                logger.debug("Focusing on element.")
                self.scrollIntoView(container)

            logger.info("Container found. Retrieving row.")
            self.handle_container(xq, url)

            i += 1
            if self.MAX_RECORDS == i:
                logger.info("Max records limit reached.")
                break

    def infinite_scroll(self, xq):
        self.scrollBy(0, 1000)
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xq)))
        except TimeoutException:
            return False
        else:
            return True

    def on_failed_callback(self, xq):
        """
        Callback method invoked when a container is not found. Scrolls and retries.

        Parameters:
        - xq (str): The XPath expression for the container.

        Returns:
        - bool: True if retrying is successful, False otherwise.
        """
        pass

    def work(self, url):
        """
        Method to initiate the crawling process.

        Parameters:
        - url (str): The URL of the page to crawl.
        """
        self.get(url)
        if self.PAGE_LOAD_XP:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.PAGE_LOAD_XP)))
        if self.PAGE_LOAD_DELAY:
            self.delay.custom(self.PAGE_LOAD_DELAY)
        self.crawl(url)
