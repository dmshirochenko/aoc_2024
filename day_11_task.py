# https://adventofcode.com/2024/day/11


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class StonesMover:
    def __init__(self):
        self.stones_data = []
        self.stones_data_reorderded = []
        self.stones_data_dct = {}

    def reading_stones_data(self, file_name):
        for row in FileReader.gen_file_reader(file_name):
            self.stones_data = [(int(num), True) for num in row.split(" ")]
            for char in row.split(" "):
                if char in self.stones_data_dct:
                    self.stones_data_dct[int(char)] += 1
                else:
                    self.stones_data_dct[int(char)] = 1

        return self.stones_data

    def move_stone(self, num):
        len_of_num = len(str(num))
        if num == 0:
            return 1, None
        elif len_of_num % 2 == 0:
            len_to_cut = len(str(num)) // 2
            num_1 = int(str(num)[:len_to_cut])
            num_2 = int(str(num)[len_to_cut:])
            return num_1, num_2
        else:
            return num * 2024, None

    def reorder_stones_with_dct(self, num_of_moves):
        while num_of_moves > 0:
            data_to_append = []
            num_of_moves -= 1
            for key, value in self.stones_data_dct.items():
                if value != 0:
                    num_1, num_2 = self.move_stone(key)
                    if num_2 is None:
                        data_to_append.append((key, value, "del"))
                        data_to_append.append((num_1, value, "add"))
                    else:
                        data_to_append.append((key, value, "del"))
                        data_to_append.append((num_1, value, "add"))
                        data_to_append.append((num_2, value, "add"))

            for key, value, action in data_to_append:
                if action == "add":
                    if key in self.stones_data_dct:
                        self.stones_data_dct[key] += value
                    else:
                        self.stones_data_dct[key] = value
                else:
                    if value > self.stones_data_dct[key]:
                        self.stones_data_dct[key] = 0
                    else:
                        self.stones_data_dct[key] -= value

        # count stones
        keys_to_remove = []
        count_stones = 0
        for key, value in self.stones_data_dct.items():
            if value != 0:
                count_stones += value
            else:
                keys_to_remove.append(key)

        return count_stones


if __name__ == "__main__":
    stones_mover = StonesMover()
    stones_data = stones_mover.reading_stones_data("day_11.txt")
    print(stones_mover.stones_data_dct)
    result = stones_mover.reorder_stones_with_dct(num_of_moves=75)
    print("result ", result)
