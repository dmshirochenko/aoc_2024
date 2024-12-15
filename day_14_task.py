# https://adventofcode.com/2024/day/14


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class RobotDetector:
    def __init__(self, num_row, num_col):
        self.robot_data = []
        self.grid = [["." for _ in range(num_col)] for _ in range(num_row)]
        self.num_row = num_row
        self.num_col = num_col

    def reading_robot_data(self, file_name):
        for row in FileReader.gen_file_reader(file_name):
            position_str, velocity_str = row.split(" ")
            position = tuple(map(int, position_str.replace("p=", "").split(",")))
            position = (position[1], position[0])
            velocity = tuple(map(int, velocity_str.replace("v=", "").split(",")))
            velocity = (velocity[1], velocity[0])
            self.robot_data.append((position, velocity))

        return self.robot_data

    def print_grid(self):
        for row in self.grid:
            print("".join(str(cell) for cell in row))

    def print_grid_to_file(self, file_name):
        with open(file_name, "a") as file:
            for row in self.grid:
                file.write("".join(str(cell) for cell in row) + "\n")

    def print_to_file(self, file_name, data):
        with open(file_name, "a") as file:
            file.write(data + "\n")

    def clean_grid_to_default(self):
        self.grid = [["." for _ in range(self.num_col)] for _ in range(self.num_row)]

    def is_in_the_grid(self, row, col):
        if row < 0 or row >= self.num_row:
            return False
        if col < 0 or col >= self.num_col:
            return False
        return True

    def teleport_robot(self, position, velocity):
        curr_row, curr_col = position
        num_row, num_col = self.num_row, self.num_col

        new_row = curr_row + velocity[0]
        new_col = curr_col + velocity[1]

        if self.is_in_the_grid(new_row, new_col):
            return new_row, new_col

        if new_row < 0:
            new_row = (new_row % num_row + num_row) % num_row
        elif new_row >= num_row:
            new_row = new_row % num_row

        if new_col < 0:
            new_col = (new_col % num_col + num_col) % num_col
        elif new_col >= num_col:
            new_col = new_col % num_col

        return new_row, new_col

    def movement_simulation(self, num_of_seconds):
        num_sec_end = 10_000
        for i in range(1, num_sec_end):
            for index, robot in enumerate(self.robot_data):
                position, velocity = robot
                new_position = self.teleport_robot(position, velocity)
                self.robot_data[index] = (new_position, velocity)
                if self.grid[position[0]][position[1]] in [".", 1]:
                    self.grid[position[0]][position[1]] = "."
                else:
                    self.grid[position[0]][position[1]] -= 1
                if self.grid[new_position[0]][new_position[1]] == ".":
                    self.grid[new_position[0]][new_position[1]] = 1
                else:
                    self.grid[new_position[0]][new_position[1]] += 1

            if i > 7000 and i < 8000:
                self.print_to_file("grid_day_14.txt", f"Num of seconds: {i}")
                self.print_grid_to_file(f"grid_day_14.txt")

        return self.grid

    def calculate_robots_per_quadrant(self):
        quadrant_coordinates = {
            "I": ((0, self.num_row // 2), (0, self.num_col // 2)),
            "II": ((self.num_row // 2, self.num_row), (0, self.num_col // 2)),
            "III": ((self.num_row // 2, self.num_row), (self.num_col // 2, self.num_col)),
            "IV": ((0, self.num_row // 2), (self.num_col // 2, self.num_col)),
        }

        middle_row = self.num_row // 2
        middle_col = self.num_col // 2
        multiplication_factor_lst = []
        for key, value in quadrant_coordinates.items():
            count = 0
            for row in range(value[0][0], value[0][1]):
                for col in range(value[1][0], value[1][1]):
                    if self.grid[row][col] != ".":
                        if row != middle_row and col != middle_col:
                            count += self.grid[row][col]
            multiplication_factor_lst.append(count)

        multiplication_factor = 1
        for factor in multiplication_factor_lst:
            multiplication_factor *= factor

        return multiplication_factor


if __name__ == "__main__":
    num_of_seconds = 2_000
    robot_detector = RobotDetector(num_row=103, num_col=101)
    robot_data = robot_detector.reading_robot_data("day_14.txt")
    robot_detector.movement_simulation(num_of_seconds)
    multiplication_factor = robot_detector.calculate_robots_per_quadrant()
    print("Num of seconds:", num_of_seconds)
    robot_detector.print_grid()
    robot_detector.clean_grid_to_default()
