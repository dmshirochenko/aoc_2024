# https://adventofcode.com/2024/day/20
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class RaceCondition:
    def __init__(self):
        self.grid = []
        self.start = None
        self.end = None
        self.path_recovery_dct = dict()
        self.path_dct = dict()
        self.path_st = set()
        self.initial_num_of_steps = 0
        self.min_saved = 100

    def read_file_data(self, file_name):
        for row_index, row in enumerate(FileReader.gen_file_reader(file_name)):
            current_row = []
            for col_index, col in enumerate(row):
                if col == "S":
                    self.start = (row_index, col_index)
                elif col == "E":
                    self.end = (row_index, col_index)
                current_row.append(col)

            self.grid.append(current_row)

        return self.grid, self.start, self.end

    def print_grid(self):
        for row in self.grid:
            print("".join(row))

    def is_move_valid(self, row, col):
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            if grid[row][col] != "#":
                return True
        return False

    def bfs(self, grid, start_node, target_node, initial_run=False):
        num_of_steps = 0
        queue = deque([(start_node, num_of_steps, start_node)])
        visited = set()

        while queue:
            node, num_of_steps, source_node = queue.popleft()
            current_row = node[0]
            current_col = node[1]

            if node == target_node:
                self.path_recovery_dct[node] = source_node
                return num_of_steps

            if node in visited:
                continue

            if initial_run:
                self.path_recovery_dct[node] = source_node
            visited.add(node)

            for row, col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row = current_row + row
                new_col = current_col + col
                if self.is_move_valid(new_row, new_col):
                    queue.append(((new_row, new_col), num_of_steps + 1, node))

        return -1

    def path_recovery(self, start_node, target_node):
        path = dict()
        num_of_steps_left_to_target = 0
        num_of_steps_done = self.initial_num_of_steps
        current_node = target_node

        while current_node != start_node:
            self.path_st.add(current_node)
            path[current_node] = (num_of_steps_done, num_of_steps_left_to_target)
            current_node = self.path_recovery_dct[current_node]
            self.grid[current_node[0]][current_node[1]] = "O"
            num_of_steps_done -= 1
            num_of_steps_left_to_target += 1

        path[start_node] = (0, num_of_steps_left_to_target)
        self.path_st.add(start_node)
        return path

    def find_shortest_path(self, start_node, target_node, is_part_one):
        self.initial_num_of_steps = self.bfs(self.grid, start_node, target_node, initial_run=True)
        self.path_dct = self.path_recovery(start_node, target_node)

        if is_part_one:
            num_of_steps_lst = []
            for row_index, row in enumerate(self.grid):
                for col_index, col in enumerate(row):
                    print(row_index, col_index)
                    if self.grid[row_index][col_index] == "#":
                        self.grid[row_index][col_index] = "."
                        changed_wall_cell = (row_index, col_index)
                        num_of_steps = self.bfs(self.grid, start_node, target_node)
                        if self.initial_num_of_steps - num_of_steps >= 100:
                            num_of_steps_lst.append((num_of_steps, changed_wall_cell))
                        self.grid[row_index][col_index] = "#"

            return num_of_steps_lst
        else:
            num_of_steps_20_cheats_lst = 0
            num_of_saved_paths = 0
            for path_cell in self.path_st:
                for radius in range(20 + 1):
                    for manhattan_neighbor in self.neighbors(path_cell, radius):
                        if (
                            self.path_dct[manhattan_neighbor][0] - self.path_dct[path_cell][0]
                        ) - self.manhattan_distance(path_cell, manhattan_neighbor) >= self.min_saved:
                            num_of_saved_paths += 1

            return num_of_saved_paths

    def neighbors(self, point, radius):
        def _manhattan_neighbors(x, y, radius):
            neighbor_points = set()
            for delta_x in range(-radius, radius + 1):
                delta_y = radius - abs(delta_x)
                neighbor_points.add((x + delta_x, y + delta_y))
                neighbor_points.add((x + delta_x, y - delta_y))
            return neighbor_points

        return _manhattan_neighbors(point[0], point[1], radius) & self.path_st

    def manhattan_distance(self, point_a, point_b):
        return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


if __name__ == "__main__":
    race_condition_instance = RaceCondition()
    grid, start, end = race_condition_instance.read_file_data("day_20.txt")
    # task_1
    num_of_steps_lst = race_condition_instance.find_shortest_path(start, end, is_part_one=True)
    print("Number of steps task 1:", len(num_of_steps_lst))
    # task_2
    num_of_steps_20_cheats = race_condition_instance.find_shortest_path(start, end, is_part_one=False)
    print("Number of steps task 2:", num_of_steps_20_cheats)
