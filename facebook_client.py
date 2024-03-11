import logging
import time
import uuid
from mytools.templates.selenium_ import *

import yaml

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

with open("secret.yaml") as f:
    secret = yaml.safe_load(f)
email = secret['email']
password = secret['password']


class Facebook(Selenium):
    REGISTER_URL = "https://web.facebook.com/login.php/?_rdc=1&_rdr"
    LINKS = []

    def write(self, fn):
        with open(fn, 'w', encoding='utf8') as file:
            file.write('\n'.join(list(set(self.LINKS))))

    def _is_login_page(self) -> bool:
        return self.find_element(By.ID, 'email') is not None

    def _is_home_page(self) -> bool:
        return self.find_element(By.XPATH, '//*[@aria-label="Home"]') is not None

    def login(self):
        self.get(self.REGISTER_URL)

        response_id = self.multiWait([self._is_login_page, self._is_home_page])
        if response_id == 1:
            logger.info("Already logged in!")
            return True

        email_elm = self.driver.find_element(By.ID, 'email')
        logger.info("Typing email...")
        email_elm.send_keys(email)
        password_elm = self.driver.find_element(By.ID, 'pass')
        logger.info("Typing password...")
        password_elm.send_keys(password)

        login_btn = self.driver.find_element(By.ID, 'loginbutton')
        logger.info("Clicked login button")
        self.click_js(login_btn)

        self.delay.custom(5)
        response_id = self.multiWait([self._is_login_page, self._is_home_page])
        if response_id == 0:
            logger.info("Can't login, retrying...")
            return self.login()

    def get_links(self):
        if self.find_element(By.XPATH, '//*[@role="dialog"]//a[contains(@href, "comment")]/div/..') is not None:  # For comments
            xq = '(//*[@role="dialog"]//a[contains(@href, "comment")]/div/..)[%s]'

            i = 0
            links = []
            while True:
                i += 1
                e = self.find_element(By.XPATH, xq % i)
                if e is None:
                    scroll_e = self.find_element(By.XPATH,
                                                 '//*[@class="xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r'
                                                 ' x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg'
                                                 ' xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1iyjqo2 xy5w88m"]')
                    if scroll_e is None:
                        self.click_js((By.XPATH, '(//*[@aria-label="Close"])[last()]'))
                        return links
                    self.scrollBy(0, 1000, element=scroll_e, method='direct')
                    time.sleep(3)
                    if e is None:
                        self.click_js((By.XPATH, '(//*[@aria-label="Close"])[last()]'))
                        return links

                self.scrollIntoView(e)
                link = self.href(By.XPATH, xq % i)
                links.append(link)
        else:
            xq = '(//*[@class="x78zum5 xdt5ytf x1iyjqo2 x7ywyr2"]//*[@class="x1rg5ohu"]/a)[%s]'

            i = 0
            links = []
            while True:
                i += 1
                e = self.find_element(By.XPATH, xq % i)
                if e is None:
                    scroll_e = self.find_element(By.XPATH,
                                                 '//*[@class="xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf'
                                                 ' x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si'
                                                 ' xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f'
                                                 ' x1e4zzel x1tbbn4q x1y1aw1k x4uap5 xwib8y2 xkhd6sd"]')
                    if scroll_e is None:
                        self.click_js((By.XPATH, '(//*[@aria-label="Close"])[last()]'))
                        return links
                    self.scrollBy(0, 1000, element=scroll_e, method='direct')
                    time.sleep(3)
                    if e is None:
                        self.click_js((By.XPATH, '(//*[@aria-label="Close"])[last()]'))
                        return links

                self.scrollIntoView(e)
                link = self.href(By.XPATH, xq % i)
                links.append(link)

    def _scrape(self, limit, fn):
        xq = '(//*[@class="x1n2onr6 x1ja2u2z"])[%s]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, xq % 1)))

        i = 0
        while True:
            i += 1
            if i == limit:
                break

            e = self.find_element(By.XPATH, f'{xq % i}')
            if e is None:
                self.scrollBy(0, 10000, method='direct')
                time.sleep(3)
                if e is None:
                    self.scrollBy(0, -1000, method='direct')
                    time.sleep(1)
                    self.scrollBy(0, 10000, method='direct')
                    time.sleep(3)
                    if e is None:
                        return True

            self.scrollIntoView(e)
            time.sleep(1)

            reaction = self.find_element(By.XPATH, f'{xq % i}//*[contains(@aria-label, "Like:")]')
            if reaction is not None:
                self.click_js((By.XPATH, f'{xq % i}//*[contains(@aria-label, "Like")]'))
                time.sleep(2)
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="x78zum5 xdt5ytf x1iyjqo2 x7ywyr2"]')))
                try:
                    links = self.get_links()
                except:
                    continue
                else:
                    self.LINKS.extend(links)
                finally:
                    self.write(fn)

            comments_and_shares = self.find_elements(By.XPATH,
                                                     f'{xq % i}//*[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn"]/i')
            if comments_and_shares:
                if len(comments_and_shares) > 1:
                    comments = self.find_element(By.XPATH,
                                                 f'({xq % i}//*[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn"]/i)[1]')
                    self.click_js(comments)
                    time.sleep(2)
                    try:
                        links = self.get_links()
                    except:
                        continue
                    else:
                        self.LINKS.extend(links)
                    finally:
                        self.write(fn)

                    shares = self.find_element(By.XPATH,
                                               f'({xq % i}//*[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn"]/i)[2]')
                    self.click_js(shares)
                    time.sleep(2)
                    try:
                        links = self.get_links()
                    except:
                        continue
                    else:
                        self.LINKS.extend(links)
                    finally:
                        self.write(fn)

                else:
                    shares = self.find_element(By.XPATH,
                                               f'({xq % i}//*[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli xg83lxy x1h0ha7o x10b6aqq x1yrsyyn"]/i)[1]')
                    self.click_js(shares)
                    time.sleep(2)
                    try:
                        links = self.get_links()
                    except:
                        continue
                    else:
                        self.LINKS.extend(links)
                    finally:
                        self.write(fn)

    def scrape(self, url, years):
        for y in range(years):
            self.get(url)

            e = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Filters"]')))
            self.scrollIntoView(e)
            time.sleep(1)
            self.click_js((By.XPATH, '//*[text()="Filters"]'))

            e = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Year"]')))
            self.scrollIntoView(e)
            time.sleep(1)
            self.click_js((By.XPATH, '//*[text()="Year"]'))

            e = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[contains(@id, ":__{y + 1}")]')))
            self.scrollIntoView(e)
            time.sleep(1)
            self.click_js((By.XPATH, f'//*[contains(@id, ":__{y + 1}")]'))

            self.click_js((By.XPATH, '(//*[text()="Done"])[last()]'))
            time.sleep(5)
            self._scrape()

    def scrape_wfilter(self, url, y):
        year, month = y
        logger.info(f"Scraping {year}, {month}")
        self.get(url)

        e = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Filters"]')))
        self.scrollIntoView(e)
        time.sleep(1)
        self.click_js((By.XPATH, '//*[text()="Filters"]'))

        e = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Year"]')))
        self.scrollIntoView(e)
        time.sleep(1)
        self.click_js((By.XPATH, '//*[text()="Year"]'))

        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[text()="{year}"]')))
        time.sleep(1)
        self.click_js((By.XPATH, f'//*[text()="{year}"]'))

        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[text()="Month"]')))
        self.click_js((By.XPATH, '//*[text()="Month"]'))

        self.wait.until(EC.presence_of_element_located((By.XPATH, f'//*[text()="{month}"]')))
        time.sleep(1)
        self.click_js((By.XPATH, f'//*[text()="{month}"]'))
        time.sleep(1)

        self.click_js((By.XPATH, '(//*[text()="Done"])[last()]'))
        time.sleep(5)

        limit = 50
        fn = f"links-{uuid.uuid4()}.txt"
        print(fn)
        self._scrape(limit, fn)
        print(f"{year}, {month} done!")

