# https://adventofcode.com/2024/day/2


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class NuclearFusionChecker():
    def __init__(self):
        pass

    def reading_fusion_data(self, file_name):
        fusion_data = []
        for row in FileReader.gen_file_reader(file_name):
            report = [int(num) for num in row.split(" ")]
            fusion_data.append(report)

        return fusion_data

    def is_always_increasing_by_one_or_two_three(self, report):
        for i in range(1, len(report)):
            if report[i] - report[i - 1] not in [1, 2, 3]:
                return False
        
        return True

    def is_always_decreasing_by_one_or_two_three(self, report):
        for i in range(1, len(report)):
            if report[i - 1] - report[i] not in [1, 2, 3]:
                return False
        
        return True

    def is_always_increasing_by_one_or_two_three_with_index_return(self, report):
        for i in range(1, len(report)):
            if report[i] - report[i - 1] not in [1, 2, 3]:
                return i-1, i
        
        return -1, -1
    
    def is_always_decreasing_by_one_or_two_three_with_index_return(self, report):
        for i in range(1, len(report)):
            if report[i - 1] - report[i] not in [1, 2, 3]:
                return i-1, i
        
        return -1, -1
    
    def is_always_increasing_by_one_or_two_three_with_skip(self, report):
        #report copy
        left, right = self.is_always_increasing_by_one_or_two_three_with_index_return(report)
        if left != -1:
            if self.is_always_increasing_by_one_or_two_three(report[:left] + report[left+1:]):
                return True
            if self.is_always_increasing_by_one_or_two_three(report[:right] + report[right+1:]):
                return True
        else:
            return True
        
        return False
    
        
    def is_always_decreasing_by_one_or_two_three_with_skip(self, report):
        left, right = self.is_always_decreasing_by_one_or_two_three_with_index_return(report)
        if left != -1:
            if self.is_always_decreasing_by_one_or_two_three(report[:left] + report[left+1:]):
                return True
            if self.is_always_decreasing_by_one_or_two_three(report[:right] + report[right+1:]):
                return True
        else:
            return True
        
        return False
    
    def all_increasing_decreasing_by_one_or_two_three(self, fusion_data):
        num_of_safe_reports = 0
        
        for report in fusion_data:
            if self.is_always_increasing_by_one_or_two_three(report) or self.is_always_decreasing_by_one_or_two_three(report):
                num_of_safe_reports += 1

        return num_of_safe_reports

    def all_increasing_decreasing_by_one_or_two_or_three_with_skip(self, fusion_data):
        num_of_safe_reports = 0
        
        for report in fusion_data:
            if self.is_always_increasing_by_one_or_two_three_with_skip(report) or self.is_always_decreasing_by_one_or_two_three_with_skip(report):
                num_of_safe_reports += 1

        return num_of_safe_reports

if "__main__" == __name__:
    fusion_checker = NuclearFusionChecker()
    fusion_data = fusion_checker.reading_fusion_data("day_2.txt")
    num_of_safe_reports = fusion_checker.all_increasing_decreasing_by_one_or_two_three(fusion_data)
    #task 1
    print("number of safe reports: ", num_of_safe_reports)
    #task 2
    num_of_safe_reports_with_skip = fusion_checker.all_increasing_decreasing_by_one_or_two_or_three_with_skip(fusion_data)
    print("number of safe reports with skip: ", num_of_safe_reports_with_skip)