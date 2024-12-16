# https://adventofcode.com/2024/day/13
import heapq


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()


class ClawMachine():
    def __init__(self):
        self.machine_data = []
        self.num_of_possible_moves = 0

    def reading_machine_data(self, file_name):
        points_pattern = r"X\+(\d+),\s*Y\+(\d+)"
        prize_pattern = r"X=(\d+),\s*Y=(\d+)"
        current_equation = {}
        for row in FileReader.gen_file_reader(file_name):
            if not row:
                self.machine_data.append(current_equation)
                current_equation = {}
                continue
            elif row[:8] == "Button A":
                match = re.search(points_pattern, row)
                current_equation["Button_A"] = (int(match.group(1)), int(match.group(2)), 3)
            elif row[:8] == "Button B":
                match = re.search(points_pattern, row)
                current_equation["Button_B"] = (int(match.group(1)), int(match.group(2)), 1)
            elif row[:8] == "Prize: X":
                match = re.search(prize_pattern, row)

                x_prize = int(str(match.group(1)))
                y_prize = int(str(match.group(2)))
                x_prize = 10000000000000 + x_prize
                y_prize = 10000000000000 + y_prize

                current_equation["Prize"] = (x_prize, y_prize)
        else:
            self.machine_data.append(current_equation)

        return self.machine_data
    
    def is_valid_move(self, new_x, new_y, result_x, result_y):
        if new_x > result_x or new_y > result_y:
            return False
        return True

    def get_next_moves(self, current_x, current_y, possible_steps):
        moves = [] 
        for step in possible_steps:
            new_x = current_x + step[0]
            new_y = current_y + step[1]
            
            moves.append(((new_x, new_y), step[2]))

        return moves

    def dijkstra_shortest_path(self, possible_moves, start_node, target):
        # Priority queue: (cumulative_weight, (x, y))
        heap = [(0, start_node)]  # Start with the source node, cumulative weight is 0
        visited = set()  # Track visited nodes
        min_cost = {}  # Track the minimum cost to each node
        min_cost[start_node] = 0

        while heap:
            current_weight, current_node = heapq.heappop(heap)
            x, y = current_node

            # If the node is already visited, skip it
            if current_node in visited:
                continue
            visited.add(current_node)   

            # Check if we reached the target
            #print(f"Current node: {current_node}, target: {target}")
            if x == target[0] and y == target[1]:
                #print(f"Target reached at {current_node} with cost {current_weight}")
                return current_weight


            # Iterate over neighbors
            for neighbor, edge_weight in self.get_next_moves(x, y, possible_moves):
                #print(f"Neighbor: {neighbor}, edge weight: {edge_weight}")
                if neighbor not in visited:
                    new_weight = current_weight + edge_weight
                    if self.is_valid_move(neighbor[0], neighbor[1], target[0], target[1]):
                        if neighbor not in min_cost or new_weight < min_cost[neighbor]:
                            min_cost[neighbor] = new_weight
                            heapq.heappush(heap, (new_weight, neighbor))

        # If the loop ends, the target is unreachable
        print("Target is unreachable.")
        return None


    def get_coins_per_game_simulation(self, possible_steps, start, target):
        ax, ay, cost_a = possible_steps[0]
        bx, by, cost_b = possible_steps[1]
        tx, ty = target
        
        b = (tx*ay-ty*ax)//(ay*bx-by*ax)
        a = (tx*by-ty*bx)//(by*ax-bx*ay)
        if ax*a+bx*b==tx and ay*a+by*b==ty:
            return 3*a+b
        else:
            return 0

    def run_game_simulation(self):
        final_results = []

        for equation in self.machine_data:
            start = (0, 0)
            target = equation["Prize"]
            possible_steps = [equation["Button_A"], equation["Button_B"]]
            
            # Dijkstra
            #coins_needed_dijkstra = self.dijkstra_shortest_path(possible_steps, start, target)
            #if coins_needed_dijkstra is not None:
            #    final_results.append(coins_needed_dijkstra)
            
            coins_needed = self.get_coins_per_game_simulation(possible_steps, start, target)
            final_results.append(coins_needed)
                

        return sum(final_results)


if __name__ == "__main__":
    claw_machine = ClawMachine()
    claw_machine.reading_machine_data("day_13.txt")
    coins_needed_dijkstra = claw_machine.run_game_simulation()
    print("Final Coins needed :", coins_needed_dijkstra)