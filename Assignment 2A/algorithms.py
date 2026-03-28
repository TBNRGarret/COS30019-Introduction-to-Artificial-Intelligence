from collections import deque
import heapq
import math


class SearchNode:
    # Represents a node in the search tree with state, parent, cost, and depth.
    def __init__(self, state, parent=None, g_cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.g_cost = g_cost
        self.depth = depth

    def extract_path(self):
        # Backtracks from the current node to the start to return the full path.
        path = []
        current = self
        while current is not None:
            path.append(current.state)
            current = current.parent
        path.reverse()
        return path


# ---------------------------
# BFS
# ---------------------------
def bfs(problem):
    frontier = deque()
    visited = set()

    start = SearchNode(problem.origin)
    frontier.append(start)

    node_count = 1  # count created nodes

    while frontier:
        node = frontier.popleft()

        if node.state in problem.destinations:
            return node, node_count

        visited.add(node.state)

        for neighbor, cost in sorted(problem.adjacency[node.state]):
            if neighbor not in visited:
                child = SearchNode(
                    state=neighbor,
                    parent=node,
                    g_cost=node.g_cost + cost,
                    depth=node.depth + 1
                )
                frontier.append(child)
                node_count += 1

    return None, node_count


# ---------------------------
# DFS
# ---------------------------
def dfs(problem):
    stack = []
    visited = set()

    start = SearchNode(problem.origin)
    stack.append(start)

    node_count = 1

    while stack:
        node = stack.pop()

        if node.state in problem.destinations:
            return node, node_count

        if node.state not in visited:
            visited.add(node.state)

            for neighbor, cost in sorted(problem.adjacency[node.state], reverse=True):
                if neighbor not in visited:
                    child = SearchNode(
                        state=neighbor,
                        parent=node,
                        g_cost=node.g_cost + cost,
                        depth=node.depth + 1
                    )
                    stack.append(child)
                    node_count += 1

    return None, node_count

# ---------------------------
# GBFS
# ---------------------------

def heuristic(state, problem):
    # Calculates the Euclidean distance from the current node to the closest destination node.
    if state not in problem.nodes:
        return 0
    x1, y1 = problem.nodes[state]
    min_dist = float('inf')
    for dest in problem.destinations:
        if dest in problem.nodes:
            x2, y2 = problem.nodes[dest]
            dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            if dist < min_dist:
                min_dist = dist
    return min_dist

def gbfs(problem):
    # Implements Greedy Best-First Search using a priority queue to expand nodes with the lowest heuristic cost.
    counter = 0
    start_node = SearchNode(problem.origin)
    h_start = heuristic(problem.origin, problem)
    frontier = []
    heapq.heappush(frontier, (h_start, problem.origin, counter, start_node))
    visited = set()
    node_count = 1

    while frontier:
        h, state_id, c, node = heapq.heappop(frontier)
        if node.state in problem.destinations:
            return node, node_count
        if node.state not in visited:
            visited.add(node.state)
            for neighbor, cost in sorted(problem.adjacency.get(node.state, [])):
                if neighbor not in visited:
                    counter += 1
                    child = SearchNode(neighbor, node, node.g_cost + cost, node.depth + 1)
                    h_child = heuristic(neighbor, problem)
                    heapq.heappush(frontier, (h_child, neighbor, counter, child))
                    node_count += 1
    return None, node_count

# ---------------------------
# A* 
# ---------------------------

def astar(problem):
    frontier = []
    visited = {}

    start = SearchNode(problem.origin)
    heapq.heappush(frontier, (0, 0, start))

    node_count = 1
    tie_break = 0

    def heuristic(state):
        x1, y1 = problem.nodes[state]
        return min(
            math.sqrt((x1 - problem.nodes[g][0])**2 +
                      (y1 - problem.nodes[g][1])**2)
            for g in problem.destinations
        )

    while frontier:
        f, _, node = heapq.heappop(frontier)

        if node.state in problem.destinations:
            return node, node_count

        if node.state in visited and visited[node.state] <= node.g_cost:
            continue

        visited[node.state] = node.g_cost

        for neighbor, cost in sorted(problem.adjacency[node.state]):
            new_g = node.g_cost + cost
            child = SearchNode(
                state=neighbor,
                parent=node,
                g_cost=new_g,
                depth=node.depth + 1
            )

            h = heuristic(neighbor)
            new_f = new_g + h

            tie_break += 1
            heapq.heappush(frontier, (new_f, tie_break, child))
            node_count += 1

    return None, node_count


# ---------------------------
# CUS1: Iterative Deepening Depth-First Search (IDDFS)
# ---------------------------

def cus1(problem):
    """
    Custom Uninformed Search 1 (CUS1) using Iterative Deepening Search (IDS).
    It repeatedly runs Depth-Limited Search (DLS) with an increasing depth limit.
    Returns the goal node and the total number of generated nodes.
    """
    depth_limit = 0
    total_node_count = 0

    while True:
        # Perform a depth-limited search with the current limit
        result_node, count, cutoff_occurred = depth_limited_search(problem, depth_limit)
        total_node_count += count

        # If the goal is found, return the node and the cumulative node count
        if result_node is not None:
            return result_node, total_node_count

        # If the search explored all reachable nodes without hitting the depth limit,
        # it means the entire state space has been explored and the goal is unreachable.
        # This prevents an infinite loop (e.g., when there are no edges to the goal).
        if not cutoff_occurred:
            return None, total_node_count

        # Otherwise, increase the depth limit and try again
        depth_limit += 1


def depth_limited_search(problem, limit):
    """
    Performs a Depth-First Search up to a specific depth limit.
    Returns a tuple: (goal_node, nodes_generated, cutoff_occurred)
    """
    stack = []
    start = SearchNode(problem.origin, depth=0)
    stack.append(start)

    node_count = 1  # The start node is created
    cutoff_occurred = False  # Flag to track if any path was cut off by the depth limit

    while stack:
        node = stack.pop()

        # Goal test
        if node.state in problem.destinations:
            return node, node_count, False

        # If the current node is exactly at the depth limit, we do not expand it.
        # However, we must check if it has unvisited neighbors to determine if a cutoff happened.
        if node.depth == limit:
            # Use .get() to prevent KeyError if the node has no outgoing edges
            neighbors = problem.adjacency.get(node.state, [])
            for neighbor, _ in neighbors:
                if not in_path(node, neighbor):
                    cutoff_occurred = True
                    break  # No need to check other neighbors if one cutoff is detected
        else:
            # Expand children if the current depth is strictly less than the limit.
            # Sort in reverse order so that smaller nodes are placed near the top of the stack.
            # This ensures they are popped and expanded first (satisfying assignment's tie-breaking rule).
            neighbors = sorted(problem.adjacency.get(node.state, []), reverse=True)

            for neighbor, cost in neighbors:
                # Prevent cycles by avoiding states already in the current path
                if not in_path(node, neighbor):
                    child = SearchNode(
                        state=neighbor,
                        parent=node,
                        g_cost=node.g_cost + cost,
                        depth=node.depth + 1
                    )
                    stack.append(child)
                    node_count += 1

    # Goal not found within this depth limit
    return None, node_count, cutoff_occurred


def in_path(node, state):
    """
    Checks if a state is already in the current path from the root.
    Used to prevent cycles in tree-based search environments.
    """
    current = node
    while current is not None:
        if current.state == state:
            return True
        current = current.parent
    return False

# ---------------------------
# CUS2 
# ---------------------------

def cus2(problem):
    """
    Step-based A* search.
    g(n) = depth (number of moves)
    h(n) = Euclidean distance to the closest goal
    f(n) = depth + heuristic

    This guarantees the shortest path in terms of number of moves
    when the heuristic does not overestimate the remaining moves.
    """

    frontier = []
    counter = 0  # ensures stable tie-breaking (insertion order)

    # Create root node
    start = SearchNode(problem.origin, parent=None, g_cost=0, depth=0)

    h = euclidean(problem, start.state, problem.destinations)

    # Priority tuple:
    # (f value, state id, insertion order, node object)
    heapq.heappush(frontier, (h, start.state, counter, start))

    node_count = 1
    counter += 1

    while frontier:
        _, _, _, node = heapq.heappop(frontier)

        # Goal test
        if node.state in problem.destinations:
            return node, node_count

        # Expand neighbors in ascending order (NOTE 2 requirement)
        neighbors = sorted(problem.adjacency[node.state])

        for neighbor, cost in neighbors:

            # Path-checking to prevent cycles (tree-based search)
            if not in_path(node, neighbor):

                child = SearchNode(
                    state=neighbor,
                    parent=node,
                    g_cost=node.g_cost + cost,
                    depth=node.depth + 1
                )

                h = euclidean(problem, neighbor, problem.destinations)
                f = child.depth + h

                heapq.heappush(frontier, (f, neighbor, counter, child))

                node_count += 1
                counter += 1

    return None, node_count


def euclidean(problem, state, goals):
    """
    Returns the minimum Euclidean distance
    from the current state to any goal state.
    """

    x1, y1 = problem.nodes[state]

    min_h = float("inf")
    for g in goals:
        x2, y2 = problem.nodes[g]
        h = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        min_h = min(min_h, h)

    return min_h