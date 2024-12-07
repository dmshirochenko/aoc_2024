# https://adventofcode.com/2024/day/7
import itertools

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()

operator_mapper = {
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
    "||" : lambda x, y: int((str(x) + str(y)))
}

class BridgeCalibrator:
    def __init__(self):
        pass

    def reading_bridge_data(self, file_name):
        bridge_data = []
        for row in FileReader.gen_file_reader(file_name):
            raw_data = row.split(" ")
            equation_result_str = raw_data.pop(0).rstrip(":")
            equation_result = int(equation_result_str)
            input_data = [int(item) for item in raw_data]
            bridge_data.append((equation_result, input_data))
            
        return bridge_data

    def combinations_of_sum_and_multiplication(self, num_of_signs, task):
        if task == 1:
            return list(itertools.product(["+", "*"], repeat=num_of_signs))
        else:
            return list(itertools.product(["+", "*", "||"], repeat=num_of_signs))

    def check_sum_of_valid_equation(self, bridge_data, task):
        sum_of_valid_equations = 0
        list_of_valid_equations = []

        for equation_result, input_data in bridge_data:
            num_of_signs = len(input_data) - 1
            for signs in self.combinations_of_sum_and_multiplication(num_of_signs, task):
                result = input_data[0]
                for index, sign in enumerate(signs):
                    result = operator_mapper[sign](result, input_data[index + 1])

                if result == equation_result:
                    sum_of_valid_equations += result
                    list_of_valid_equations.append(equation_result)
                    break
        
        return sum_of_valid_equations

        
if __name__ == "__main__":
    bridge_calibrator = BridgeCalibrator()
    bridge_data = bridge_calibrator.reading_bridge_data("day_7.txt")
    sum_of_valid_equations = bridge_calibrator.check_sum_of_valid_equation(bridge_data, 1)
    #task 1
    print("sum of valid equations: ", sum_of_valid_equations)
    #task 2
    sum_of_valid_equations = bridge_calibrator.check_sum_of_valid_equation(bridge_data, 2)
    print("sum of valid equations: ", sum_of_valid_equations)