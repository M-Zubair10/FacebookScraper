import csv
import os
from collections import Counter

links = []
for fn in os.listdir():
    if '.txt' not in fn:
        continue

    if any(x in fn for x in ('final-links', 'merge')):
        print('skipping ...')
        continue

    with open(fn, 'r', encoding='utf8') as f:
        urls = f.readlines()
        links.extend(urls)

links = [x[:x.find('?')] for x in links]
counter = Counter(links)
print(len(set(links)))
print(len(links))

with open('final-links.txt', 'w', encoding='utf8') as f:
    f.writelines([x + '\n' for x in list(set(links)) if x])

with open('final-links.csv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['url', 'count'])
    writer.writerows([(x, v) for x, v in counter.items()])

with open('merge.txt', 'w', encoding='utf8') as f:
    f.writelines([x + '\n' for x in links if x])
