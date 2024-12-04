# https://adventofcode.com/2024/day/4
import re
from collections import deque

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()

possible_xmas_set = {"X", "M", "A", "S"}

possible_directions = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
    "up_left": (-1, -1),
    "up_right": (-1, 1),
    "down_left": (1, -1),
    "down_right": (1, 1),
}

class CeresSearch:
    def __init__(self):
        pass

    def reading_ceres_data(self, file_name):
        ceres_data = []
        for row in FileReader.gen_file_reader(file_name):
            line = []
            for char in row:
                if char not in possible_xmas_set:
                    line.append(".")
                else:
                    line.append(char)
            ceres_data.append(line)

        return ceres_data

    def possible_moves_in_grid_for_bfs(self, ceres_data, row, col):
        # moves wit directions
        moves = []
        if row - 1 >= 0:
            moves.append((row - 1, col))
        if row + 1 < len(ceres_data):
            moves.append((row + 1, col))
        if col - 1 >= 0:
            moves.append((row, col - 1))
        if col + 1 < len(ceres_data[0]):
            moves.append((row, col + 1))
        #diagonal moves
        if row - 1 >= 0 and col - 1 >= 0:
            moves.append((row - 1, col - 1))
        if row - 1 >= 0 and col + 1 < len(ceres_data[0]):
            moves.append((row - 1, col + 1))
        if row + 1 < len(ceres_data) and col - 1 >= 0:
            moves.append((row + 1, col - 1))
        if row + 1 < len(ceres_data) and col + 1 < len(ceres_data[0]):
            moves.append((row + 1, col + 1))

        return moves

    def define_direction(self, row, col, prev_row, prev_col):
        if row < prev_row and col == prev_col:
            return "up"
        elif row > prev_row and col == prev_col:
            return "down"
        elif row == prev_row and col < prev_col:
            return "left"
        elif row == prev_row and col > prev_col:
            return "right"
        elif row < prev_row and col < prev_col:
            return "up_left"
        elif row < prev_row and col > prev_col:
            return "up_right"
        elif row > prev_row and col < prev_col:
            return "down_left"
        elif row > prev_row and col > prev_col:
            return "down_right"

        return None

    def check_if_prev_chat_is_valid(self, prev_char, current_char):
        # X -> M -> A -> S    
        if prev_char == "X" and current_char == "M":
            return True
        if prev_char == "M" and current_char == "A":
            return True
        if prev_char == "A" and current_char == "S":
            return True
        
        return False


    def xmas_word_search(self, row, col, ceres_data):
        count_xmas_words = 0

        for direction, (dr, dc) in possible_directions.items():
            word = "X"
            current_row, current_col = row, col
            
            while True:
                # Calculate the next move
                next_row, next_col = current_row + dr, current_col + dc
                
                # Check if the move is within the grid and valid
                if (next_row, next_col) in self.possible_moves_in_grid_for_bfs(ceres_data, current_row, current_col):
                    prev_char = ceres_data[current_row][current_col]
                    new_char = ceres_data[next_row][next_col]

                    # Validate the transition from prev_char to new_char
                    if self.check_if_prev_chat_is_valid(prev_char, new_char):
                        print(prev_char, new_char)
                        word += new_char
                        
                        # Check if we have found "XMAS"
                        if word == "XMAS":
                            print("Found word:", word)
                            count_xmas_words += 1
                            break
                        
                        # Move to the next position
                        current_row, current_col = next_row, next_col
                    else:
                        break
                else:
                    break

        return count_xmas_words


    def count_xmas_words(self, ceres_data):
        count_xmas_words = 0

        for row in range(len(ceres_data)):
            for col in range(len(ceres_data[0])):
                if ceres_data[row][col] == "X":
                    count_xmas_words += self.xmas_word_search(row, col, ceres_data)

        return count_xmas_words
    
    def print_path(self, ceres_data, path):
        for row in range(len(ceres_data)):
            for col in range(len(ceres_data[0])):
                if (row, col) in path:
                    print(ceres_data[row][col], end="")
                else:
                    print(".", end="")
            print()
        print()

    def sort_by_row_then_col(self, coord_lst):
        # Sort by row (x[0]), then by column (x[1])
        coord_lst.sort(key=lambda x: (x[0], x[1]))
        return coord_lst


    def xmas_pattern_search(self, row, col, ceres_data):
        """
        Searches for the Xmas pattern:
        M.S
        .A.
        M.S
        """
        count_xmas_words = 0

        # check that from A we can find 2 M on the left and 2 S on the right
        if col - 1 >= 0 and col + 1 < len(ceres_data[0]) and row - 1 >= 0 and row + 1 < len(ceres_data):
            if ceres_data[row][col] == "A" and ceres_data[row - 1][col - 1] == "M" and ceres_data[row + 1][col - 1] == "M":
                if ceres_data[row + 1][col + 1] == "S" and ceres_data[row - 1][col + 1] == "S":
                    count_xmas_words += 1
        
        # check that from A we can find 2 M on the right and 2 S on the left
        if col - 1 >= 0 and col + 1 < len(ceres_data[0]) and row - 1 >= 0 and row + 1 < len(ceres_data):
            if ceres_data[row][col] == "A" and ceres_data[row - 1][col + 1] == "M" and ceres_data[row + 1][col + 1] == "M":
                if ceres_data[row + 1][col - 1] == "S" and ceres_data[row - 1][col - 1] == "S":
                    count_xmas_words += 1
        
        # check that from A we can find 2 S on the top and 2 M on the bottom
        if col - 1 >= 0 and col + 1 < len(ceres_data[0]) and row - 1 >= 0 and row + 1 < len(ceres_data):
            if ceres_data[row][col] == "A" and ceres_data[row - 1][col - 1] == "S" and ceres_data[row - 1][col + 1] == "S":
                if ceres_data[row + 1][col + 1] == "M" and ceres_data[row + 1][col - 1] == "M":
                    count_xmas_words += 1

        # check that from A we can find 2 S on the bottom and 2 M on the top
        if col - 1 >= 0 and col + 1 < len(ceres_data[0]) and row - 1 >= 0 and row + 1 < len(ceres_data):
            if ceres_data[row][col] == "A" and ceres_data[row + 1][col - 1] == "S" and ceres_data[row + 1][col + 1] == "S":
                if ceres_data[row - 1][col + 1] == "M" and ceres_data[row - 1][col - 1] == "M":
                    count_xmas_words += 1


        return count_xmas_words



    def count_xmas_patterns(self, ceres_data):
        count_xmas_words = 0
        known_patterns = set()
        for row in range(len(ceres_data)):
            for col in range(len(ceres_data[0])):
                if ceres_data[row][col] == "A":
                    count_xmas_words += self.xmas_pattern_search(row, col, ceres_data)

        return count_xmas_words

if __name__ == "__main__":
    ceres_search = CeresSearch()
    ceres_data = ceres_search.reading_ceres_data("day_4.txt")
    #task 1
    print(ceres_search.count_xmas_words(ceres_data))
    #task 2
    print(ceres_search.count_xmas_patterns(ceres_data))

