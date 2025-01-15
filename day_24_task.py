# https://adventofcode.com/2024/day/24
from collections import deque


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class Wire:
    def __init__(self, wire_name, wire_value):
        self.wire_name = wire_name
        self.wire_value = wire_value
        self.wire_neighbours_lst = []

    def add_neighbour(self, neighbour, operation, wire_output):
        self.wire_neighbours_lst.append((neighbour, operation, wire_output))

    def __repr__(self):
        return f"Wire node {self.wire_name}: {self.wire_value}"


class CrossedWires:
    def __init__(self):
        self.wires_graph = dict()
        self.all_signals_lst = []
        self.operations = {"AND": self.and_gate, "OR": self.or_gate, "XOR": self.xor_gate}

    @staticmethod
    def and_gate(a, b):
        return a & b

    @staticmethod
    def or_gate(a, b):
        return a | b

    @staticmethod
    def xor_gate(a, b):
        return a ^ b

    def read_file_data(self, file_name):
        is_wire_definition = True
        num_of_operations = 0
        for row in FileReader.gen_file_reader(file_name):
            if row == "":
                is_wire_definition = False
                continue

            if is_wire_definition:
                wire_name, wire_value = row.split(": ")
                self.wires_graph[wire_name] = Wire(wire_name, int(wire_value))
            else:
                num_of_operations += 1
                wire_equasion, wire_output = row.split(" -> ")
                wire_name, operation, neighbour = wire_equasion.split(" ")

                if wire_name not in self.wires_graph:
                    self.wires_graph[wire_name] = Wire(wire_name, None)
                if neighbour not in self.wires_graph:
                    self.wires_graph[neighbour] = Wire(neighbour, None)
                if wire_output not in self.wires_graph:
                    self.wires_graph[wire_output] = Wire(wire_output, None)

                wire_node = self.wires_graph[wire_name]
                neighbour_node = self.wires_graph[neighbour]
                wire_output_node = self.wires_graph[wire_output]

                wire_node.add_neighbour(neighbour_node, operation, wire_output_node)
                self.all_signals_lst.append((wire_node, neighbour_node, operation, wire_output_node))

        print("Number of operations:", num_of_operations)
        return self.wires_graph

    def signal_simulation(self):
        seen_operations = set()
        while self.all_signals_lst:
            wire_node, neighbour_node, operation, wire_output_node = self.all_signals_lst.pop(0)

            if (
                wire_node.wire_name,
                neighbour_node.wire_name,
                operation,
                wire_output_node.wire_name,
            ) in seen_operations:
                continue

            if wire_node.wire_value is not None and neighbour_node.wire_value is not None:
                print(wire_node, neighbour_node, operation, wire_output_node)
                seen_operations.add(
                    (wire_node.wire_name, neighbour_node.wire_name, operation, wire_output_node.wire_name)
                )
                wire_output_node.wire_value = self.operations[operation](
                    wire_node.wire_value, neighbour_node.wire_value
                )
            else:
                self.all_signals_lst.append((wire_node, neighbour_node, operation, wire_output_node))

        z_letters_lst = []
        for wire_name, wire_node in self.wires_graph.items():
            if wire_node.wire_name[0] == "z":
                z_letters_lst.append((wire_name, wire_node.wire_value))

        z_letters_lst.sort(key=lambda x: x[0], reverse=True)
        # return value string representation
        return "".join([str(z[1]) for z in z_letters_lst])


if __name__ == "__main__":
    cross_wires = CrossedWires()
    cross_wires.read_file_data("day_24.txt")
    z_values_str = cross_wires.signal_simulation()
    # from st byites to decimal
    print("Value of wire a:", int(z_values_str, 2))
