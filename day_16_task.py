# https://adventofcode.com/2024/day/16
import heapq


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


POSSIBLE_MOVES = {
    "right": (0, 1),
    "down": (1, 0),
    "left": (0, -1),
    "up": (-1, 0),
}

DIRECTION_TO_ARROW = {
    "right": ">",
    "down": "v",
    "left": "<",
    "up": "^",
}

OPPOSITE_DIRECTION = {
    "right": "left",
    "down": "up",
    "left": "right",
    "up": "down",
}


class ReindeerMaze:
    def __init__(self):
        self.grid = []
        self.reindeer_initial_position = None
        self.reinder_final_position = None
        self.visited_paths = set()

    def reading_reindeer_data(self, file_name):
        for row_index, row in enumerate(FileReader.gen_file_reader(file_name)):
            row_lst = list(row)
            self.grid.append(row_lst)
            for col_index, char in enumerate(row_lst):
                if char == "S":
                    self.reindeer_initial_position = (row_index, col_index)
                if char == "E":
                    self.reinder_final_position = (row_index, col_index)

    def is_move_possible(self, row, col):
        if self.grid[row][col] == "#":
            return False
        return True

    def print_grid(self, grid):
        for row in grid:
            print("".join(str(cell) for cell in row))

    def turn_clockwise_90(self, direction):
        if direction == "right":
            return "down"
        if direction == "down":
            return "left"
        if direction == "left":
            return "up"
        if direction == "up":
            return "right"

    def turn_counter_clockwise_90(self, direction):
        if direction == "right":
            return "up"
        if direction == "up":
            return "left"
        if direction == "left":
            return "down"
        if direction == "down":
            return "right"

    def find_inital_moves(self, row, col):

        direction = "left"
        moves = []
        for direction in POSSIBLE_MOVES:
            move = POSSIBLE_MOVES[direction]
            new_row, new_col = row + move[0], col + move[1]
            if self.is_move_possible(new_row, new_col):
                moves.append((forward_move_cost, (new_row, new_col, direction)))

        return moves

    def get_next_moves(self, node):
        moves = []
        # add forward move
        row, col, direction = node
        # Go forward
        move = POSSIBLE_MOVES[direction]
        new_row, new_col = row + move[0], col + move[1]
        if self.is_move_possible(new_row, new_col):
            moves.append(((new_row, new_col, direction), 1))

        # Turn clockwise
        new_direction = self.turn_clockwise_90(direction)
        move = POSSIBLE_MOVES[new_direction]
        new_row, new_col = row + move[0], col + move[1]
        if self.is_move_possible(new_row, new_col):
            moves.append(((new_row, new_col, new_direction), 1001))

        # Turn counter clockwise
        new_direction = self.turn_counter_clockwise_90(direction)
        move = POSSIBLE_MOVES[new_direction]
        new_row, new_col = row + move[0], col + move[1]
        if self.is_move_possible(new_row, new_col):
            moves.append(((new_row, new_col, new_direction), 1001))

        # Turn around
        new_direction = OPPOSITE_DIRECTION[direction]
        move = POSSIBLE_MOVES[new_direction]
        new_row, new_col = row + move[0], col + move[1]
        if self.is_move_possible(new_row, new_col):
            moves.append(((new_row, new_col, new_direction), 2001))

        return moves

    def path_recovery(self, min_cost, target_node):
        path = []
        current_node = target_node
        robot_initial_position = (self.reindeer_initial_position[0], self.reindeer_initial_position[1], "right")
        while True:
            path.append(current_node)
            current_node = min_cost[current_node][1]
            if current_node == robot_initial_position:
                break
            self.grid[current_node[0]][current_node[1]] = DIRECTION_TO_ARROW[current_node[2]]
        path.append(start_node)

        return path

    def dijkstra_shortest_path(self, start_node, starting_direction, part_two=False):
        start_row, start_col = start_node
        heap = [(0, (start_row, start_col, starting_direction))]  # Start with the source node, cumulative weight is 0
        visited = set()  # Track visited nodes
        min_cost = {}  # Track the minimum cost to each node
        min_cost[(start_row, start_col, starting_direction)] = (0, starting_direction)

        while heap:
            current_weight, current_node = heapq.heappop(heap)
            x, y, direction = current_node

            if current_node in visited:
                continue
            visited.add(current_node)

            # Iterate over neighbors
            for neighbor, edge_weight in self.get_next_moves(current_node):
                # print(f"Neighbor: {neighbor}, edge weight: {edge_weight}")
                if neighbor not in visited:
                    new_weight = current_weight + edge_weight
                    if neighbor in min_cost:
                        if new_weight < min_cost[neighbor][0]:
                            min_cost[neighbor] = (new_weight, current_node)
                            heapq.heappush(heap, (new_weight, neighbor))
                    else:
                        min_cost[neighbor] = (new_weight, current_node)
                        heapq.heappush(heap, (new_weight, neighbor))

        return min_cost


if __name__ == "__main__":
    reindeer_maze = ReindeerMaze()
    reindeer_maze.reading_reindeer_data("day_16.txt")
    start_node = reindeer_maze.reindeer_initial_position
    min_cost = reindeer_maze.dijkstra_shortest_path(start_node, "right")
    # task 1
    min_path = float("inf")
    for key, value in min_cost.items():
        if reindeer_maze.grid[key[0]][key[1]] == "E":
            if value[0] < min_path:
                min_path = value[0]
                target_node = key

    print("Min path: ", min_path)
