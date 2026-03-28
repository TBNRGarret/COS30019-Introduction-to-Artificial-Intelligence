class Problem:
    def __init__(self):
        self.nodes = {}          # {node_id: (x, y)}
        self.adjacency = {}      # {node_id: [(neighbor, cost)]}
        self.origin = None
        self.destinations = set()


def parse_problem(filename):
    problem = Problem()

    section = None

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("Nodes:"):
                section = "nodes"
                continue
            elif line.startswith("Edges:"):
                section = "edges"
                continue
            elif line.startswith("Origin:"):
                section = "origin"
                continue
            elif line.startswith("Destinations:"):
                section = "destinations"
                continue

            if section == "nodes":
                node_id, coords = line.split(":")
                node_id = int(node_id.strip())
                coords = coords.strip()[1:-1]  # remove ()
                x, y = map(int, coords.split(","))
                problem.nodes[node_id] = (x, y)
                problem.adjacency[node_id] = []

            elif section == "edges":
                left, cost = line.split(":")
                cost = int(cost.strip())
                left = left.strip()[1:-1]  # remove ()
                n1, n2 = map(int, left.split(","))
                problem.adjacency[n1].append((n2, cost))

            elif section == "origin":
                problem.origin = int(line.strip())

            elif section == "destinations":
                parts = line.split(";")
                for p in parts:
                    problem.destinations.add(int(p.strip()))

    return problem