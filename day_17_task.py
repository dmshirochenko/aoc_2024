# https://adventofcode.com/2024/day/17
import heapq

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()

class ElfComputer:
    def __init__(self):
        self.register_a = None
        self.register_b = None
        self.register_c = None

        self.program_lst  = []
        self.program_output = []
    
    def reading_program_data(self, file_name):
        file_generator = FileReader.gen_file_reader(file_name)
        self.register_a = int(next(file_generator).split("Register A: ")[1])
        self.register_b = int(next(file_generator).split("Register B: ")[1])
        self.register_c = int(next(file_generator).split("Register C: ")[1])

        _ = next(file_generator)
        row_program = next(file_generator).lstrip("Program: ")
        self.program_lst = [int(num) for num in row_program.split(",")]
        return self.program_lst

    def get_combo_operand_value(self, literal_operand):
        if 0 <= literal_operand <= 3:
            return literal_operand
        if literal_operand == 4:
            return self.register_a
        if literal_operand == 5:
            return self.register_b
        if literal_operand == 6:
            return self.register_c

    def print_to_file(self, name, data):
        with open("day_17_logs.txt", "a") as file:
            file.write(name + str(data) + "\n")
    
    def instruntion_mapper(self, opcode, literal_operand):
        if opcode == 0:
            return self.opcode_0(literal_operand)
        if opcode == 1:
            return self.opcode_1(literal_operand)
        if opcode == 2:
            return self.opcode_2(literal_operand)
        if opcode == 3:
            return self.opcode_3(literal_operand)
        if opcode == 4:
            return self.opcode_4(literal_operand)
        if opcode == 5:
            return self.opcode_5(literal_operand)
        if opcode == 6:
            return self.opcode_6(literal_operand)
        if opcode == 7:
            return self.opcode_7(literal_operand)

    def opcode_0(self, literal_operand):
        combo_operand = self.get_combo_operand_value(literal_operand)
        updated_a_register = self.register_a // (2 ** combo_operand)

        self.register_a = updated_a_register

        return None

    def opcode_1(self, literal_operand):
        updated_b_register = self.register_b ^ literal_operand

        self.register_b = updated_b_register

        return None

    def opcode_2(self, literal_operand):
        combo_operand = self.get_combo_operand_value(literal_operand)
        updated_b_register = combo_operand % 8

        self.register_b = updated_b_register

        return None

    def opcode_3(self, literal_operand):
        new_instruction_pointer = literal_operand
        if self.register_a != 0:
            return new_instruction_pointer
        return None
     
    def opcode_4(self, literal_operand):
        updated_b_register = self.register_b ^ self.register_c

        self.register_b = updated_b_register

        return None

    def opcode_5(self, literal_operand):
        combo_operand = self.get_combo_operand_value(literal_operand) 

        self.program_output.append(combo_operand % 8)

        return None

    def opcode_6(self, literal_operand):
        combo_operand = self.get_combo_operand_value(literal_operand)
        updated_b_register = self.register_a // (2 ** combo_operand)

        self.register_b = updated_b_register

        return None
    
    def opcode_7(self, literal_operand):
        combo_operand = self.get_combo_operand_value(literal_operand)
        updated_c_register = self.register_a // (2 ** combo_operand)

        self.register_c = updated_c_register   

        return None

    def computer_program_execution(self):
        instruction_pointer = 0
        is_instruction_jump = True
        while instruction_pointer < len(self.program_lst):
            try:
                opcode = self.program_lst[instruction_pointer]
                operand = self.program_lst[instruction_pointer + 1]

                result = self.instruntion_mapper(opcode, operand)

                if result is not None:
                    instruction_pointer = result
                else:
                    instruction_pointer += 2
            except IndexError:
                break

        return self.program_output

if __name__ == "__main__":
    elf_computer = ElfComputer()
    program_lst = elf_computer.reading_program_data("day_17.txt")
    # task 1
    output = elf_computer.computer_program_execution()
    print("register a: ", elf_computer.register_a)
    print("register b: ", elf_computer.register_b)
    print("register c: ", elf_computer.register_c)
    print("output: ", ",".join(str(num) for num in output))