# https://adventofcode.com/2024/day/8
import math
import itertools


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class AntennaDetector:
    def __init__(self):
        self.grid_set = set()
        self.new_coords_set = set()
        self.bounds = None

    def reading_antenna_data(self, file_name):
        grid = []
        row = 0
        for line in FileReader.gen_file_reader(file_name):
            line_lst = []
            for index, char in enumerate(line):
                line_lst.append(char)
                self.grid_set.add((row, index))
            grid.append(line_lst)
            row += 1

        self.bounds = (len(grid[0]), len(grid))
        return grid

    def print_grid(self, grid):
        for row in grid:
            print("".join(row))

    def inbounds(self, coord):
        x, y = coord
        return 0 <= x < self.bounds[0] and 0 <= y < self.bounds[1]

    def coord_pair_combination(self, coords):
        coords_pairs_product = {}
        for item, coords in coords.items():
            coords_pairs_product[item] = list(itertools.combinations(coords, 2))

        return coords_pairs_product

    def porints_coords(self, grid):
        coords = {}
        for row_index, row in enumerate(grid):
            for col_index, char in enumerate(row):
                if char != ".":
                    if char not in coords:
                        coords[char] = [(row_index, col_index)]
                    else:
                        coords[char].append((row_index, col_index))

        return coords

    def symmetric_points(self, coord_1, coord_2):
        valid_antinodes = set()

        y_1, x_1 = coord_1
        y_2, x_2 = coord_2
        p_1 = (2 * x_1 - x_2, 2 * y_1 - y_2)
        if self.inbounds(p_1):
            valid_antinodes.add(p_1)
        p_2 = (2 * x_2 - x_1, 2 * y_2 - y_1)
        if self.inbounds(p_2):
            valid_antinodes.add(p_2)

        return valid_antinodes

    def symmetric_points_with_checking_all_distances(self, coord_1, coord_2):
        valid_antinodes = set()

        y_1, x_1 = coord_1
        y_2, x_2 = coord_2

        diff = (x_2 - x_1, y_2 - y_1)
        distance = 0

        while True:
            p_1 = (x_2 + distance * diff[0], y_2 + distance * diff[1])
            if self.inbounds(p_1):
                valid_antinodes.add(p_1)
            p_2 = (x_1 - distance * diff[0], y_1 - distance * diff[1])
            if self.inbounds(p_2):
                valid_antinodes.add(p_2)

            if not self.inbounds(p_1) and not self.inbounds(p_2):
                break

            distance += 1

        return valid_antinodes

    def new_point_at_angle(self, pair_coords_product, grid):
        antinodes_part_1 = set()
        antinodes_part_2 = set()

        for item, coords in pair_coords_product.items():
            for coord_1, coord_2 in coords:
                given_2_points_antinodes = self.symmetric_points(coord_1, coord_2)
                for antinode in given_2_points_antinodes:
                    antinodes_part_1.add(antinode)
                    # grid[antinode[1]][antinode[0]] = "#"

                given_2_points_antinodes_part_2 = self.symmetric_points_with_checking_all_distances(coord_1, coord_2)
                for antinode in given_2_points_antinodes_part_2:
                    antinodes_part_2.add(antinode)
                    grid[antinode[1]][antinode[0]] = "#"

        return antinodes_part_1, antinodes_part_2


if __name__ == "__main__":
    file_name = "day_8.txt"
    antenna_detector = AntennaDetector()
    grid = antenna_detector.reading_antenna_data(file_name)
    porints_coords = antenna_detector.porints_coords(grid)
    pair_coords_product = antenna_detector.coord_pair_combination(porints_coords)
    antinodes_part_1, antinodes_part_2 = antenna_detector.new_point_at_angle(pair_coords_product, grid)
    antenna_detector.print_grid(grid)
    # task 1
    print("number of antinodes: ", len(antinodes_part_1))
    # task 2
    print("number of antinodes: ", len(antinodes_part_2))
