# https://adventofcode.com/2024/day/9
import math
import itertools
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


possible_moves = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}


class HikePro:
    def __init__(self):
        self.hike_grid = []
        self.hike_grid_copy = []
        self.starting_points = []
        self.all_unique_paths = 0

    def reading_hike_data(self, file_name):
        curr_row = 0
        for row in FileReader.gen_file_reader(file_name):
            row_lst = []
            for col, char in enumerate(row):
                if char == ".":
                    row_lst.append(char)
                    continue
                elif int(char) == 0:
                    self.starting_points.append((curr_row, col))
                row_lst.append(int(char))

            self.hike_grid.append(row_lst)
            curr_row += 1

        self.hike_grid_copy = [row[:] for row in self.hike_grid]
        return self.hike_grid

    def print_grid(self, grid):
        for row in grid:
            print("".join(str(cell) for cell in row))

    def is_in_the_grid(self, row, col):
        if row < 0 or row >= len(self.hike_grid):
            return False
        if col < 0 or col >= len(self.hike_grid[0]):
            return False
        return True

    def bfs(self, start_row, start_col, unique_paths):
        grid_copy = [row[:] for row in self.hike_grid]
        times_reached_end = 0
        queue = deque()
        queue.append((start_row, start_col))
        visited = set()
        while queue:

            row, col = queue.popleft()
            current_sell_value = self.hike_grid[row][col]
            if unique_paths:
                if (row, col) in visited:
                    continue
            if current_sell_value == 9:
                times_reached_end += 1
                visited.add((row, col))
                continue
            visited.add((row, col))
            for move in possible_moves.values():
                new_row, new_col = row + move[0], col + move[1]
                if self.is_in_the_grid(new_row, new_col):
                    new_cell_value = self.hike_grid[new_row][new_col]
                    if new_cell_value == ".":
                        continue
                    if new_cell_value == current_sell_value + 1:
                        grid_copy[new_row][new_col] = "#"
                        queue.append((new_row, new_col))

        return times_reached_end

    def count_routes(self, unique_paths=False):
        sum_of_trails = 0
        for start_row, start_col in self.starting_points:
            sum_of_trails += self.bfs(start_row, start_col, unique_paths)

        return sum_of_trails


if __name__ == "__main__":
    hike_pro = HikePro()
    hike_pro.reading_hike_data("day_10.txt")
    sum_unique_of_trails = hike_pro.count_routes(unique_paths=True)
    # task 1
    print("sum of unique trails: ", sum_unique_of_trails)
    # task 2
    sum_of_all_trails = hike_pro.count_routes(unique_paths=False)
    print("sum of all trails: ", sum_of_all_trails)
