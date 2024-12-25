# https://adventofcode.com/2024/day/25
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class CodeChronicle:
    def __init__(self):
        self.loks_lst = []
        self.keys_lst = []
        self.max_col = 7
        self.max_row = 5

    def read_file_data(self, file_name):
        temp_lst = [0] * 5
        is_first_row = True
        is_lock = True
        for row in FileReader.gen_file_reader(file_name):
            if row == "":
                if is_lock:
                    self.loks_lst.append(temp_lst)
                else:
                    self.keys_lst.append(temp_lst)
                temp_lst = [0] * 5
                is_first_row = True
                continue

            for index, char in enumerate(row):
                if char == "#":
                    temp_lst[index] += 1

            if is_first_row:
                is_first_row = False
                if all(el == "#" for el in row):
                    is_lock = True
                else:
                    is_lock = False
                continue
        else:
            if is_lock:
                self.loks_lst.append(temp_lst)
            else:
                self.keys_lst.append(temp_lst)

    def check_if_key_fits(self):
        count_fits = 0
        for key in self.keys_lst:
            for lock in self.loks_lst:
                if all(k + l <= self.max_col for k, l in zip(key, lock)):
                    print("Key fits")
                    count_fits += 1

        return count_fits


if __name__ == "__main__":
    code_chronicle = CodeChronicle()
    code_chronicle.read_file_data("day_25.txt")
    count_fits = code_chronicle.check_if_key_fits()
    print("Task 1:", count_fits)
