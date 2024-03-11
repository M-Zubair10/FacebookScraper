import csv
import os
import shutil
import configparser


class INI:
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        self.config = configparser.RawConfigParser()
        self.config.read(self.filename)
        self.exist = None
    
    def create(self):
        with open(self.filename, "w+") as file: pass
        return self
    
    def read(self, header="*", section="*"):
        reader = {}
        if header == "*":
            headers = list(self.config)
        if section == "*":
            if isinstance(headers, list):
                for h in headers:
                    reader[h] = dict(self.config[h])
            else:
                reader[header] = dict(self.config[header])
        else:
            reader[header] = self.config[header][section]
        return reader
    
    def write(self, section, __key, __value):
        self.config.set(section, __key, __value)
        self.__save()

    def mkhd(self, header, __settings: dict):
        self.config[header] = __settings
        self.__save()
        
    def __save(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
        
    
    
class CSV:
    def __init__(self, filename):
        self.file = filename + ".csv" if ".csv" not in filename else filename
        self.exist = None

    def read(self, header=False):
        rows = []
        with open(self.file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            if self.isEmpty():
                return []
            try:
                h = next(reader)
            except StopIteration:
                header = False
            for row in reader:
                rows.append(row) if row else ''
            # Striping lists
            for r in range(len(rows)):
                for c in range(len(rows[r])):
                    if rows[r][c][0] == '[' and rows[r][c][-1] == ']':
                        rows[r][c] = [x.strip('[').strip(']').strip(' ').strip("'") for x in rows[r][c].split(',')]
            if header:
                return h, rows

            return rows

    def write(self, rows: list[list], header: list = None):
        with open(self.file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header) if header not in (None, True, False) else ''
            [writer.writerow(row) for row in rows]
        return self

    def append(self, row: list):
        with open(self.file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row)
        return self

    def pop(self, __index=-1):
        reader = self.read(header=True)
        h, reader = reader[0], reader[1:]
        reader.pop(__index)
        self.write(reader, header=h)
        return self
        
    def create(self):
        if self.file not in os.listdir(os.getcwd()):
            with open(self.file, "w+") as file: pass
        return self

    def cvtDF(self):
        import pandas as pd
        return pd.read_csv(self.file)

    def df_to_csv(self, df):
        df.to_csv(self.file)
        return self.read(header=True)

    def isEmpty(self):
        with open(self.file, "r", encoding="utf-8") as file:
            if len(file.read()) == 0:
                return True
            else:
                return False

    def copy(self, dst):
        shutil.copy(self.file, dst)
        return self

    def move(self, dst):
        shutil.move(self.file, dst)
        return self

    def remove(self):
        os.remove(self.file)
        return self

    def isExist(self):
        try:
            with open(self.file):
                self.exist = True
        except FileNotFoundError:
            self.exist = False
        return self.exist

    def rename(self, __new):
        os.rename(self.file, __new)
        return self

    def replace_row(self, i, __new, append=True):
        rows = self.read(True)
        try:
            rows[i + 1] = __new
        except IndexError:
            rows.append(__new)
        self.write(rows[1:], rows[0])

    def replace(self, i, __old, __new):
        with open(self.file, "r", encoding="utf-8") as file:
            con = file.readlines()
        con[i] = con[i].replace(__old, __new)
        with open(self.file, "w", encoding="utf-8") as file:
            file.writelines(con)
        return self


class File:
    def __init__(self, filename):
        self.file = filename
        self.exist = None

    def read(self):
        with open(self.file, "r", encoding="utf-8") as file:
            return file.read().split("\n")

    def write(self, content: list or tuple or str):
        with open(self.file, "w", encoding="utf-8") as file:
            file.writelines(content)
        return self

    def append(self, content: list or tuple or str, linebreak=True):
        if linebreak:
            if isinstance(content, list) or isinstance(content, tuple):
                content = [x + "\n" for x in content]
            else:
                content += "\n"
        with open(self.file, "a+", encoding="utf-8") as file:
            file.writelines(content)
        return self

    def create(self):
        if not self.file in os.listdir(os.getcwd()):
            with open(self.file, "w+", encoding="utf-8") as file: pass
        return self

    def replace(self, i, __old, __new):
        with open(self.file, "r", encoding="utf-8") as file:
            con = file.readlines()
        con[self.ch[0]] = con[self.ch[0]].replace(self.ch[1], self.ch[2])
        with open(self.file, "w", encoding="utf-8") as file:
            file.writelines(con)
        return self

    def isExist(self):
        try:
            with open(self.file):
                self.exist = True
        except FileNotFoundError:
            self.exist = False
        return self.exist

    def rename(self, __new):
        os.rename(self.file, __new)
        return self

    def copy(self, location=None):
        shutil.copy(self.file, location)
        return self

    def move(self, location):
        shutil.move(self.file, location)
        return self

    def remove(self):
        os.remove(self.file)
        return self
