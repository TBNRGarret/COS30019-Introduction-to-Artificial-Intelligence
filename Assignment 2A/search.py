import sys
from parser import parse_problem
import algorithms


def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        return

    filename = sys.argv[1]
    method = sys.argv[2].lower()

    # Parse problem file
    try:
        problem = parse_problem(filename)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Select algorithm
    if method == "dfs":
        result = algorithms.dfs(problem)
    elif method == "bfs":
        result = algorithms.bfs(problem)
    elif method == "gbfs":
        result = algorithms.gbfs(problem)
    elif method == "astar":
        result = algorithms.astar(problem)
    elif method == "cus1":
        result = algorithms.cus1(problem)
    elif method == "cus2":
        result = algorithms.cus2(problem)
    else:
        print("Unknown method.")
        return

    goal_node, node_count = result

    if goal_node is None:
        print(f"{filename} {method}")
        print("No solution found")
        return

    path = goal_node.extract_path()

    # Required output format
    print(f"Filename: {filename} Method: {method}")
    print(f"Goal: {goal_node.state} Nodes: {node_count}")
    print("Path:", " ".join(map(str, path)))


if __name__ == "__main__":
    main()