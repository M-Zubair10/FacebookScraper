# -*- encoding: utf8 -*-

import csv
import logging
import re
from mytools.common.log import Handlers
from mytools.templates.webtools.imports import *
from mytools.templates.webtools.runner import Runner
from mytools.templates.webtools.scraper import ScraperBase

logging.basicConfig(format=Handlers().format, level=logging.INFO, handlers=[Handlers().colored_stream()])


class Scraper(ScraperBase):
    START_I = 1
    XQ = '(//*[@class="x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz"])[%s]'
    PAGE_LOAD_XP = '//*[@class="x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz"]'
    PAGE_LOAD_DELAY = 0

    HEADERS = ["URL", "Chapter", "Section", "Text"]
    OUTPUT_FP = 'FaceookPeopleScrapeFinal.csv'

    def get_email(self, html):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        email_addresses = re.findall(email_pattern, html)
        if email_addresses:
            ex_keywords = ['jelly', 'postmas', 'png', 'domain.com', 'user@']
            email_addresses = [x for x in email_addresses if not any(k in x for k in ex_keywords)]
            email_addresses = [x for x in email_addresses if len(x) < 45]
            email_addresses = list(set(email_addresses))
            return email_addresses[0] if email_addresses else None

    def get_row(self, xq, inputs):
        username = self.text(By.XPATH, xq)
        business_name = self.find_element(By.XPATH, '//b/..')
        if business_name is not None:
            business_name = self.text(By.XPATH, '//b/..')
            business_name = business_name.replace('Page · ', '')

        telephone_no = self.find_element(By.XPATH,
                                               '//*[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h" and contains(text(), "+")]')
        if telephone_no is not None:
            telephone_no = self.text(By.XPATH,
                                '//*[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h" and contains(text(), "+")]')

        pic = self.find_element(By.XPATH, '//*[@preserveAspectRatio="xMidYMid slice"]/../../..//*[@role="img"]//*[@preserveAspectRatio="xMidYMid slice"]')
        if pic is not None:
            pic = self.get_attribute(By.XPATH, '//*[@preserveAspectRatio="xMidYMid slice"]/../../..//*[@role="img"]//*[@preserveAspectRatio="xMidYMid slice"]', attr='xlink:href')
        email = self.get_email(self.driver.page_source)

        row = [inputs['url'], inputs['count'], username, business_name, telephone_no, email, pic]
        return row

    def work(self, inputs):
        if 'url' not in inputs:
            raise ValueError("Missing 'url' key in the inputs. One of the inputs fields must be 'url'.")
        if not inputs['url']:
            self.handle_row(list(inputs.values()))
            return True

        url = inputs['url']
        self.get(url)

        r = self.multiWait([(By.XPATH, '//*[@class="x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz"]'), (By.XPATH, '//*[text()="You must log in to continue."]')])
        if r == 1:
            print(f"Skipping {url} ...")
            return True

        if self.PAGE_LOAD_XP:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.PAGE_LOAD_XP)))
        if self.PAGE_LOAD_DELAY:
            self.delay.custom(self.PAGE_LOAD_DELAY)

        self.scrape(inputs)


def read_file():
    with open('final-links.csv', 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        return [x for x in reader]


if __name__ == '__main__':
    from driver_pool import DriverPool

    inputs_ = read_file()
    start = 84
    inputs_ = inputs_[start:]
    scraper_args = {'timeout': 60}
    runner = Runner(Scraper, inputs_, worker_params=scraper_args, debug=False, driver_pool_cls=DriverPool,
                    concurrency=5, launching_speed=10)
    runner.run_threaded()
