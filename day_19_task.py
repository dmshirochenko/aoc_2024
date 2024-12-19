# https://adventofcode.com/2024/day/19
from collections import deque
from multiprocessing import Pool, cpu_count
from functools import lru_cache


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class TowelDesign:
    def __init__(self):
        self.towel_patterns = set()
        self.max_pattern_length = 0
        self.desired_design = set()

    def read_file_data(self, file_name):
        file_generator = FileReader.gen_file_reader(file_name)
        tower_patterns_str = next(file_generator)
        _ = next(file_generator)  # skip empty line
        for row in file_generator:
            self.desired_design.add(row.strip())

        for pattern in tower_patterns_str.split(","):
            strippted_pattern = pattern.strip()
            self.towel_patterns.add(strippted_pattern)
            self.max_pattern_length = max(self.max_pattern_length, len(strippted_pattern))

        return self.towel_patterns, self.desired_design, self.max_pattern_length

    def check_if_design_is_possible_task_1(self, design, towel_patterns):
        num_of_possible_combinations = 0
        queue = deque()
        visited_path = set()
        # try to find first possible pattern
        for i in range(0, self.max_pattern_length + 1):
            if design[:i] in towel_patterns:
                queue.append((design, design[:i], i, (i,)))

        while queue:
            design, matched_part, index, index_tuple = queue.pop()
            if index == len(design):
                visited_path.add(index_tuple)
                num_of_possible_combinations += 1
                return 1

            if index_tuple in visited_path:
                continue

            if index > len(design):
                continue

            for i in range(index, min(index + self.max_pattern_length + 1, len(design) + 1)):
                if design[index:i] in towel_patterns:
                    tuple_to_add = (i,)
                    new_index_tuple = index_tuple + tuple_to_add
                    queue.append((design, design[index:i], i, new_index_tuple))
        if num_of_possible_combinations > 0:
            return num_of_possible_combinations
        return False

    def check_if_design_is_possible_task_2(self, design, towel_patterns):
        n = len(design)
        dp = [0] * (n + 1)
        dp[0] = 1

        for i in range(1, n + 1):
            for j in range(max(0, i - self.max_pattern_length), i):
                if design[j:i] in towel_patterns:
                    dp[i] += dp[j]

        if dp[n] > 0:
            print("Design is possible. Total combinations:", dp[n])
            return dp[n]
        return False

    @staticmethod
    def check_design_wrapper(args):
        instance, design, towel_patterns, task_num = args
        if task_num == 1:
            result = instance.check_if_design_is_possible_task_1(design, towel_patterns)
        else:
            result = instance.check_if_design_is_possible_task_2(design, towel_patterns)
        if result:
            print("Design is possible: ", design)
            return result
        else:
            print("Design is not possible: ", design)
            return 0

    def find_num_of_possible_designs(self, task_num=1):
        # Prepare arguments for the multiprocessing pool
        args = [(self, design, set(self.towel_patterns), task_num) for design in self.desired_design]

        # Use a multiprocessing pool to parallelize the checks
        with Pool(processes=cpu_count()) as pool:
            results = pool.map(self.check_design_wrapper, args)

        # Sum up the results to get the number of possible designs
        return sum(results)


if __name__ == "__main__":
    towel_design = TowelDesign()
    towel_patterns, desired_design, max_pattern_length = towel_design.read_file_data("day_19.txt")
    # task 1
    num_of_possible_designs_slow = towel_design.find_num_of_possible_designs(task_num=1)
    print("Number of possible designs slow: ", num_of_possible_designs_slow)
    # task 2
    num_of_possible_designs_fast = towel_design.find_num_of_possible_designs(task_num=2)
    print("Number of possible designs fast: ", num_of_possible_designs_fast)
