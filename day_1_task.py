# https://adventofcode.com/2024/day/1


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class HistorianLocator:
    def __init__(self):
        pass

    def location_id_reader(self, file_name):
        locations_lst_1 = []
        locations_lst_2 = []
        for row in FileReader.gen_file_reader(file_name):
            loc_1, loc_2 = row.split("   ")
            locations_lst_1.append(loc_1)
            locations_lst_2.append(loc_2)

        locations_lst_1.sort()
        locations_lst_2.sort()

        return locations_lst_1, locations_lst_2

    def sum_of_locations_diff(self, locations_1, locations_2):
        sum_diff = 0
        for loc_1, loc_2 in zip(locations_1, locations_2):
            sum_diff += abs(int(loc_1) - int(loc_2))

        return sum_diff

    def hash_map_of_locations(self, locations):
        locations_dict = {}
        for loc in locations:
            if loc in locations_dict:
                locations_dict[loc] += 1
            else:
                locations_dict[loc] = 1

        return locations_dict

    def find_common_locations(self, locations_1, locations_2):
        sum_of_common_locations = 0
        locations_dict_2 = self.hash_map_of_locations(locations_2)

        for loc in locations_1:
            if loc in locations_dict_2:
                sum_of_common_locations += int(loc) * locations_dict_2[loc]

        return sum_of_common_locations


if __name__ == "__main__":
    locator = HistorianLocator()
    locations_1, locations_2 = locator.location_id_reader("day_1.txt")
    sum_diff = locator.sum_of_locations_diff(locations_1, locations_2)
    # task 1
    print("sum of locations diff: ", sum_diff)
    # task 2
    sum_common = locator.find_common_locations(locations_1, locations_2)
    print("sum of common locations: ", sum_common)
