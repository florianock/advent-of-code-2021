#!/usr/bin/env python3
import heapq
# noinspection PyUnresolvedReferences
from aocd import data, submit

# --- Day 15: Chiton ---

Graph = dict[(int, int), dict[(int, int), int]]


def main():
    ex1 = solve(example)
    assert ex1 == 40, f"expected 40, but got {ex1}"
    answer1 = solve(data)
    assert answer1 == 720, f"expected 720, but got {answer1}"
    ex2 = solve(example, 5)
    assert ex2 == 315, f"expected 315, but got {ex2}"
    answer2 = solve(data, 5)
    assert answer2 == 3025, f"expected 3025, but got {answer2}"


def solve(inputs: str, multiply: int = 1) -> int:
    graph, values = read_inputs(inputs, multiply)
    bottom_right = (len(values) - 1, len(values[9]) - 1)
    # nodes, shortest_paths = astar(graph, (0, 0), bottom_right)
    nodes, shortest_paths = dijkstra(graph, (0, 0))
    answer = shortest_paths[bottom_right]
    draw_path((0, 0), bottom_right, nodes, values)
    print(f"Path cost: {answer}")
    return answer


def dijkstra(graph: Graph, start: (int, int)):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    came_from = {node: None for node in graph}
    queue = [(0, start)]
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        for next_node, weight in graph[current_node].items():
            distance_temp = current_distance + weight
            if distance_temp < distances[next_node]:
                distances[next_node] = distance_temp
                came_from[next_node] = current_node
                heapq.heappush(queue, (distance_temp, next_node))
    return came_from, distances


def astar(og_graph: Graph, start: (int, int), end: (int, int)) -> (dict[(int, int), (int, int)], dict[(int, int), int]):
    def create_graph(g: Graph, e: (int, int)) -> dict[(int, int), dict[(int, int), [int, int]]]:
        nodes = g.keys()
        result = {}
        for n in nodes:
            result[n] = {m: [w, mh_distance(*m, *e)] for m, w in g[n].items()}
        return result

    def mh_distance(p1, p2, q1, q2):
        return abs(p1 - q1) + abs(p2 - q2)

    graph = create_graph(og_graph, end)
    f_distance = {node: float('inf') for node in graph}
    f_distance[start] = 0
    g_distance = {node: float('inf') for node in graph}
    g_distance[start] = 0
    came_from = {node: None for node in graph}
    came_from[start] = start
    queue = [(0, start)]
    while queue:
        current_f_distance, current_node = heapq.heappop(queue)
        if current_node == end:
            return came_from, f_distance
        for next_node, weights in graph[current_node].items():
            temp_g_distance = g_distance[current_node] + weights[0]
            if temp_g_distance < g_distance[next_node]:
                g_distance[next_node] = temp_g_distance
                heuristic = weights[1]
                f_distance[next_node] = temp_g_distance + heuristic
                came_from[next_node] = current_node
                heapq.heappush(queue, (f_distance[next_node], next_node))
    return came_from, f_distance


def get_neighbors(r: int, c: int, num_rows: int, num_cols: int) -> set[tuple[int, int]]:
    neighbors = {(r + x, c) for x in {-1, 1}} | {(r, c + x) for x in {-1, 1}}
    return {(n, m) for n, m in neighbors if 0 <= n < num_rows and 0 <= m < num_cols}


def read_inputs(inputs: str, multiply: int) -> (Graph, list[list[int]]):
    nums_file = [[int(x) for x in line] for line in inputs.split('\n')]
    num_rows = len(nums_file)
    num_cols = len(nums_file[0])
    nums = [[-1 for x in range(num_rows * multiply)] for y in range(num_cols * multiply)]
    for r, row in enumerate(nums_file):
        for c, val in enumerate(row):
            for m in range(0, multiply):
                for n in range(0, multiply):
                    nums[r + (num_rows * m)][c + (num_cols * n)] = ((val - 1 + 1 * m + 1 * n) % 9) + 1
    graph = Graph()
    for r, row in enumerate(nums):
        for c, _ in enumerate(row):
            graph[(r, c)] = {(i, j): nums[i][j]
                             for (i, j) in get_neighbors(r, c, num_rows * multiply, num_cols * multiply)}
    return graph, nums


def draw_path(start: (int, int),
              end: (int, int),
              previous_nodes: dict[(int, int), (int, int)],
              grid: list[list[int]]):
    c_red = '\033[91m'
    c_end = '\033[0m'
    path = [end]
    node = end
    while node is not start:
        node = previous_nodes[node]
        path.append(node)
        if node == start:
            break
    matrix = ""
    for r, row in enumerate(grid):
        row_string = ""
        for c, cell in enumerate(row):
            if (r, c) in path:
                row_string += c_red + str(cell) + c_end
            else:
                row_string += str(cell)
        row_string += "\n"
        matrix += row_string
    print(matrix)


example = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".strip()

if __name__ == "__main__":
    main()
