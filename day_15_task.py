# https://adventofcode.com/2024/day/15


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


MOVES = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


class Robot:
    def __init__(self):
        self.robot_moves = []
        self.grid = []
        self.robot_initial_position = None

    def reading_robot_data(self, file_name):
        is_grid = True
        row_index = 0
        for row in FileReader.gen_file_reader(file_name):
            if is_grid:
                if row == "":
                    is_grid = False
                    continue

                line = []
                for col, char in enumerate(row):
                    if char == "#":
                        char_1 = "#"
                        char_2 = "#"
                    if char == "O":
                        char_1 = "["
                        char_2 = "]"
                    if char == ".":
                        char_1 = "."
                        char_2 = "."
                    if char == "@":
                        char_1 = "@"
                        char_2 = "."

                    line.append(char_1)
                    line.append(char_2)

                self.grid.append(line)
                row_index += 1
            else:
                for char in row:
                    if char != "\n":
                        self.robot_moves.append(char)

        return self.grid, self.robot_moves

    def print_grid(self):
        for row in self.grid:
            print("".join(row))

    def is_valid_move(self, new_row, new_col):
        if self.grid[new_row][new_col] == "#":
            return False
        return True

    def find_robot_initial_position(self):
        for row_index, row in enumerate(self.grid):
            for col_index, char in enumerate(row):
                if char == "@":
                    self.robot_initial_position = (row_index, col_index)
                    return self.robot_initial_position

    def shift_rocks_task_1(self, move, new_row, new_col):
        # check how many rocks are there
        count_rocks = []
        while self.grid[new_row][new_col] == "O":
            count_rocks.append((move, new_row, new_col))
            new_row += MOVES[move][0]
            new_col += MOVES[move][1]

        # check if there no wall after last rock
        if self.grid[new_row][new_col] == "#":
            return False

        # move rocks
        is_first_rock = True
        for move, row, col in count_rocks:
            if is_first_rock:
                self.grid[row][col] = "."
                is_first_rock = False
            else:
                self.grid[row][col] = "O"
            row += MOVES[move][0]
            col += MOVES[move][1]
            self.grid[row][col] = "O"

        return True

    def get_close_bracket(self, move, new_row, new_col):
        # (move, cell_value, new_row, new_col)
        if self.grid[new_row][new_col] == "[":
            return (move, "]", new_row, new_col + 1)
        if self.grid[new_row][new_col] == "]":
            return (move, "[", new_row, new_col - 1)

    def shift_rocks_task_2(self, move, new_row, new_col):
        # check how many rocks are there
        print("Grid:")
        self.print_grid()
        print("next move:", move)
        print("_________________________")
        count_rocks = []
        if move in ["^", "v"]:
            # add first rock
            count_rocks.append((move, self.grid[new_row][new_col], new_row, new_col))
            # add close bracket
            close_bracket = self.get_close_bracket(move, new_row, new_col)
            count_rocks.append(close_bracket)
            new_row += MOVES[move][0]
            new_col += MOVES[move][1]

            last_rock_row = count_rocks[:]
            is_last_row_empty = False
            while not is_last_row_empty:
                temp_last_rock_row = []
                for rock in last_rock_row:
                    print("rock:", rock)
                    move, cell_value, row, col = rock
                    row += MOVES[move][0]
                    col += MOVES[move][1]
                    cell_value = self.grid[row][col]
                    if self.grid[row][col] == "#":
                        return False
                    if self.grid[row][col] in ["[", "]"]:
                        if (move, cell_value, row, col) not in temp_last_rock_row:
                            temp_last_rock_row.append((move, cell_value, row, col))
                            close_bracket = self.get_close_bracket(move, row, col)
                            temp_last_rock_row.append(close_bracket)
                        else:
                            continue
                print("temp_last_rock_row:", temp_last_rock_row)
                if temp_last_rock_row:
                    count_rocks.extend(temp_last_rock_row)
                    last_rock_row = temp_last_rock_row[:]
                    temp_last_rock_row = []
                else:
                    is_last_row_empty = True

        if move == "<" and self.grid[new_row][new_col] == "]":
            while self.grid[new_row][new_col] == "]":
                cell_value = self.grid[new_row][new_col]
                count_rocks.append((move, cell_value, new_row, new_col))
                # open bracket is from the right side
                open_bracket_row = new_row
                right_side_col = new_col - 1
                cell_value = self.grid[open_bracket_row][right_side_col]
                count_rocks.append((move, cell_value, open_bracket_row, right_side_col))
                new_row += MOVES[move][0]
                new_col += MOVES[move][1] - 1

        if move == ">" and self.grid[new_row][new_col] == "[":
            while self.grid[new_row][new_col] == "[":
                cell_value = self.grid[new_row][new_col]
                count_rocks.append((move, cell_value, new_row, new_col))
                # close bracket is from the right side
                close_bracket_row = new_row
                right_side_col = new_col + 1
                cell_value = self.grid[close_bracket_row][right_side_col]
                count_rocks.append((move, cell_value, close_bracket_row, right_side_col))
                new_row += MOVES[move][0]
                new_col += MOVES[move][1] + 1

        # check if there no wall after last rock
        last_rock_coord = (count_rocks[-1], count_rocks[-2])
        for rock in last_rock_coord:
            rock_row, row_col = rock[2], rock[3]

            new_row = rock_row + MOVES[move][0]
            new_col = row_col + MOVES[move][1]
            if self.grid[new_row][new_col] == "#":
                return False

        # move rocks
        count_rocks = count_rocks[::-1]
        for i in range(len(count_rocks) - 2):
            move, cell_value, row, col = count_rocks[i]
            self.grid[row][col] = "."
            # move rock
            row += MOVES[move][0]
            col += MOVES[move][1]
            self.grid[row][col] = cell_value
        else:
            # last 2 brackets
            rock_1 = count_rocks[-2]
            rock_2 = count_rocks[-1]

            move, cell_value, row, col = rock_1
            self.grid[row][col] = "."
            row += MOVES[move][0]
            col += MOVES[move][1]
            self.grid[row][col] = cell_value

            move, cell_value, row, col = rock_2
            self.grid[row][col] = "."
            row += MOVES[move][0]
            col += MOVES[move][1]
            self.grid[row][col] = cell_value

        return True

    def movement_simulation(self):
        row, col = self.robot_initial_position
        for move in self.robot_moves:
            new_row = row + MOVES[move][0]
            new_col = col + MOVES[move][1]

            if not self.is_valid_move(new_row, new_col):
                continue

            if self.grid[new_row][new_col] in ["[", "]"]:
                if not self.shift_rocks_task_2(move, new_row, new_col):
                    continue

            self.grid[row][col] = "."
            self.grid[new_row][new_col] = "@"
            row, col = new_row, new_col

        return self.grid

    def sum_of_final_box_gps_coordinates(self):
        sum_of_coordinates = 0

        for row_index, row in enumerate(self.grid):
            for col_index, char in enumerate(row):
                if char == "[":
                    sum_of_coordinates += 100 * row_index + col_index

        return sum_of_coordinates


if __name__ == "__main__":
    robot = Robot()
    robot.reading_robot_data("day_15.txt")
    robot.find_robot_initial_position()
    robot.movement_simulation()
    robot.print_grid()
    sum_of_coordinates = robot.sum_of_final_box_gps_coordinates()
    print("Sum of coordinates:", sum_of_coordinates)
