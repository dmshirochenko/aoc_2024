# https://adventofcode.com/2024/day/18
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


POSSIBLE_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class RamRun:
    def __init__(self, grid_size):
        self.grid = self.generating_grid(grid_size)
        self.last_fallen_bits = None

    def generating_grid(self, grid_size):
        grid = []
        for row in range(grid_size):
            grid.append(["."] * grid_size)
        return grid

    def reading_fallen_bits_from_file(self, file_name, num_of_fallen_bits_to_record):
        file_generator = FileReader.gen_file_reader(file_name)
        num_of_fallen_bits = num_of_fallen_bits_to_record
        for row in file_generator:
            if num_of_fallen_bits == 0:
                break
            row, col = row.split(",")
            self.grid[int(row)][int(col)] = "#"
            self.last_fallen_bits = row, col
            num_of_fallen_bits -= 1

    def print_grid(self):
        for row in self.grid:
            print("".join(row))

    def is_move_valid(self, row, col):
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            return True
        return False

    def bfs(self, start_node, target_node):
        num_of_steps = 0
        queue = deque([(start_node, num_of_steps)])
        visited = set()
        while queue:
            node, num_of_steps = queue.popleft()
            current_row = node[0]
            current_col = node[1]

            if node == target_node:
                return num_of_steps

            if node in visited:
                continue
            visited.add(node)

            for move in POSSIBLE_MOVES:
                new_row = current_row + move[0]
                new_col = current_col + move[1]
                if self.is_move_valid(new_row, new_col) and self.grid[new_row][new_col] == ".":
                    queue.append(((new_row, new_col), num_of_steps + 1))

        return False

    def find_shortest_path(self, start_node, target_node):
        return self.bfs(start_node, target_node)


if __name__ == "__main__":
    file = "day_18.txt"
    ram_run_instance = RamRun(grid_size=71)
    num_of_fallen_bits = 3450
    for num_of_bits in range(1024, num_of_fallen_bits):
        print("Checking number of bits: ", num_of_bits)
        ram_run_instance.reading_fallen_bits_from_file(file, num_of_fallen_bits_to_record=num_of_bits)
        result = ram_run_instance.find_shortest_path((0, 0), (70, 70))
        if not result:
            print("No path found")
            print("Number of bits: ", num_of_bits, ram_run_instance.last_fallen_bits)
            break
    ram_run_instance.print_grid()
    print("End of program")
