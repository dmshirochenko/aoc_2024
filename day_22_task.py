# https://adventofcode.com/2024/day/22
from collections import defaultdict


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class SecrerNumberGenerator:
    def __init__(self):
        self.secret_numbers_lst = []
        self.secret_numbers_best_sequnces = dict()

    def read_file_data(self, file_name):
        for row in FileReader.gen_file_reader(file_name):
            self.secret_numbers_lst.append(int(row))

        return self.secret_numbers_lst

    def print_dct_to_file(self, dct, file_name):
        with open(file_name, "w") as file:
            for key, value in dct.items():
                file.write(f"{key}: {value}\n")

    def get_secret_number(self, initial_secret_number):
        # first section
        cal_value_first = initial_secret_number * 64
        new_secret_number = cal_value_first ^ initial_secret_number
        new_secret_number = new_secret_number % 16777216

        # second section
        cal_value_second = new_secret_number // 32
        new_secret_number = cal_value_second ^ new_secret_number
        new_secret_number = new_secret_number % 16777216

        # third section
        cal_value_third = new_secret_number * 2048
        new_secret_number = cal_value_third ^ new_secret_number
        new_secret_number = new_secret_number % 16777216

        return new_secret_number

    def get_sum_of_secret_numbers_after_n_steps(self, n):
        for i in range(n):
            for index, number in enumerate(self.secret_numbers_lst):
                new_secret_number = self.get_secret_number(number)
                self.secret_numbers_lst[index] = new_secret_number

        return sum(self.secret_numbers_lst)

    def get_dct_with_secret_numbers_best_prices_sequence(self, n=2000):
        prices_lst = []

        for index, number in enumerate(self.secret_numbers_lst):
            price_lst = []
            change_lst = []
            price_lst.append(number % 10)
            initial_secret_number = number

            for i in range(n):
                new_secret_number = self.get_secret_number(number)
                price_lst.append(new_secret_number % 10)
                number = new_secret_number
                self.secret_numbers_lst[index] = new_secret_number

            change_lst = [b - a for a, b in zip(price_lst, price_lst[1:])]

            for i in range(len(change_lst) - 3):
                key = tuple(change_lst[i : i + 4])
                if key not in self.secret_numbers_best_sequnces:
                    self.secret_numbers_best_sequnces[key] = [(price_lst[i + 4], initial_secret_number)]
                else:
                    self.secret_numbers_best_sequnces[key].append((price_lst[i + 4], initial_secret_number))

        return self.secret_numbers_best_sequnces

    def get_max_num_of_bananas(self):
        max_num_of_bananas = 0
        for key, value in self.secret_numbers_best_sequnces.items():
            seen_initial_secret_num = set()
            sequence_max_num_of_bananas = 0
            for val in value:
                if val[1] in seen_initial_secret_num:
                    continue
                seen_initial_secret_num.add(val[1])

                sequence_max_num_of_bananas += val[0]

            max_num_of_bananas = max(max_num_of_bananas, sequence_max_num_of_bananas)

        return max_num_of_bananas


if __name__ == "__main__":
    secret_number_generator = SecrerNumberGenerator()
    secret_numbers_lst = secret_number_generator.read_file_data("day_22.txt")

    # task 1
    # sum_of_secret_numbers = secret_number_generator.get_sum_of_secret_numbers_after_n_steps(n=2000)
    # print("Sum of secret numbers is: ", sum(secret_numbers_lst))
    # task 2
    secret_number_generator.get_dct_with_secret_numbers_best_prices_sequence(n=2000)
    max_num_of_bananas = secret_number_generator.get_max_num_of_bananas()
    print("Max number of bananas: ", max_num_of_bananas)
