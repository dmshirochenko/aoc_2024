# https://adventofcode.com/2024/day/6

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()

possible_directions = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1)
}

turn_90_degrees_right = {
    "up": "right",
    "down": "left",
    "left": "up",
    "right": "down"
}

arrow_mapper = {
    "up": "^",
    "down": "v",
    "left": "<",
    "right": ">"
}

class GuardSurfer:
    def __init__(self):
        pass

    def reading_guard_data(self, file_name):
        grid = []
        guard_starting_position = None
        row = 0
        col = 0
        for line in FileReader.gen_file_reader(file_name):
            col = 0
            line_lst = []
            for char in line:
                line_lst.append(char)
                if char == "^":
                    guard_starting_position = (row, col)
                col += 1
            grid.append(line_lst)
            row += 1

        return grid, guard_starting_position
    
    def is_in_grid(self, grid, row, col):
        if row < 0 or row >= len(grid):
            return False
        if col < 0 or col >= len(grid[0]):
            return False
        return True

    def print_grid(self, grid):
        for row in grid:
            print("".join(row))
        
    
    def get_grid_size(self, grid):
        return len(grid) * len(grid[0])

    def simulating_guard_walk(self, grid, guard_starting_position):
        row, col = guard_starting_position
        direction = "up"
        visited_cells = set()
        visited_cells.add((row, col))

        is_a_cycle = False

        while True:
            
            row += possible_directions[direction][0]
            col += possible_directions[direction][1]
            if not self.is_in_grid(grid, row, col):
                break
            if grid[row][col] == "#" or grid[row][col] == "O":
                #step back and turn 
                row -= possible_directions[direction][0]
                col -= possible_directions[direction][1]
                direction = turn_90_degrees_right[direction]
                continue
            if grid[row][col] == arrow_mapper[direction]:
                is_a_cycle = True
                break
            grid[row][col] = arrow_mapper[direction]

            if (row, col) not in visited_cells:
                visited_cells.add((row, col))

                    

        return visited_cells, is_a_cycle

    def check_if_cycle_possible_for_each_cell(self, grid, guard_starting_position, visited_cells):
        row, col = guard_starting_position
        grid_size = self.get_grid_size(grid)
        num_of_obsticales_that_lead_to_cycle = 0
        cells_left = grid_size
        for i, j in visited_cells:
                if grid[i][j] == "#" or grid[i][j] == "^":
                    continue
                grid_copy = [row[:] for row in grid]
                grid_copy[i][j] = "O"
                steps, is_a_cycle = self.simulating_guard_walk(grid_copy, (row, col))
                
                if is_a_cycle:
                    num_of_obsticales_that_lead_to_cycle += 1
                cells_left -= 1
        return num_of_obsticales_that_lead_to_cycle

if __name__ == "__main__":
    guard_surfer = GuardSurfer()
    grid, guard_starting_position = guard_surfer.reading_guard_data("day_6.txt")
    grid_copy = [row[:] for row in grid]
    visited_cells, _ = guard_surfer.simulating_guard_walk(grid_copy, guard_starting_position)
    #task 1
    print("guard steps: ", len(visited_cells))
    #task 2
    num_of_obsticales_that_lead_to_cycle = guard_surfer.check_if_cycle_possible_for_each_cell(grid, guard_starting_position, visited_cells)
    print("num_of_obsticales_that_lead_to_cycle: ", num_of_obsticales_that_lead_to_cycle)