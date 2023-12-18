import time
from queue import PriorityQueue
from typing import Tuple, Callable

import numpy as np

EXAMPLE1 = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

EXAMPLE2 = """
111111111111
999999999991
999999999991
999999999991
999999999991
"""

# left: 0, right: 1, up: 2, down: 3, n/a: 4
ORIENTATIONS = [
    {0, 2, 3},
    {1, 2, 3},
    {2, 0, 1},
    {3, 0, 1},
    {0, 1, 2, 3}
]

DISPLACEMENTS = [
    (lambda c: (c[0], c[1] - 1)),
    (lambda c: (c[0], c[1] + 1)),
    (lambda c: (c[0] - 1, c[1])),
    (lambda c: (c[0] + 1, c[1])),
]


def parse_input(text: str) -> np.ndarray:
    grid = []
    for line in text.strip().split("\n"):
        grid.append(list(map(int, line.strip())))

    return np.array(grid)


def can_crucible_run_part1(next_dir: int, last_dir: int, n_last_dir: int) -> bool:
    return n_last_dir < 3 or next_dir != last_dir


def can_crucible_run_part2(next_dir: int, last_dir: int, n_last_dir: int) -> bool:
    if n_last_dir >= 10 and next_dir == last_dir:
        return False
    if n_last_dir < 4 and next_dir != last_dir and last_dir != 4:
        return False
    return True


def can_crucible_stop_part1(current_coords: Tuple[int, int], target_coords: Tuple[int, int], _n_last_dir) -> bool:
    return current_coords == target_coords


def can_crucible_stop_part2(current_coords: Tuple[int, int], target_coords: Tuple[int, int], n_last_dir) -> bool:
    return current_coords == target_coords and n_last_dir >= 4


def find_shortest_distance_dijkstra(
        grid: np.ndarray, start_coords: Tuple[int, int], target_coords: Tuple[int, int], steering_condition: Callable,
        termination_condition: Callable
) -> Tuple[int, np.ndarray]:
    i_max, j_max = grid.shape
    min_candidates = []

    unvisited_nodes = PriorityQueue()
    # Item structure of unvisited_nodes:
    # Tuple(
    #     distance, Tuple(
    #         <node coordinates on the grid>,
    #         <from which direction was the node entered>,
    #         <how many times did the crucible run this direction before in a row>
    #     )
    # )
    unvisited_nodes.put((0, (start_coords, 4, 0)))
    visited_nodes = {}

    while unvisited_nodes.queue:
        current_distance, (current_coords, last_dir, n_last_dir) = unvisited_nodes.get()
        if visited_nodes.get((current_coords, last_dir, n_last_dir)) is not None:
            # Node has already been visited
            continue
        if termination_condition(current_coords, target_coords, n_last_dir):
            min_candidates.append(current_distance)
        for next_dir in ORIENTATIONS[last_dir]:
            if next_dir == last_dir:
                n_curr_dir = n_last_dir + 1
            else:
                n_curr_dir = 1
            # Don't follow the same direction more than three steps
            if steering_condition(next_dir, last_dir, n_last_dir):
                next_coords = DISPLACEMENTS[next_dir](current_coords)
                if visited_nodes.get((next_coords, next_dir, n_curr_dir)) is None:
                    # Node hasn't already been visited
                    if 0 <= next_coords[0] < i_max and 0 <= next_coords[1] < j_max:
                        new_distance = current_distance + grid[next_coords]
                        unvisited_nodes.put((new_distance, (next_coords, next_dir, n_curr_dir)))

        visited_nodes[(current_coords, last_dir, n_last_dir)] = current_distance

    return min(min_candidates)


if __name__ == "__main__":
    with open("../inputs/input17.txt", "r") as fh:
        in_text = fh.read()

    block_grid = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    # noinspection PyTypeChecker
    res = find_shortest_distance_dijkstra(
        block_grid,
        (0, 0),
        tuple(x - 1 for x in block_grid.shape),
        can_crucible_run_part1,
        can_crucible_stop_part1
    )
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    # noinspection PyTypeChecker
    res = find_shortest_distance_dijkstra(
        block_grid,
        (0, 0),
        tuple(x - 1 for x in block_grid.shape),
        can_crucible_run_part2,
        can_crucible_stop_part2
    )
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
