from pyvis.network import Network

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for row in file:
                yield row.strip()

edges = []
for row in FileReader.gen_file_reader("day_23.txt"):
    node1, node2 = row.split("-")
    edges.append((node1, node2))

# Create a Pyvis network
net = Network(notebook=True)

# Add edges to the Pyvis graph
for edge in edges:
    net.add_node(edge[0], label=edge[0])  # Add nodes if not already present
    net.add_node(edge[1], label=edge[1])
    net.add_edge(edge[0], edge[1])

# Generate and display the interactive graph
net.show("graph.html")
