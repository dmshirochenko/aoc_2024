# https://adventofcode.com/2024/day/3
import re


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class ComputerChecker:
    def __init__(self):
        pass

    def reading_computer_data(self, file_name):
        computer_data = ""
        for row in FileReader.gen_file_reader(file_name):
            computer_data += row

        return computer_data

    def reg_exp_matching(self, report):
        pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)"

        matches = re.findall(pattern, report)

        return matches

    def reg_exp_matching_result_multiplication(self, matching_lst):
        result = 0
        for match in matching_lst:
            digit_left, digit_right = match[4:-1].split(",")
            result += int(digit_left) * int(digit_right)

        return result

    def finding_given_pattern(self, report):
        digit_lst = []
        # pattern mul(5,5)
        for i in range(5, len(report)):
            left = i - 1
            right = i + 1
            possible_digits_left = 3
            is_digit_left_exist = False
            is_bracket_left_exist = False
            is_valid = True
            possible_digits_right = 3
            is_digit_right_exist = False
            is_bracket_right_exist = False
            is_valid = True
            if report[i] == ",":
                while True:
                    if report[left].isdigit() and possible_digits_left > 0:
                        possible_digits_left -= 1
                        is_digit_left_exist = True
                    elif report[left] == "(":
                        is_bracket_left_exist = True
                        break
                    else:
                        is_valid = False
                        break

                    left -= 1

                while True:
                    if report[right].isdigit() and possible_digits_right > 0:
                        possible_digits_right -= 1
                        is_digit_right_exist = True
                    elif report[right] == ")":
                        is_bracket_right_exist = True
                        break
                    else:
                        is_valid = False
                        break

                    right += 1

            if report[i] == "d":

                if report[i : i + 4] == "do()":
                    digit_lst.append(1)
                elif report[i : i + 7] == "don't()":
                    digit_lst.append(0)

            if (
                is_valid
                and is_digit_left_exist
                and is_bracket_left_exist
                and is_digit_right_exist
                and is_bracket_right_exist
            ):
                if report[left - 3 : left] == "mul":
                    digit_left, digit_right = report[left + 1 : right].split(",")
                    digit_lst.append((int(digit_left), int(digit_right)))

        return digit_lst

    def digit_multiplication(self, digit_lst):
        result = 0
        for digits in digit_lst:
            if digits in [0, 1]:
                continue
            digit_left, digit_right = digits
            result += digit_left * digit_right

        return result

    def digit_multiplication_with_do_and_dont(self, digit_lst):
        result = 0
        do_multiplier = 1
        for digits in digit_lst:
            if digits in [0, 1]:
                do_multiplier = digits
                continue
            digit_left, digit_right = digits
            result += digit_left * digit_right * do_multiplier

        return result


if __name__ == "__main__":
    checker = ComputerChecker()
    report = checker.reading_computer_data("day_3.txt")
    digit_lst = checker.finding_given_pattern(report)
    reg_exp_matches = checker.reg_exp_matching(report)
    result = checker.digit_multiplication(digit_lst)
    result_reg_exp = checker.reg_exp_matching_result_multiplication(reg_exp_matches)
    # task 1
    print("result: ", result)
    print("result_reg_exp: ", result_reg_exp)
    # task 2
    result_do_dont = checker.digit_multiplication_with_do_and_dont(digit_lst)
    print("result_do_dont: ", result_do_dont)
