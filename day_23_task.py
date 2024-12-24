# https://adventofcode.com/2024/day/23
from itertools import combinations


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class LanParty:
    def __init__(self):
        self.network_dct = dict()
        self.all_networks_lst = []

    def read_file_data(self, file_name):
        for row in FileReader.gen_file_reader(file_name):
            machine_1, machine_2 = row.strip().split("-")
            if machine_1 not in self.network_dct:
                self.network_dct[machine_1] = set()
                self.network_dct[machine_1].add(machine_2)
                self.network_dct[machine_1].add(machine_1)
            else:
                self.network_dct[machine_1].add(machine_2)

            if machine_2 not in self.network_dct:
                self.network_dct[machine_2] = set()
                self.network_dct[machine_2].add(machine_1)
                self.network_dct[machine_2].add(machine_2)
            else:
                self.network_dct[machine_2].add(machine_1)

    def count_networks_with_n_machines_starts_with_letter(self, n, letter):
        count = 0
        seen_networks = set()
        for inital_key, machines in self.network_dct.items():
            for neighbor in machines:
                for second_neighbor in self.network_dct[neighbor]:
                    for third_neighbor in self.network_dct[second_neighbor]:
                        if third_neighbor == inital_key:
                            current_mesh_set = set([inital_key, neighbor, second_neighbor])
                            if len(current_mesh_set) == n:
                                current_mesh_set_to_sorted_tuple = tuple(sorted(current_mesh_set))
                                seen_networks.add(current_mesh_set_to_sorted_tuple)

        for network in seen_networks:
            for machine in network:
                if machine.startswith(letter):
                    count += 1
                    break

        return count

    def get_all_connected_networks(self):
        all_connected_networks_lst = []
        for key, machines in self.network_dct.items():
            connected_to_key_node_pack = []
            connected_to_key_node_pack.append(self.network_dct[key])
            for machine in machines:
                if machine != key:
                    connected_to_key_node_pack.append(self.network_dct[machine])

            all_connected_networks_lst.append(connected_to_key_node_pack)

        return all_connected_networks_lst

    def get_max_len_of_connected_network(self, all_connected_networks_lst):
        max_len_of_all_connected_networks = 3
        max_connected_network = None
        for network in all_connected_networks_lst:
            initial_set = set.intersection(*network)

            if len(initial_set) > max_len_of_all_connected_networks:
                max_len_of_all_connected_networks = len(initial_set)
                max_connected_network = initial_set
            else:
                perm_factor = len(network) - 1
                while perm_factor > max_len_of_all_connected_networks:
                    for perm in combinations(network, perm_factor):
                        perm_intersection = set.intersection(*perm)
                        if len(perm_intersection) > max_len_of_all_connected_networks:
                            max_len_of_all_connected_networks = len(perm_intersection)
                            max_connected_network = perm_intersection
                    perm_factor -= 1

        return max_connected_network

    def sort_and_join(self, max_connected_network):
        """set to list to string sorted ialphabetically and joined ,"""
        max_connected_network_lst = list(max_connected_network)
        max_connected_network_lst.sort()
        return ",".join(max_connected_network_lst)


if __name__ == "__main__":
    lan_party = LanParty()
    lan_party.read_file_data("day_23.txt")
    # task 1
    count = lan_party.count_networks_with_n_machines_starts_with_letter(3, "t")
    print("Task 1 Count of networks with 3 machines that start with letter t:", count)
    # task 2
    all_connected_networks_lst = lan_party.get_all_connected_networks()
    max_connected_network = lan_party.get_max_len_of_connected_network(all_connected_networks_lst)
    result = lan_party.sort_and_join(max_connected_network)
    print("Task 2 password is :", result)
