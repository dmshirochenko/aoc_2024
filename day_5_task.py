# https://adventofcode.com/2024/day/5

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()

class ElfPrinter:
    def __init__(self):
        pass

    def reading_elf_data(self, file_name):
        rules = {}
        data_to_print = []
        is_rules = True
        for row in FileReader.gen_file_reader(file_name):
            if row == "":
                is_rules = False
                continue
            if is_rules:
                page_1, page_2 = map(int, row.split("|"))
                if page_1 not in rules:
                    rules[page_1] = {page_2}
                else:
                    rules[page_1].add(page_2)
            else:
                new_data = [int(num) for num in row.split(",")]
                data_to_print.append(new_data)
    

        return rules, data_to_print
    
    def is_update_data_correct(self, rules, data):
        is_data_correct_first_try = True
        is_data_correct = False
        prev_chars = []
        for index, element in enumerate(data):
            if element not in rules:
                prev_chars.append((element, index))
                continue
            
            should_not_be_prev_elements = rules[element]

            for char, index_prev in prev_chars:
                if char in should_not_be_prev_elements:
                    is_data_correct_first_try = False
                    while not is_data_correct:
                        data[index], data[index_prev] = data[index_prev], data[index]
                        _, is_data_correct, data = self.is_update_data_correct(rules, data)

            prev_chars.append((element, index))
        is_data_correct = True
        return is_data_correct_first_try, is_data_correct, data

    def get_middle_elements(self, update_data):
        middle_index = len(update_data) // 2
        return update_data[middle_index]

    def find_all_valid_midle_elements_sum(self, rules, data):
        valid_indexes_sum = 0
        invalid_indexes_sum = 0
        for i in range(len(data)):
            is_valid, _, data_fixed = self.is_update_data_correct(rules, data[i])
            if is_valid:
                middle_element = self.get_middle_elements(data[i])
                valid_indexes_sum += middle_element
            else:
                middle_element = self.get_middle_elements(data_fixed)
                invalid_indexes_sum += middle_element


        return valid_indexes_sum, invalid_indexes_sum

if __name__ == "__main__":
    elf_printer = ElfPrinter()
    rules, data_to_print = elf_printer.reading_elf_data("day_5.txt")
    valid_indexes_sum, invalid_indexes_sum = elf_printer.find_all_valid_midle_elements_sum(rules, data_to_print)
    #task 1
    print("valid indexes: ", valid_indexes_sum)
    #task 2
    print("invalid indexes: ", invalid_indexes_sum)