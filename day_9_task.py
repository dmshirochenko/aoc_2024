# https://adventofcode.com/2024/day/9
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

class DataChank:
    def __init__(self, starting_index, chank_size, file_id=None):
        self.starting_index = starting_index
        self.chank_size = chank_size
        self.file_id = file_id

    def __repr__(self):
        return f"DataChank({self.starting_index}, {self.chank_size}, {self.file_id})"


class DiskFragmenter:
    def __init__(self):
        self.disk_data = []
        self.initial_free_space_index = None
        self.free_space_size = 0
        self.file_chuncks_lst = []
        self.free_space_chuncks_lst = []
        

    def reading_disk_data(self, file_name):
        first_file_num = None
        next_chunk = "file"
        file_id = 0
        for row in FileReader.gen_file_reader(file_name):
            first_file_num = int(row[0])
            for num in row:
                if next_chunk == "file":
                    self.file_chuncks_lst.append(DataChank(len(self.disk_data), int(num), file_id))
                    for i in range(int(num)):
                        self.disk_data.append(file_id)
                    file_id += 1
                    next_chunk = "free_space"
                elif next_chunk == "free_space":
                    self.free_space_chuncks_lst.append(DataChank(len(self.disk_data), int(num)))
                    for i in range(int(num)):
                        self.disk_data.append(".")
                    self.free_space_size += int(num)
                    next_chunk = "file"
        
        self.initial_free_space_index = first_file_num

        #delete first file chuck
        self.file_chuncks_lst.pop(0)
        # revert file chuncks list
        self.file_chuncks_lst = self.file_chuncks_lst[::-1]

        return self.disk_data

    def print_to_file(self, file_name, data):
        with open(file_name, "w") as file:
            file.write(" ,".join(map(str, data)))

    def defragmenting_disk(self):
        left = self.initial_free_space_index
        right = len(self.disk_data) - 1
        disk_data_copy = self.disk_data[:]
        while self.free_space_size > 0 and left < right:
            if disk_data_copy[left] != ".":
                left += 1
                continue
            elif disk_data_copy[right] == ".":
                right -= 1
                continue
            elif disk_data_copy[left] == "." and disk_data_copy[right] != ".":
                disk_data_copy[left], disk_data_copy[right] = disk_data_copy[right], disk_data_copy[left]
                left += 1
                right -= 1
                self.free_space_size -= 1


        return disk_data_copy
    
    def defragmenting_disk_full_file(self):
        disk_data_copy = self.disk_data[:]
        for file_chunk in self.file_chuncks_lst:
            for free_space_chunk in self.free_space_chuncks_lst:
                if free_space_chunk.starting_index > file_chunk.starting_index:
                    break
                if free_space_chunk.chank_size < file_chunk.chank_size:
                    continue
                if free_space_chunk.chank_size == file_chunk.chank_size:
                    for i in range(file_chunk.chank_size):
                        disk_data_copy[free_space_chunk.starting_index + i] = file_chunk.file_id
                        disk_data_copy[file_chunk.starting_index + i] = "."
                    free_space_chunk.chank_size = 0
                    break
                if free_space_chunk.chank_size > file_chunk.chank_size:
                    for i in range(file_chunk.chank_size):
                        disk_data_copy[free_space_chunk.starting_index + i] = file_chunk.file_id
                        disk_data_copy[file_chunk.starting_index + i] = "."
                    free_space_chunk.chank_size -= file_chunk.chank_size
                    free_space_chunk.starting_index += file_chunk.chank_size
                    break
        
        return disk_data_copy

    def count_new_disk_check_sum(self, disk_data_copy):
        check_sum = 0
        for index, num in enumerate(disk_data_copy):
            if num == ".":
                continue
            check_sum += num * index
        
        return check_sum


if __name__ == "__main__":
    disk_fragmenter = DiskFragmenter()
    disk_data = disk_fragmenter.reading_disk_data("day_9.txt")
    disk_data_copy = disk_fragmenter.defragmenting_disk()
    check_sum = disk_fragmenter.count_new_disk_check_sum(disk_data_copy)
    #task 1
    print("check sum: ", check_sum)
    #task 2
    disk_data_copy_2 = disk_fragmenter.defragmenting_disk_full_file()
    check_sum_task_2 = disk_fragmenter.count_new_disk_check_sum(disk_data_copy_2)
    print("check sum task 2: ", check_sum_task_2)