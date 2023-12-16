import time
from typing import Tuple, Dict, List

import numpy as np

EXAMPLE1 = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

ORIENTATIONS = {
    "u": {"|": "u", "\\": "l", "/": "r", ".": "u"},
    "d": {"|": "d", "\\": "r", "/": "l", ".": "d"},
    "l": {"-": "l", "\\": "u", "/": "d", ".": "l"},
    "r": {"-": "r", "\\": "d", "/": "u", ".": "r"},
}

DISPLACEMENTS = {
    "u": (lambda c: (c[0] - 1, c[1])),
    "d": (lambda c: (c[0] + 1, c[1])),
    "l": (lambda c: (c[0], c[1] - 1)),
    "r": (lambda c: (c[0], c[1] + 1)),
}

SPLITS = {
    "u": ("l", "r"),
    "d": ("l", "r"),
    "l": ("u", "d"),
    "r": ("u", "d")
}


def parse_input(text: str) -> np.ndarray:
    grid = []
    for line in text.strip().split("\n"):
        grid.append(list(line.strip()))

    return np.array(grid)


def follow_path(grid: np.ndarray, coords: Tuple[int, int],
                direction: str, already_visited_grid_points: Dict[Tuple[int, int], List[str]]):
    i_max, j_max = grid.shape
    while True:
        coords_visited_directions = already_visited_grid_points.get(coords)
        if coords_visited_directions is not None:
            if direction in coords_visited_directions:
                return
            else:
                coords_visited_directions.append(direction)
        else:
            already_visited_grid_points[coords] = [direction]

        try:
            direction = ORIENTATIONS[direction][grid[coords]]
        except KeyError:
            # Splitting point reached
            dir1, dir2 = SPLITS[direction]
            follow_path(grid, coords, dir1, already_visited_grid_points)
            follow_path(grid, coords, dir2, already_visited_grid_points)
            return

        coords = DISPLACEMENTS[direction](coords)
        i, j = coords
        if i < 0 or i >= i_max:
            return
        if j < 0 or j >= j_max:
            return


def get_num_visited_points_starting_top_left(grid):
    already_visited_grid_points = {}
    follow_path(grid, (0, 0), "r", already_visited_grid_points)

    return len(already_visited_grid_points)


def get_max_num_visited_points(grid):
    i_max, j_max = grid.shape
    max_num_visited_points = 0

    # Light enters from the top
    for j in range(j_max):
        already_visited_grid_points = {}
        follow_path(grid, (0, j), "d", already_visited_grid_points)
        num_visited_points = len(already_visited_grid_points)
        if num_visited_points > max_num_visited_points:
            max_num_visited_points = num_visited_points

    # Light enters from the bottom
    for j in range(j_max):
        already_visited_grid_points = {}
        follow_path(grid, (i_max - 1, j), "u", already_visited_grid_points)
        num_visited_points = len(already_visited_grid_points)
        if num_visited_points > max_num_visited_points:
            max_num_visited_points = num_visited_points

    # Light enters from the left
    for i in range(i_max):
        already_visited_grid_points = {}
        follow_path(grid, (i, 0), "r", already_visited_grid_points)
        num_visited_points = len(already_visited_grid_points)
        if num_visited_points > max_num_visited_points:
            max_num_visited_points = num_visited_points

    # Light enters from the right
    for i in range(i_max):
        already_visited_grid_points = {}
        follow_path(grid, (i, j_max - 1), "l", already_visited_grid_points)
        num_visited_points = len(already_visited_grid_points)
        if num_visited_points > max_num_visited_points:
            max_num_visited_points = num_visited_points

    return max_num_visited_points


if __name__ == "__main__":
    with open("../inputs/input16.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    res = get_num_visited_points_starting_top_left(parse_input(in_text))
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_max_num_visited_points(parse_input(in_text))
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
