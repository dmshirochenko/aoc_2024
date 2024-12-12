import copy


class FileReader:
    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


# Constants for movement
POSSIBLE_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]
MOVE_DIRECTIONS = {"right": (0, 1), "left": (0, -1), "down": (1, 0), "up": (-1, 0)}


class FencePlanner:
    def __init__(self):
        self.garden_grid = []
        self.global_visited = set()
        self.areas = []

    def read_fence_data(self, file_name):
        self.garden_grid = [list(row) for row in FileReader.gen_file_reader(file_name)]
        return self.garden_grid

    def print_grid(self, grid):
        for row in grid:
            print("".join(row))

    def bfs(self, grid, start):
        queue = [start]
        visited = set()

        while queue:
            node = queue.pop(0)
            if node in visited:
                continue

            visited.add(node)
            row, col = node

            for move in POSSIBLE_MOVES:
                new_row, new_col = row + move[0], col + move[1]
                if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                    if grid[new_row][new_col] == grid[row][col]:
                        queue.append((new_row, new_col))

        return visited

    def get_all_areas(self, grid):
        self.areas = []

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if (row, col) not in self.global_visited:
                    area = self.bfs(grid, (row, col))
                    self.areas.append({grid[row][col]: area})
                    self.global_visited.update(area)

        return self.areas

    def get_area_perimeter(self, grid, area):
        perimeter = len(area) * 4

        for row, col in area:
            for move in POSSIBLE_MOVES:
                new_row, new_col = row + move[0], col + move[1]
                if (new_row, new_col) in area:
                    perimeter -= 1

        return perimeter

    def get_region_perimeter(self, grid, area):
        region_border_cells = {
            (row, col) for row, col in area for move in POSSIBLE_MOVES if (row + move[0], col + move[1]) not in area
        }

        grouped_sides = {}
        for cell in region_border_cells:
            for direction, move in MOVE_DIRECTIONS.items():
                neighbor = (cell[0] + move[0], cell[1] + move[1])
                if neighbor not in area:
                    grouped_sides.setdefault(direction, set()).add(neighbor)

        count_sides = 0
        for side_cells in grouped_sides.values():
            visited = set()
            for cell in side_cells:
                if cell in visited:
                    continue

                count_sides += 1
                queue = [cell]

                while queue:
                    node = queue.pop(0)
                    if node in visited:
                        continue

                    visited.add(node)
                    for move in POSSIBLE_MOVES:
                        neighbor = (node[0] + move[0], node[1] + move[1])
                        if neighbor in side_cells:
                            queue.append(neighbor)

        return count_sides

    def calculate_region_values(self, grid):
        total_score = 0
        total_side_score = 0

        for area in self.get_all_areas(grid):
            for _, cells in area.items():
                perimeter = self.get_area_perimeter(grid, cells)
                area_score = len(cells)
                total_score += area_score * perimeter

                side_perimeter = self.get_region_perimeter(grid, cells)
                total_side_score += side_perimeter * area_score

        return total_score, total_side_score


if __name__ == "__main__":
    fence_planner = FencePlanner()
    fence_planner.read_fence_data("day_12.txt")
    total, side_total = fence_planner.calculate_region_values(fence_planner.garden_grid)
    # 1st part
    print("Total fence cells:", total)
    # 2nd part
    print("Total side fence cells:", side_total)
