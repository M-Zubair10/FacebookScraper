import sys
import csv


def find_missing(csv1path, csv2path, index=0, output_fn='missing.csv'):
    """
    Get the csv containing all the rows of csv1 which are not included in csv2
    :param csv1path: path to csv1
    :param csv2path: path to csv2
    :param index: common element to check in csv2 like url, id or name etc
    :param output_fn: name of output file. Default missing.csv
    :return: None
    """
    
    with open(csv1path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        h1 = next(reader)
        rows1 = [x for x in reader]

    with open(csv2path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        h2 = next(reader)
        rows2 = [x for x in reader]
        common = [x[index] for x in rows2]

    missing = [x for x in rows1 if x[index] not in common]
    
    print(len(missing))
    with open('missing.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(h1)
        writer.writerows(missing)

