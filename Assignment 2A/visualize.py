import sys
import matplotlib.pyplot as plt
from parser import parse_problem


def draw_graph(problem, highlight_path=None):
    """
    problem: đối tượng Problem từ parser
    highlight_path: list các node id nếu muốn tô đậm một đường đi
    """

    plt.figure(figsize=(8, 6))

    # --- Vẽ nodes ---
    for node_id, (x, y) in problem.nodes.items():
        plt.scatter(x, y, s=500)
        plt.text(x, y, str(node_id),
                 ha='center', va='center',
                 color='white', weight='bold')

    # --- Vẽ edges ---
    for u in problem.adjacency:
        x1, y1 = problem.nodes[u]

        for v, cost in problem.adjacency[u]:
            x2, y2 = problem.nodes[v]

            # kiểm tra xem cạnh có thuộc path cần highlight không
            is_highlight = False
            if highlight_path:
                for i in range(len(highlight_path) - 1):
                    if highlight_path[i] == u and highlight_path[i + 1] == v:
                        is_highlight = True
                        break

            dx = x2 - x1
            dy = y2 - y1

            plt.arrow(
                x1, y1,
                dx, dy,
                length_includes_head=True,
                head_width=0.15,
                alpha=0.7 if not is_highlight else 1.0,
                linewidth=1 if not is_highlight else 3
            )

            # ghi cost ở giữa cạnh
            plt.text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                str(cost),
                fontsize=18,
                color='red'
            )

    plt.title("Route Finding Graph")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <filename>")
        return

    filename = sys.argv[1]
    problem = parse_problem(filename)

    draw_graph(problem)


if __name__ == "__main__":
    main()