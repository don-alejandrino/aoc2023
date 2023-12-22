import time
from typing import Tuple, List

import numpy as np

EXAMPLE1 = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def parse_input(text: str) -> Tuple[np.ndarray, Tuple[int, int]]:
    lines = text.strip().split("\n")
    grid = np.empty((len(lines), len(lines[0].strip())), dtype=int)
    start_pos = (0, 0)
    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            if char == ".":
                grid[i, j] = 0
            elif char == "#":
                grid[i, j] = 1
            elif char == "S":
                grid[i, j] = 0
                start_pos = (i, j)
            else:
                raise ValueError(f"Unexpected input: {char}")

    return np.array(grid), start_pos


def get_reachable_garden_plots(grid: np.ndarray, starting_positions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    i_max, j_max = grid.shape
    reachable_plots = set()
    for i, j in starting_positions:
        # Go right
        if j + 1 < j_max and grid[i, j + 1] == 0:
            reachable_plots.add((i, j + 1))
        # Go down
        if i + 1 < i_max and grid[i + 1, j] == 0:
            reachable_plots.add((i + 1, j))
        # Go left
        if j - 1 >= 0 and grid[i, j - 1] == 0:
            reachable_plots.add((i, j - 1))
        # Go up
        if i - 1 >= 0 and grid[i - 1, j] == 0:
            reachable_plots.add((i - 1, j))

    return list(reachable_plots)


def get_reachable_garden_plots_on_infinite_grid(
        grid: np.ndarray,
        starting_positions: List[Tuple[Tuple[int, int], Tuple[int, int]]],
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    i_max, j_max = grid.shape
    reachable_plots = set()
    for (i, j), (grid_idx_i, grid_idx_j) in starting_positions:
        # Go right
        if j + 1 >= j_max:
            j_new = j + 1 - j_max
            new_grid_idx_j = grid_idx_j + 1
        else:
            j_new = j + 1
            new_grid_idx_j = grid_idx_j
        if grid[i, j_new] == 0:
            reachable_plots.add(((i, j_new), (grid_idx_i, new_grid_idx_j)))

        # Go down
        if i + 1 >= i_max:
            i_new = i + 1 - i_max
            new_grid_idx_i = grid_idx_i + 1
        else:
            i_new = i + 1
            new_grid_idx_i = grid_idx_i
        if grid[i_new, j] == 0:
            reachable_plots.add(((i_new, j), (new_grid_idx_i, grid_idx_j)))

        # Go left
        if j - 1 < 0:
            j_new = j - 1 + j_max
            new_grid_idx_j = grid_idx_j - 1
        else:
            j_new = j - 1
            new_grid_idx_j = grid_idx_j
        if grid[i, j_new] == 0:
            reachable_plots.add(((i, j_new), (grid_idx_i, new_grid_idx_j)))

        # Go up
        if i - 1 < 0:
            i_new = i - 1 + i_max
            new_grid_idx_i = grid_idx_i - 1
        else:
            i_new = i - 1
            new_grid_idx_i = grid_idx_i
        if grid[i_new, j] == 0:
            reachable_plots.add(((i_new, j), (new_grid_idx_i, grid_idx_j)))

    return list(reachable_plots)


def get_num_reachable_garden_plots_after_n_steps(grid: np.ndarray, start_pos: Tuple[int, int], n_steps: int) -> int:
    start_positions = [start_pos]
    for _ in range(n_steps):
        start_positions = get_reachable_garden_plots(grid, start_positions)

    return len(start_positions)


def get_num_reachable_garden_plots_after_26501365_steps_on_infinite_grid(
        grid: np.ndarray,
        start_pos: Tuple[int, int]
) -> int:
    """
    The infinite grid consists of a periodic repetition of the original block from the input. Due to the structure of
    this input (no rocks in the row and column of the starting point, starting position in the middle of the grid), the
    elf will leave the initial grid block first fully to the left, right, top, and bottom. That is, the reachable plots
    grow approximately like a square tilted by 45 degrees on the infinite grid. More precisely, the occupied grid blocks
    grow like the following:

                                                 3 3 3
                                               3 2 2 2 3
                                             3 2 1 1 1 2 3
                                             3 2 1 0 1 2 3
                                             3 2 1 1 1 2 3
                                               3 2 2 2 3
                                                 3 3 3

    Here, the numbers represent the number of cycles. A cycle is defined by the number of steps an elf needs to take to
    fully cross a block horizontally or vertically (0 is the initial "offset" cycle that takes only half the steps due
    to the elf starting in the middle of the initial block). That is, after the first cycle, 8 more blocks are occupied,
    after the second 12, after the third 16, and so on. This means that during the n-th cycle, 4 * (n + 1) additional
    blocks are occupied. Taking the cumulative sum using the triangular number, we get for the total number N of
    occupied blocks after n steps: N = 1 (offset) + 2 * n^2 + 6 * n. We thus see that the number of reachable garden
    plots must grow quadratically in n.

    Looking at the exact input dimensions, we see that the grid shape is 131x131. The elf starts at position (65, 65).
    That is, we have an offset of 65 and a cycle length of 131.
    Looking at the number of target steps, 26501365, we notice that 26501365 mod 131 = 65
    <=> (26501365 - 65) mod 131 = 0 and (26501365 - 65) // 202300, i.e., the elf stops exactly at the end of the cycle
    with n = 202300.
    Knowing the quadratic power law in n, we can find the exact number of reachable garden plots g via determining the
    coefficients of the polynomial g(n) = a * n^2 + b * n + c by calculating g(n) for three values of n (most
    conveniently for n = 0, 1, and 2; the corresponding numbers of steps are 65, 65 + 131, and 65 + 131 * 2).
    """
    n1 = 0
    n2 = 1
    n3 = 2
    g1 = g2 = 0
    start_positions = [(start_pos, (0, 0))]
    for s in range(65 + 131 * 2):
        start_positions = get_reachable_garden_plots_on_infinite_grid(grid, start_positions)
        if s == 64:
            g1 = len(start_positions)
        elif s == 64 + 131:
            g2 = len(start_positions)
    g3 = len(start_positions)
    n_mat = np.array([
        [n1 ** 2, n1, 1],
        [n2 ** 2, n2, 1],
        [n3 ** 2, n3, 1]
    ], dtype=int)

    a, b, c = list(np.linalg.solve(n_mat, np.array([g1, g2, g3], dtype=int)).astype(int))

    return a * 202300 ** 2 + b * 202300 + c


if __name__ == "__main__":
    with open("../inputs/input21.txt", "r") as fh:
        in_text = fh.read()

    # PART 1
    start = time.perf_counter()
    garden_grid, starting_position = parse_input(in_text)
    res = get_num_reachable_garden_plots_after_n_steps(garden_grid, starting_position, 64)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_num_reachable_garden_plots_after_26501365_steps_on_infinite_grid(garden_grid, starting_position)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
