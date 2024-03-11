import queue
import threading
from concurrent.futures import ThreadPoolExecutor

from facebook_client import Facebook

PAGE_URL = "https://web.facebook.com/ultracryorecovery?_rdc=1&_rdr"
YEARS = 5
FILTERS = [
    (2024, 'January'),
    (2024, 'February'),
    # (2024, 'March'),
    # (2024, 'April'),
    # (2024, 'May'),
    # (2024, 'June'),
    # (2024, 'July'),
    # (2024, 'August'),
    # (2024, 'September'),
    # (2024, 'October'),
    # (2024, 'November'),
    # (2024, 'December'),

    # (2023, 'January'),
    # (2023, 'February'),
    # (2023, 'March'),
    # (2023, 'April'),
    # (2023, 'May'),
    # (2023, 'June'),
    # (2023, 'July'),
    # (2023, 'August'),
    # (2023, 'September'),
    # (2023, 'October'),
    # (2023, 'November'),
    # (2023, 'December'),

    # (2022, 'January'),
    # (2022, 'February'),
    # (2022, 'March'),
    # (2022, 'April'),
    # (2022, 'May'),
    # (2022, 'June'),
    # (2022, 'July'),
    # (2022, 'August'),
    # (2022, 'September'),
    # (2022, 'October'),
    # (2022, 'November'),
    # (2022, 'December'),
    #
    # (2021, 'January'),
    # (2021, 'February'),
    # (2021, 'March'),
    # (2021, 'April'),
    # (2021, 'May'),
    # (2021, 'June'),
    # (2021, 'July'),
    # (2021, 'August'),
    # (2021, 'September'),
    # (2021, 'October'),
    # (2021, 'November'),
    # (2021, 'December'),
    #
    # (2020, 'January'),
    # (2020, 'February'),
    # (2020, 'March'),
    # (2020, 'April'),
    # (2020, 'May'),
    # (2020, 'June'),
    # (2020, 'July'),
    # (2020, 'August'),
    # (2020, 'September'),
    # (2020, 'October'),
    # (2020, 'November'),
    # (2020, 'December')
]

semaphore = threading.Semaphore(1)


def main():
    if q.empty():
        return True

    y = q.get()

    facebook = Facebook("chrome", start=True, timeout=90)
    semaphore.acquire()
    facebook.login()
    semaphore.release()
    facebook.scrape_wfilter(PAGE_URL, y)
    facebook.quit()

    return main()


if __name__ == '__main__':
    q = queue.Queue()
    for f in FILTERS:
        q.put(f)

    concurrency = 1
    with ThreadPoolExecutor(max_workers=concurrency) as exe:
        for _ in range(concurrency):
            exe.submit(main)
